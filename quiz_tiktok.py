"""
Quiz interactif automatisé pour TikTok Live
------------------------------------------
Ce script permet de créer un quiz interactif entièrement automatique pendant un livestream TikTok
où les spectateurs doivent compléter les réponses partiellement affichées.
"""

from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, ConnectEvent, DisconnectEvent
import asyncio
import json
import os
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import tkinter as tk
from tkinter import font
import time
import threading
import shutil
import locale
import pyttsx3

# Importation des modules d'amélioration
from config import (
    TIKTOK_USERNAME, SCORES_FILE, QUESTIONNAIRES_DIR, 
    DEFAULT_QUESTIONNAIRE, DEFAULT_TIME_LIMIT, DEFAULT_POINTS,
    SCORE_EXPIRATION_HOURS, MAX_ANSWER_LENGTH, ANSWER_SIMILARITY_THRESHOLD,
    TTS_ENABLED, TTS_VOICE_RATE, TTS_VOICE_VOLUME
)
from logger_setup import logger
from validators import validate_questions_file, sanitize_input

class Question:
    """Classe représentant une question du quiz avec réponse à compléter"""
    def __init__(self, text: str, answer: str, 
                revealed_indices: List[int] = None, 
                points: int = DEFAULT_POINTS, time_limit: int = DEFAULT_TIME_LIMIT):
        self.text = text
        self.answer = answer
        self.revealed_indices = revealed_indices or self.get_default_revealed_indices()
        self.points = points
        self.time_limit = time_limit
        self.active = False
        self.start_time: Optional[datetime] = None
        
    def get_default_revealed_indices(self) -> List[int]:
        """Génère aléatoirement les indices des lettres à révéler"""
        answer_length = len(self.answer)
        
        # Ne pas révéler de lettres si la réponse est très courte (1 ou 2 caractères)
        if answer_length <= 2:
            return []
            
        # Pour les réponses courtes (3-4 caractères), révéler une seule lettre
        if answer_length <= 4:
            return [random.randrange(answer_length)]
            
        # Pour les réponses plus longues, révéler environ 25% des lettres
        num_revealed = max(1, int(answer_length * 0.25))
        revealed = random.sample(range(answer_length), num_revealed)
        return revealed
        
    def get_masked_answer(self) -> str:
        """Retourne la réponse avec des tirets et quelques lettres révélées"""
        masked = []
        for i, char in enumerate(self.answer):
            if i in self.revealed_indices or char == ' ':
                masked.append(char)
            else:
                masked.append('_')
        return ' '.join(masked)
        
    def activate(self):
        """Active la question et démarre le chronomètre"""
        self.active = True
        self.start_time = datetime.now()
        
    def deactivate(self):
        """Désactive la question"""
        self.active = False
        
    def is_time_expired(self) -> bool:
        """Vérifie si le temps de réponse est écoulé"""
        if not self.active or self.start_time is None:
            return False
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return elapsed > self.time_limit
    
    def check_answer(self, answer: str) -> bool:
        """Vérifie si la réponse donnée est correcte"""
        # Liste des articles et mots à ignorer
        articles = ['le ', 'la ', 'les ', 'un ', 'une ', 'des ', 'l\'', 'du ', 'de ', 'des ']
        
        # Limiter la longueur de la réponse
        answer = sanitize_input(answer, max_length=MAX_ANSWER_LENGTH)
        
        # Nettoyer la réponse de l'utilisateur
        user_answer = answer.strip().lower()  # Convertir en minuscules
        # Supprimer les points et virgules à la fin
        user_answer = user_answer.rstrip('.,')
        
        # Supprimer les articles au début de la réponse utilisateur
        for article in articles:
            if user_answer.startswith(article):
                user_answer = user_answer[len(article):]
                break
        
        # Nettoyer la réponse correcte
        correct_answer = self.answer.strip().lower()  # Convertir en minuscules
        # Supprimer les points et virgules à la fin
        correct_answer = correct_answer.rstrip('.,')
        
        # Supprimer les articles au début de la réponse correcte
        for article in articles:
            if correct_answer.startswith(article):
                correct_answer = correct_answer[len(article):]
                break

        # Vérification directe après suppression des articles
        if user_answer == correct_answer:
            return True

        # Vérification avec les variations courantes
        variations = {
            correct_answer,
            correct_answer.replace(' ', ''),  # Sans espaces
            correct_answer.replace(' ', '-'),  # Avec tirets
            correct_answer.replace('-', ' ')   # Espaces au lieu des tirets
        }
        
        # Ajouter des variations avec les articles
        for article in articles:
            variations.add(article + correct_answer)
        
        # Vérifier si la réponse correspond à une des variations
        if user_answer in variations:
            return True
            
        # Vérification des mots individuels
        user_words = set(user_answer.split())
        correct_words = set(correct_answer.split())
        
        # Si tous les mots de la réponse correcte sont présents
        if correct_words and user_words.issuperset(correct_words):
            # Vérifier que la réponse n'est pas trop longue
            if len(user_words) <= len(correct_words) + 2:
                return True
        
        # Vérification de similarité pour les fautes de frappe
        if len(user_answer) > 2 and len(correct_answer) > 2:
            # Calculer la similarité
            if abs(len(user_answer) - len(correct_answer)) <= 2:
                common_chars = sum(1 for i in range(min(len(user_answer), len(correct_answer)))
                                 if user_answer[i] == correct_answer[i])
                if common_chars >= len(correct_answer) * 0.8:
                    return True
        
        return False
    
    def __str__(self) -> str:
        masked = self.get_masked_answer()
        return f"{self.text}\nRéponse: {masked}\n"

class QuizManager:
    """Gestionnaire du quiz"""
    def __init__(self, questions_file: str):
        self.questions: List[Question] = []
        self.current_question_index = -1
        self.current_question: Optional[Question] = None
        self.scores: Dict[str, Dict[str, int]] = {}  # {user_id: {"score": points, "name": nickname}}
        self.answered_users: List[str] = []
        self.correct_answer_found = False
        # Nom du fichier pour sauvegarder les scores
        self.scores_file = SCORES_FILE
        # Charger les scores existants s'ils sont valides (moins de 24h)
        self.load_scores()
        self.load_questions(questions_file)
        
    def normalize_text(self, text: str) -> str:
        """Normalise le texte en remplaçant les caractères spéciaux"""
        replacements = {
            'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
            'à': 'a', 'â': 'a', 'ä': 'a',
            'î': 'i', 'ï': 'i',
            'ô': 'o', 'ö': 'o',
            'ù': 'u', 'û': 'u', 'ü': 'u',
            'ç': 'c',
            "'": '', '"': '', ' ': ''
        }
        text = text.lower()
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def load_questions(self, file_path: str):
        """Charge les questions depuis un fichier JSON après validation"""
        try:
            # Utilisation du validateur pour sécuriser le chargement des questions
            questions_data = validate_questions_file(file_path)
                
            for q_data in questions_data:
                q = Question(
                    text=q_data["text"],
                    answer=q_data["answer"],
                    revealed_indices=q_data.get("revealed_indices"),
                    points=q_data.get("points", DEFAULT_POINTS),
                    time_limit=q_data.get("time_limit", DEFAULT_TIME_LIMIT)
                )
                self.questions.append(q)
                
            logger.info(f"Quiz chargé avec {len(self.questions)} questions")
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            logger.error(f"Erreur lors du chargement des questions: {e}")
            raise
    
    def save_scores(self):
        """Sauvegarde les scores actuels avec un timestamp"""
        scores_data = {
            "timestamp": datetime.now().timestamp(),
            "scores": self.scores
        }
        try:
            with open(self.scores_file, 'w', encoding='utf-8') as f:
                json.dump(scores_data, f, ensure_ascii=False, indent=4)
            logger.info(f"Scores sauvegardés dans {self.scores_file}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des scores: {e}")
    
    def load_scores(self):
        """Charge les scores sauvegardés s'ils existent et sont valides (moins de 24h)"""
        try:
            if not os.path.exists(self.scores_file):
                logger.info("Aucun fichier de scores existant.")
                return
                
            with open(self.scores_file, 'r', encoding='utf-8') as f:
                scores_data = json.load(f)
                
            # Vérifier si les scores sont encore valides (moins de 24h)
            saved_time = datetime.fromtimestamp(scores_data["timestamp"])
            current_time = datetime.now()
            time_diff = (current_time - saved_time).total_seconds()
            
            # Utilisation de la constante pour la durée de validité
            if time_diff <= SCORE_EXPIRATION_HOURS * 3600:
                self.scores = scores_data["scores"]
                logger.info(f"Scores chargés depuis {self.scores_file} (sauvegardés il y a {time_diff//3600:.1f} heures)")
            else:
                logger.info(f"Les scores sauvegardés ont expiré (plus de {SCORE_EXPIRATION_HOURS}h). Nouveau classement créé.")
                # Supprimer le fichier de scores périmé
                os.remove(self.scores_file)
        except Exception as e:
            logger.error(f"Erreur lors du chargement des scores: {e}")
            logger.info("Création d'un nouveau classement.")
    
    def next_question(self) -> Optional[Question]:
        """Passe à la question suivante"""
        if self.current_question:
            self.current_question.deactivate()
            
        self.current_question_index += 1
        self.answered_users = []
        self.correct_answer_found = False
        
        if self.current_question_index < len(self.questions):
            self.current_question = self.questions[self.current_question_index]
            self.current_question.activate()
            return self.current_question
        else:
            self.current_question = None
            # Sauvegarder les scores à la fin du quiz
            self.save_scores()
            return None
    
    def _is_valid_context(self) -> bool:
        """Vérifie si le contexte permet de traiter une réponse"""
        return (self.current_question and 
                self.current_question.active and 
                not self.correct_answer_found)
    
    def process_answer(self, user_id: str, username: str, answer: str) -> Tuple[bool, int]:
        """Traite la réponse d'un utilisateur"""
        # Validation du contexte
        if not self._is_valid_context():
            return False, 0
            
        # Vérifier que la question est toujours active
        if not self.current_question or not self.current_question.active:
            return False, 0
            
        if user_id in self.answered_users:
            return False, 0
            
        if self.current_question.is_time_expired():
            return False, 0
            
        # Ignorer les messages qui sont trop longs (plus de 3 mots)
        words = answer.strip().split()
        if len(words) > 3:
            return False, 0
            
        # Ignorer les messages qui contiennent des mots de test courants
        test_words = ["test", "essai", "fonctionne", "marche", "ok", "oui", "non", "bonjour", "salut", "hello"]
        if any(word.lower() in test_words for word in words):
            return False, 0
            
        # Ignorer uniquement les caractères spéciaux non autorisés (sauf apostrophes et accents)
        allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '-éèêëàâäîïôöùûüç")
        if any(c not in allowed_chars for c in answer):
            return False, 0
            
        # Vérifier que la question n'a pas déjà été résolue
        if self.correct_answer_found:
            return False, 0
            
        # Ajouter l'utilisateur à la liste des utilisateurs ayant répondu
        self.answered_users.append(user_id)
        
        # Vérifier la réponse
        is_correct = self.current_question.check_answer(answer)
        if is_correct:
            # Si c'est la première bonne réponse, marquer la question comme résolue
            self.correct_answer_found = True
            
            # Calculer les points gagnés
            points = self.current_question.points
            
            # Mettre à jour le score de l'utilisateur
            if user_id not in self.scores:
                self.scores[user_id] = {"score": 0, "name": username}
            
            self.scores[user_id]["score"] += points
            self.scores[user_id]["name"] = username  # Mettre à jour le nom au cas où
            
            # Sauvegarder les scores
            self.save_scores()
            
            logger.info(f"Réponse correcte de {username} ({user_id}): {points} points")
            return True, points
        
        return False, 0
    
    def get_leaderboard(self, limit: int = 10) -> List[Tuple[str, int, str]]:
        """Retourne le classement des meilleurs scores"""
        sorted_scores = sorted(
            [(uid, data["score"], data["name"]) for uid, data in self.scores.items()],
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_scores[:limit]
    
    def reset_scores(self) -> bool:
        """Réinitialise tous les scores"""
        try:
            self.scores = {}
            if os.path.exists(self.scores_file):
                os.remove(self.scores_file)
            logger.info("Classement réinitialisé avec succès")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la réinitialisation des scores: {e}")
            return False

    def start_from_question(self, question_number: int):
        """Reprend le quiz à partir d'une question spécifique"""
        if 0 <= question_number < len(self.questions):
            self.current_question_index = question_number - 1  # -1 car next_question() incrémente l'index
            self.answered_users = []
            self.correct_answer_found = False
            # Sauvegarder les scores actuels
            self.save_scores()
            # Passer à la question spécifiée
            return self.next_question()
        return None

class TikTokQuiz:
    """Classe principale pour le quiz TikTok Live"""
    def __init__(self, tiktok_username: str, questions_file: str):
        self.tiktok_username = tiktok_username
        self.client = TikTokLiveClient(unique_id=tiktok_username)
        self.quiz_manager = QuizManager(questions_file)
        self.quiz_running = False
        self.connection_retries = 0
        self.max_retries = 5
        self.retry_delay = 5  # secondes
        self.setup_listeners()
        
    def setup_listeners(self):
        """Configure les écouteurs d'événements"""
        @self.client.on(ConnectEvent)
        async def on_connect(event: ConnectEvent):
            print(f"\n✅ Connecté au live de @{event.unique_id}")
            self.connection_retries = 0  # Réinitialiser le compteur de tentatives
            print("Démarrage automatique du quiz dans 10 secondes...")
            await asyncio.sleep(10)  # Attendre 10 secondes avant de commencer
            await self.run_quiz()
            
        @self.client.on(CommentEvent)
        async def on_comment(event: CommentEvent):
            try:
                # Vérifier si le quiz est actif et si une question est en cours
                if not self.quiz_running:
                    return
                if not self.quiz_manager.current_question:
                    return
                if not self.quiz_manager.current_question.active:
                    return
                
                # Afficher le commentaire reçu
                print(f"💬 {event.user.nickname}: '{event.comment}'")
                
                # Traiter la réponse
                is_correct, points = self.quiz_manager.process_answer(
                    event.user.unique_id, 
                    event.user.nickname,
                    event.comment
                )
                
                if is_correct:
                    # Afficher la réponse correcte
                    print(f"\n✨ BONNE RÉPONSE! ✨")
                    print(f"✅ {event.user.nickname} a trouvé la réponse et gagne {points} points!")
                    print(f"📝 La réponse était: {self.quiz_manager.current_question.answer}")
                    
                    # Mettre à jour le score et désactiver la question
                    self.quiz_manager.current_question.deactivate()
                    self.quiz_manager.save_scores()  # Sauvegarder les scores immédiatement
                    
                    # Afficher le classement actuel
                    print("\n🏆 CLASSEMENT ACTUEL:")
                    leaderboard = self.quiz_manager.get_leaderboard(5)
                    for i, (_, score, name) in enumerate(leaderboard, 1):
                        if i == 1:
                            print(f"🥇 {name}: {score} points")
                        elif i == 2:
                            print(f"🥈 {name}: {score} points")
                        elif i == 3:
                            print(f"🥉 {name}: {score} points")
                        else:
                            print(f"{i}. {name}: {score} points")
                    
                    # Attendre avant de passer à la question suivante
                    print("\nPassage à la question suivante dans 3 secondes...")
                    await asyncio.sleep(3)
                    
            except Exception as e:
                logger.error(f"Erreur lors du traitement du commentaire: {e}")
                print(f"⚠️ Erreur lors du traitement du commentaire: {e}")
                    
        @self.client.on(DisconnectEvent)
        async def on_disconnect(_):
            print("\n❌ Déconnecté du live TikTok")
            self.quiz_running = False
            
            # Tenter de se reconnecter avec un nombre limité de tentatives
            if self.connection_retries < self.max_retries:
                self.connection_retries += 1
                print(f"Tentative de reconnexion ({self.connection_retries}/{self.max_retries}) dans {self.retry_delay} secondes...")
                try:
                    await asyncio.sleep(self.retry_delay)
                    await self.client.connect()
                except Exception as e:
                    logger.error(f"Échec de la reconnexion: {e}")
                    # Augmenter le délai entre les tentatives
                    self.retry_delay = min(self.retry_delay * 2, 30)  # Maximum 30 secondes
            else:
                print("Nombre maximum de tentatives de reconnexion atteint. Arrêt du quiz.")
                
    async def run_quiz(self):
        """Exécute le quiz automatiquement"""
        self.quiz_running = True
        print("\n🎮 DÉBUT DU QUIZ AUTOMATIQUE 🎮\n")
        
        # Réinitialiser l'index des questions
        self.quiz_manager.current_question_index = -1
        
        # Boucle principale du quiz
        while self.quiz_running:
            try:
                # Passer à la question suivante
                question = self.quiz_manager.next_question()
                
                if not question:
                    # Fin du quiz, toutes les questions ont été posées
                    print("\n🏁 FIN DU QUIZ 🏁")
                    await self.show_final_leaderboard()
                    self.quiz_running = False
                    break
                    
                print(f"\n----- Question {self.quiz_manager.current_question_index + 1}/{len(self.quiz_manager.questions)} -----")
                print(question)
                print(f"Temps de réponse: {question.time_limit} secondes")
                
                # Attendre soit que la réponse correcte soit trouvée, soit que le temps expire
                start_time = datetime.now()
                while question.active and (datetime.now() - start_time).total_seconds() < question.time_limit:
                    if self.quiz_manager.correct_answer_found:
                        # Une réponse correcte a été trouvée, on passe à la question suivante
                        break
                    await asyncio.sleep(0.1)  # Réduire le temps d'attente pour plus de réactivité
                
                # Terminer la question si elle est encore active
                if question.active:
                    question.deactivate()
                    print(f"⏱️ Temps écoulé! La bonne réponse était: {question.answer}")
                
                # Afficher le classement après chaque question
                await self.show_leaderboard()
                
                # Pause entre les questions
                print("\nProchaine question dans 5 secondes...")
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"Erreur pendant le quiz: {e}")
                # Continuer avec la question suivante en cas d'erreur
                continue
    
    async def show_leaderboard(self):
        """Affiche le classement actuel"""
        leaderboard = self.quiz_manager.get_leaderboard()
        print("\n----- CLASSEMENT ACTUEL -----")
        if not leaderboard:
            print("Aucun score pour l'instant.")
            return
            
        for i, (user_id, score, name) in enumerate(leaderboard):
            print(f"{i+1}. {name}: {score} points")
        
    async def show_final_leaderboard(self):
        """Affiche le classement final avec plus de détails"""
        leaderboard = self.quiz_manager.get_leaderboard()
        print("\n🏆 CLASSEMENT FINAL 🏆")
        if not leaderboard:
            print("Aucun participant n'a marqué de points.")
            return
            
        for i, (user_id, score, name) in enumerate(leaderboard):
            if i == 0:
                print(f"🥇 1. {name}: {score} points")
            elif i == 1:
                print(f"🥈 2. {name}: {score} points")
            elif i == 2:
                print(f"🥉 3. {name}: {score} points")
            else:
                print(f"{i+1}. {name}: {score} points")
        
    async def run_quiz_demo(self):
        """Version démo du quiz qui simule des réponses de spectateurs"""
        self.quiz_running = True
        print("\n🎮 DÉMO DU QUIZ - MODE SIMULATION 🎮\n")
        
        # Réinitialiser l'index des questions
        self.quiz_manager.current_question_index = -1
        
        # Créer quelques utilisateurs fictifs pour la démo
        demo_users = [
            {"id": "user1", "name": "Sophie"},
            {"id": "user2", "name": "Thomas"},
            {"id": "user3", "name": "Julie"},
            {"id": "user4", "name": "Lucas"},
            {"id": "user5", "name": "Emma"}
        ]
        
        # Boucle principale du quiz
        while self.quiz_running:
            # Passer à la question suivante
            question = self.quiz_manager.next_question()
            
            if not question:
                # Fin du quiz, toutes les questions ont été posées
                print("\n🏁 FIN DU QUIZ DÉMO 🏁")
                await self.show_final_leaderboard()
                self.quiz_running = False
                break
            
            print(f"\n----- Question {self.quiz_manager.current_question_index + 1}/{len(self.quiz_manager.questions)} -----")
            print(question)
            print(f"Temps de réponse: {question.time_limit} secondes")
            
            # Simuler des réponses aléatoires
            await asyncio.sleep(random.randint(3, 10))  # Attente aléatoire
            
            # 50% de chance d'avoir une bonne réponse
            if random.random() > 0.5:
                random_user = random.choice(demo_users)
                is_correct, points = self.quiz_manager.process_answer(
                    random_user["id"],
                    random_user["name"],
                    question.answer
                )
                
                if is_correct:
                    print(f"✅ {random_user['name']} a répondu correctement et gagne {points} points!")
            else:
                # Simuler quelques mauvaises réponses
                for _ in range(random.randint(1, 3)):
                    random_user = random.choice(demo_users)
                    bad_answer = question.answer + "X"  # Réponse incorrecte
                    self.quiz_manager.process_answer(random_user["id"], random_user["name"], bad_answer)
                    print(f"❌ {random_user['name']} a tenté une réponse incorrecte.")
                    await asyncio.sleep(2)
            
            # Attendre la fin du temps
            remaining_time = question.time_limit - random.randint(5, 15)
            if remaining_time > 0:
                await asyncio.sleep(remaining_time)
            
            # Terminer la question
            question.deactivate()
            print(f"⏱️ Temps écoulé! La bonne réponse était: {question.answer}")
            
            # Afficher le classement après chaque question
            await self.show_leaderboard()
            
            # Pause entre les questions
            print("\nProchaine question dans 5 secondes...")
            await asyncio.sleep(5)
        
    def run(self):
        """Lance le client TikTok Live"""
        print(f"\n🎮 Connexion au live de @{self.tiktok_username}...")
        print("En attente de la connexion au stream...")
        
        while True:
            try:
                self.client.run()
            except Exception as e:
                logger.error(f"Erreur de connexion: {e}")
                if self.connection_retries < self.max_retries:
                    self.connection_retries += 1
                    retry_delay = min(self.retry_delay * (2 ** self.connection_retries), 30)
                    print(f"\n⚠️ Tentative de reconnexion ({self.connection_retries}/{self.max_retries}) dans {retry_delay} secondes...")
                    time.sleep(retry_delay)
                else:
                    print("\n❌ Nombre maximum de tentatives atteint. Veuillez vérifier:")
                    print("1. Que le stream TikTok est bien actif")
                    print("2. Que le nom d'utilisateur est correct")
                    print("3. Votre connexion internet")
                    print("\nRedémarrez le programme pour réessayer.")
                    break

class TikTokQuizGUI:
    """Classe combinant l'interface graphique et la connexion TikTok Live"""
    def __init__(self, root, tiktok_username, questions_file=None, start_question=1):
        self.root = root
        self.root.title("Quiz TikTok Live")
        self.root.geometry("400x700")
        self.root.configure(bg="#000000")
        
        # Configurer la transparence de la fenêtre
        self.root.attributes('-alpha', 0.9)  # Légère transparence pour la fenêtre
        self.root.attributes('-transparentcolor', '#000000')  # Rendre le noir transparent
        
        # Initialiser le gestionnaire de questionnaires
        self.questionnaire_manager = QuestionnaireManager()
        
        # Forcer l'utilisation du questionnaire culture_quizz au démarrage
        questions_file = os.path.join("questionnaires", "questions_culture_quizz.json")
        if not os.path.exists(questions_file):
            print(f"Questionnaire {questions_file} non trouvé!")
            questions_file = self.questionnaire_manager.get_next_questionnaire_path()
        
        # Initialiser le quiz manager
        self.quiz_manager = QuizManager(questions_file)
        
        # Initialiser le moteur TTS si activé
        self.tts_engine = None
        if TTS_ENABLED:
            self.init_tts_engine()
        
        # Création des polices et interface
        self.setup_gui()
        
        # Variables pour suivre l'état du quiz
        self.current_question_index = 0
        self.timer_count = 40
        self.is_running = True
        self.timer_id = None  # Pour stocker l'identifiant du timer actuel
        
        # Si une question de départ est spécifiée, la configurer
        self.start_question = start_question
        
        # Ajouter un verrou pour le TTS
        self.tts_lock = threading.Lock()
        self.current_tts_thread = None

        # Initialiser le client TikTok Live
        self.tiktok_client = TikTokLiveClient(unique_id=tiktok_username)
        self.setup_tiktok_listeners()

    def setup_tiktok_listeners(self):
        """Configure les écouteurs d'événements TikTok"""
        @self.tiktok_client.on(ConnectEvent)
        async def on_connect(_):
            print("✅ Connecté au live TikTok!")
            
        @self.tiktok_client.on(CommentEvent)
        async def on_comment(event):
            if self.is_running and self.quiz_manager.current_question and self.quiz_manager.current_question.active:
                print(f"💬 {event.user.nickname}: {event.comment}")
                is_correct, points = self.quiz_manager.process_answer(
                    event.user.unique_id,
                    event.user.nickname,
                    event.comment
                )
                if is_correct:
                    self.show_correct_answer(event.user.nickname)
                    
        @self.tiktok_client.on(DisconnectEvent)
        async def on_disconnect(_):
            print("❌ Déconnecté du live TikTok")
            # Tenter de se reconnecter
            try:
                await self.tiktok_client.connect()
            except Exception as e:
                print(f"Erreur de reconnexion: {e}")

    def init_tts_engine(self):
        """Initialise le moteur de synthèse vocale"""
        if not TTS_ENABLED:
            print("TTS: Désactivé dans la configuration")
            return

        try:
            # Vérifier si nous avons les permissions nécessaires
            import ctypes
            import sys
            
            def is_admin():
                try:
                    return ctypes.windll.shell32.IsUserAnAdmin()
                except:
                    return False
            
            if not is_admin():
                print("TTS: Attention - L'application n'a pas les droits administrateur")
                print("TTS: Certaines fonctionnalités vocales pourraient ne pas fonctionner")
            
            # Initialiser le moteur avec SAPI5
            try:
                self.tts_engine = pyttsx3.init(driverName='sapi5')
            except Exception as e:
                print(f"TTS: Erreur lors de l'initialisation du moteur: {e}")
                self.tts_engine = None
                return
                
            # Vérifier si le moteur est bien initialisé
            if not self.tts_engine:
                print("TTS: Échec de l'initialisation du moteur")
                return
                
            # Configurer le taux de parole et le volume
            try:
                self.tts_engine.setProperty('rate', TTS_VOICE_RATE)
                self.tts_engine.setProperty('volume', TTS_VOICE_VOLUME)
            except Exception as e:
                print(f"TTS: Erreur lors de la configuration des propriétés: {e}")
            
            # Essayer de configurer une voix française si disponible
            try:
                voices = self.tts_engine.getProperty('voices')
                print(f"TTS: {len(voices)} voix trouvées")
                
                for voice in voices:
                    print(f"TTS: Voix disponible - {voice.id}")
                    if 'french' in voice.id.lower() or 'fr' in voice.id.lower():
                        try:
                            self.tts_engine.setProperty('voice', voice.id)
                            print(f"TTS: Voix française sélectionnée: {voice.id}")
                            break
                        except Exception as e:
                            print(f"TTS: Erreur lors de la configuration de la voix {voice.id}: {e}")
                            continue
            except Exception as e:
                print(f"TTS: Erreur lors de la configuration de la voix: {e}")
            
            print("TTS: Initialisation terminée")
            
        except Exception as e:
            print(f"TTS: Erreur globale lors de l'initialisation: {e}")
            self.tts_engine = None
    
    def clean_text_for_tts(self, text: str) -> str:
        """Nettoie le texte pour la synthèse vocale"""
        # Supprimer les emojis et autres caractères spéciaux
        cleaned = ""
        for char in text:
            # Ne garder que les caractères imprimables de base et les accents français
            if char.isprintable() and (char.isascii() or char in "éèêëàâäîïôöùûüçÉÈÊËÀÂÄÎÏÔÖÙÛÜÇ"):
                cleaned += char
        return cleaned

    def speak_text(self, text):
        """Lit le texte à voix haute en utilisant le moteur TTS"""
        if not TTS_ENABLED:
            return
            
        # Nettoyer le texte avant la lecture
        text = self.clean_text_for_tts(text)
        if not text.strip():
            return
            
        def speak_worker():
            engine = None
            with self.tts_lock:  # Utiliser le verrou pour éviter les conflits
                try:
                    # Créer un nouveau moteur pour chaque lecture
                    engine = pyttsx3.init(driverName='sapi5')  # Forcer l'utilisation de SAPI5 sur Windows
                    if not engine:
                        print("TTS: Échec de création du moteur")
                        return
                        
                    # Configurer le moteur
                    engine.setProperty('rate', TTS_VOICE_RATE)
                    engine.setProperty('volume', TTS_VOICE_VOLUME)
                    
                    # Configurer la voix française
                    voices = engine.getProperty('voices')
                    for voice in voices:
                        if 'french' in voice.id.lower() or 'fr' in voice.id.lower():
                            engine.setProperty('voice', voice.id)
                            break
                    
                    # Utiliser directement runAndWait() dans le thread dédié
                    engine.say(text)
                    engine.runAndWait()
                    
                except RuntimeError as re:
                    if "run loop already started" in str(re):
                        print("TTS: Tentative de relecture...")
                        try:
                            # Attendre un peu et réessayer
                            time.sleep(0.1)
                            engine = pyttsx3.init(driverName='sapi5')
                            engine.say(text)
                            engine.runAndWait()
                        except Exception as e2:
                            print(f"TTS: Échec de la seconde tentative: {e2}")
                    else:
                        print(f"TTS: Erreur runtime: {re}")
                except Exception as e:
                    print(f"TTS: Erreur lors de la lecture: {e}")
                finally:
                    if engine:
                        try:
                            engine.stop()
                        except:
                            pass
        
        # Arrêter le thread TTS précédent s'il existe
        if hasattr(self, 'current_tts_thread') and self.current_tts_thread and self.current_tts_thread.is_alive():
            try:
                self.current_tts_thread.join(timeout=0.5)
            except:
                pass
        
        # Démarrer un nouveau thread
        try:
            self.current_tts_thread = threading.Thread(target=speak_worker, daemon=True)
            self.current_tts_thread.start()
        except Exception as e:
            print(f"TTS: Erreur lors du démarrage du thread: {e}")
    
    def setup_gui(self):
        # Création des polices
        self.title_font = font.Font(family="Arial", size=12, weight="bold")
        self.question_font = font.Font(family="Arial", size=18, weight="bold")
        self.timer_font = font.Font(family="Arial", size=32, weight="bold")  # Augmentation de la taille
        self.answer_font_large = font.Font(family="Arial", size=22)  # Police grande pour réponses courtes
        self.answer_font_medium = font.Font(family="Arial", size=18)  # Police moyenne pour réponses moyennes
        self.answer_font_small = font.Font(family="Arial", size=14)  # Police petite pour réponses longues
        self.score_font = font.Font(family="Arial", size=10)
        
        # Création des frames avec un fond semi-transparent
        self.header_frame = tk.Frame(self.root, bg="#232323", height=60)  # Augmentation de la hauteur
        self.header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Frame pour le timer et le compteur de questions
        self.info_frame = tk.Frame(self.header_frame, bg="#232323")
        self.info_frame.pack(side=tk.RIGHT, padx=15)  # Plus d'espace à droite
        
        self.question_frame = tk.Frame(self.root, bg="#232323")
        self.question_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.answer_frame = tk.Frame(self.root, bg="#232323")
        self.answer_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Frame pour l'objectif de likes
        self.likes_frame = tk.Frame(self.root, bg="#232323")
        self.likes_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Frame pour les scores placée après les likes
        self.scores_frame = tk.Frame(self.root, bg="#232323")
        self.scores_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Création des éléments d'interface
        self.setup_interface()
        
    def setup_interface(self):
        # Header
        self.date_label = tk.Label(self.header_frame, text="", 
                            bg="#232323", fg="white", font=self.title_font)
        self.date_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Initialiser et mettre à jour la date et l'heure
        self.update_datetime()
        
        # Conteneur pour le compteur de questions et le timer
        self.info_frame = tk.Frame(self.header_frame, bg="#232323")
        self.info_frame.pack(side=tk.RIGHT, padx=15)  # Plus d'espace à droite
        
        self.question_count = tk.Label(self.info_frame, text="Question 1/65", 
                               bg="#232323", fg="white", font=self.title_font)
        self.question_count.pack(side=tk.LEFT, padx=(0,15))  # Plus d'espace entre le compteur et le timer
        
        # Timer à droite du compteur
        self.timer_label = tk.Label(self.info_frame, text="40", 
                            bg="#232323", fg="#FF3333", font=self.timer_font)
        self.timer_label.pack(side=tk.LEFT, padx=(0,10), pady=5)  # Ajout de padding vertical
        
        # Question
        self.question_label = tk.Label(self.question_frame, text="En attente de connexion...", 
                               bg="#232323", fg="white", font=self.question_font,
                               wraplength=350, justify="center")
        self.question_label.pack(padx=20, pady=30)
        
        # Réponse
        self.answer_label = tk.Label(self.answer_frame, text="", 
                              bg="#232323", fg="white", font=self.answer_font_large)
        self.answer_label.pack(pady=20)
        
        # Titre de l'objectif
        self.likes_title = tk.Label(self.likes_frame, text="OBJECTIF LIKES ❤️", 
                             bg="#232323", fg="#FF69B4", font=self.title_font)
        self.likes_title.pack(pady=(5,0))
        
        # Conteneur pour la barre de progression
        self.likes_progress_frame = tk.Frame(self.likes_frame, bg="#232323")
        self.likes_progress_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Objectif actuel / total
        self.likes_count = tk.Label(self.likes_progress_frame, text="0 / 1000", 
                             bg="#232323", fg="#FF69B4", font=self.title_font)
        self.likes_count.pack(side=tk.TOP, pady=2)
        
        # Barre de progression avec coins arrondis
        self.likes_progress = tk.Canvas(self.likes_progress_frame, 
                                height=20, bg="#333333", highlightthickness=0)
        self.likes_progress.pack(fill=tk.X, pady=2)
        
        # Initialiser la barre de progression
        self.update_likes_progress(0, 1000)
        
        # Scores
        self.scores_title_frame = tk.Frame(self.scores_frame, bg="#232323")
        self.scores_title_frame.pack(fill=tk.X, pady=(10, 5))
        
        self.scores_title = tk.Label(self.scores_title_frame, text="TOP SCORES", 
                              bg="#232323", fg="gold", font=self.title_font)
        self.scores_title.pack(side=tk.LEFT, padx=10)
        
        # Bouton de réinitialisation du classement
        self.reset_scores_button = tk.Button(self.scores_title_frame, text="Réinitialiser", 
                                    bg="#FF3333", fg="white", font=font.Font(family="Arial", size=8),
                                    command=self.reset_scores)
        self.reset_scores_button.pack(side=tk.RIGHT, padx=10)
        
        # Créer un canvas avec scrollbar pour les scores
        self.scores_canvas = tk.Canvas(self.scores_frame, bg="#232323", 
                                     highlightthickness=0, width=380)
        self.scores_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Ajouter une scrollbar
        self.scores_scrollbar = tk.Scrollbar(self.scores_frame, orient="vertical", 
                                           command=self.scores_canvas.yview)
        self.scores_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurer le canvas
        self.scores_canvas.configure(yscrollcommand=self.scores_scrollbar.set)
        
        # Frame pour contenir les labels de score
        self.scores_container = tk.Frame(self.scores_canvas, bg="#232323")
        self.scores_canvas.create_window((380, 0), window=self.scores_container, anchor="ne")
        
        # Créer les labels pour les scores
        self.score_labels = []
        for i in range(10):
            score_label = tk.Label(self.scores_container, 
                                 text="...", 
                                 bg="#232323", fg="white", font=self.score_font,
                                 anchor="e", justify="right")
            score_label.pack(pady=2)
            self.score_labels.append(score_label)
            
        # Configurer le scrolling
        self.scores_container.bind("<Configure>", lambda e: self.scores_canvas.configure(
            scrollregion=self.scores_canvas.bbox("all")))

    def update_datetime(self):
        """Met à jour la date et l'heure en temps réel"""
        now = datetime.now()
        
        # Essayer de définir la locale française
        try:
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')  # Pour Linux/Mac
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, 'fra_fra')  # Pour Windows
            except locale.Error:
                try:
                    locale.setlocale(locale.LC_TIME, 'fr')  # Alternative simplifiée
                except locale.Error:
                    print("Impossible de définir la locale en français, utilisation de la locale par défaut")
            
        # Format : Jour Numéro Mois Année + Heure:Minute:Seconde
        date_text = now.strftime("%A %d %B %Y\n%H:%M:%S")
        
        # Traduction manuelle si la locale ne fonctionne pas
        jours_fr = {"Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi", 
                    "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi", 
                    "Sunday": "Dimanche"}
        mois_fr = {"January": "Janvier", "February": "Février", "March": "Mars", 
                  "April": "Avril", "May": "Mai", "June": "Juin", 
                  "July": "Juillet", "August": "Août", "September": "Septembre", 
                  "October": "Octobre", "November": "Novembre", "December": "Décembre"}
        
        # Remplacer les jours et mois anglais par leurs équivalents français
        for en, fr in jours_fr.items():
            date_text = date_text.replace(en, fr)
        for en, fr in mois_fr.items():
            date_text = date_text.replace(en, fr)
        
        self.date_label.config(text=date_text)
        # Mettre à jour toutes les secondes
        self.root.after(1000, self.update_datetime)
    
    def start_quiz(self):
        """Démarre le quiz"""
        # Afficher l'information sur la validité des scores
        if os.path.exists(self.quiz_manager.scores_file):
            try:
                with open(self.quiz_manager.scores_file, 'r', encoding='utf-8') as f:
                    scores_data = json.load(f)
                saved_time = datetime.fromtimestamp(scores_data["timestamp"])
                current_time = datetime.now()
                time_diff = (current_time - saved_time).total_seconds() / 3600  # en heures
                if time_diff <= 24:
                    self.question_label.config(text=f"Classement chargé!\nSauvegardé il y a {time_diff:.1f} heures")
                    # Mise à jour immédiate des scores
                    self.update_scores()
                    self.root.after(3000, lambda: self.question_label.config(text="Quiz démarré!"))
                else:
                    self.question_label.config(text="Nouveau classement créé!")
                    self.root.after(3000, lambda: self.question_label.config(text="Quiz démarré!"))
            except Exception:
                self.question_label.config(text="Nouveau classement créé!")
                self.root.after(3000, lambda: self.question_label.config(text="Quiz démarré!"))
        else:
            self.question_label.config(text="Nouveau classement créé!")
            self.root.after(3000, lambda: self.question_label.config(text="Quiz démarré!"))
            
        # Démarrer à partir de la question spécifiée
        if hasattr(self, 'start_question') and self.start_question > 1:
            self.quiz_manager.start_from_question(self.start_question)
        
        # S'assurer que le quiz est bien en cours d'exécution
        self.is_running = True
        # Démarrer la première question après l'affichage du message
        self.root.after(3500, self.next_question)

    def get_appropriate_font(self, text):
        """Retourne la police appropriée en fonction de la longueur du texte"""
        length = len(text)
        if length <= 15:
            return self.answer_font_large
        elif length <= 30:
            return self.answer_font_medium
        else:
            return self.answer_font_small

    def next_question(self):
        """Affiche la prochaine question"""
        # Annuler tout timer précédent
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
            
        question = self.quiz_manager.next_question()
        if question:
            # Afficher la question immédiatement
            self.question_label.config(text=question.text)
            self.question_count.config(text=f"Question {self.quiz_manager.current_question_index+1}/{len(self.quiz_manager.questions)}")
            
            # Obtenir la réponse masquée et ajuster la taille de la police
            masked_answer = question.get_masked_answer()
            appropriate_font = self.get_appropriate_font(masked_answer)
            self.answer_label.config(text=masked_answer, fg="white", font=appropriate_font)
            
            # Réinitialiser et démarrer le timer
            self.timer_count = question.time_limit
            self.timer_label.config(text=str(self.timer_count))
            self.update_timer()
            
            # Essayer de lire la question
            try:
                self.speak_text(question.text)
            except Exception as e:
                print(f"TTS: Erreur lors de la lecture de la question: {e}")
        else:
            # Fin du quiz actuel
            self.question_label.config(text="Quiz terminé!")
            self.answer_label.config(text="")
            self.timer_label.config(text="0")
            
            # Attendre un court instant avant de lire le message de fin
            self.root.after(100, lambda: self.speak_text("Quiz terminé!"))
            
            # Attendre quelques secondes puis passer au questionnaire suivant
            self.timer_id = self.root.after(5000, self.load_next_questionnaire)
    
    def load_next_questionnaire(self):
        """Charge le questionnaire suivant et redémarre le quiz"""
        # Afficher un message de transition
        self.question_label.config(text="Chargement du prochain thème...")
        
        # Charger le prochain questionnaire
        questionnaire_file = self.questionnaire_manager.get_next_questionnaire_path()
        theme = self.questionnaire_manager.get_current_theme()
        
        # Informer l'utilisateur du changement de thème
        message = f"Nouveau thème: {theme}"
        self.question_label.config(text=message)
        self.speak_text(message)
        
        # Réinitialiser le quiz avec le nouveau questionnaire
        self.quiz_manager = QuizManager(questionnaire_file)
        
        # Attendre quelques secondes puis démarrer le nouveau quiz
        self.timer_id = self.root.after(3000, self.start_quiz)
            
    def update_timer(self):
        """Met à jour le timer"""
        # Vérifier que le timer est actif et que le quiz est en cours
        if self.timer_count > 0 and self.is_running:
            self.timer_count -= 1
            self.timer_label.config(text=str(self.timer_count))
            # Planifier la prochaine mise à jour dans 1 seconde
            self.timer_id = self.root.after(1000, self.update_timer)
        elif self.is_running:
            # Temps écoulé, passer à la question suivante
            if self.quiz_manager.current_question:
                self.quiz_manager.current_question.deactivate()
                self.answer_label.config(text=self.quiz_manager.current_question.answer, fg="orange")
                self.question_label.config(text="Temps écoulé!")
                # Passer à la question suivante après un délai
                self.timer_id = self.root.after(3000, self.next_question)
    
    def show_correct_answer(self, username):
        """Affiche la réponse correcte et le gagnant"""
        current_q = self.quiz_manager.current_question
        if current_q:
            # Arrêter le compte à rebours actuel
            if self.timer_id is not None:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
                
            # Désactiver la question
            self.timer_count = 0
            current_q.deactivate()
            
            # Nettoyer le nom d'utilisateur pour l'affichage
            clean_username = self.clean_text_for_tts(username)
            
            # Ajuster la taille de la police pour la réponse
            appropriate_font = self.get_appropriate_font(current_q.answer)
            self.answer_label.config(text=current_q.answer, fg="green", font=appropriate_font)
            
            display_message = f"{username} a trouvé la bonne réponse!"
            self.question_label.config(text=display_message)
            
            # Annoncer le gagnant et la bonne réponse
            announcement = f"{clean_username} a trouvé la bonne réponse! La réponse était: {current_q.answer}"
            print(f"TTS: Annonce de la bonne réponse: {announcement}")
            
            # Attendre un court instant avant de lire l'annonce
            self.root.after(500, lambda: self.speak_text(announcement))
            
            # Mettre à jour l'affichage des scores
            self.update_scores()
            
            # Passer à la question suivante après un délai
            self.timer_id = self.root.after(3000, self.next_question)
    
    def update_scores(self):
        """Met à jour l'affichage des scores"""
        leaderboard = self.quiz_manager.get_leaderboard(10)  # Augmenté à 10 joueurs
        
        for i, label in enumerate(self.score_labels):
            if i < len(leaderboard):
                user_id, score, name = leaderboard[i]
                # Formater le texte avec une largeur fixe pour un meilleur alignement
                if i == 0:
                    text = f"🥇 {name:<20}: {score:>4} points"
                    label.config(text=text, fg="gold")
                elif i == 1:
                    text = f"🥈 {name:<20}: {score:>4} points"
                    label.config(text=text, fg="silver")
                elif i == 2:
                    text = f"🥉 {name:<20}: {score:>4} points"
                    label.config(text=text, fg="#CD7F32")  # Bronze
                elif i < 5:
                    text = f"{i+1}. {name:<20}: {score:>4} points"
                    label.config(text=text, fg="#00FF00")  # Vert pour top 5
                else:
                    text = f"{i+1}. {name:<20}: {score:>4} points"
                    label.config(text=text, fg="white")
            else:
                label.config(text="...")
    
    def reset_scores(self):
        """Réinitialise le classement et met à jour l'affichage"""
        if self.quiz_manager.reset_scores():
            # Mettre à jour l'affichage
            for label in self.score_labels:
                label.config(text="...")
            # Afficher un message de confirmation
            self.question_label.config(text="Classement réinitialisé!")
            # Revenir à l'état normal après 3 secondes
            if self.quiz_manager.current_question:
                self.root.after(3000, lambda: self.question_label.config(text=self.quiz_manager.current_question.text))
    
    def cleanup_tts(self):
        """Nettoie les ressources du TTS"""
        # Attendre la fin du thread TTS en cours s'il existe
        if hasattr(self, 'current_tts_thread') and self.current_tts_thread and self.current_tts_thread.is_alive():
            try:
                self.current_tts_thread.join(timeout=1.0)
            except:
                pass

    def start(self):
        """Démarre l'application"""
        # Configurer la gestion de fermeture propre
        def on_closing():
            self.is_running = False
            if self.timer_id is not None:
                self.root.after_cancel(self.timer_id)
            
            # Nettoyer le moteur TTS avant de quitter
            self.cleanup_tts()
            
            # Fermer la connexion TikTok
            try:
                self.tiktok_client.stop()
            except:
                pass
                
            self.root.destroy()
            
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Démarrer la connexion TikTok dans un thread séparé
        def run_tiktok():
            asyncio.set_event_loop(asyncio.new_event_loop())
            self.tiktok_client.run()

        threading.Thread(target=run_tiktok, daemon=True).start()
        
        # Démarrer le quiz
        self.start_quiz()
        
        # Démarrer la boucle principale Tkinter
        self.root.mainloop()

    def update_likes_progress(self, current_likes: int, total_likes: int):
        """Met à jour la barre de progression des likes"""
        # Mettre à jour le texte
        self.likes_count.config(text=f"{current_likes} / {total_likes}")
        
        # Calculer le pourcentage
        progress = min(1.0, current_likes / total_likes)
        
        # Mettre à jour la barre de progression
        self.likes_progress.delete("all")
        width = self.likes_progress.winfo_width()
        if width > 0:  # S'assurer que le widget est visible
            # Dessiner le fond
            self.likes_progress.create_rectangle(0, 0, width, 20, 
                                              fill="#333333", outline="")
            
            # Dessiner la barre de progression
            if progress > 0:
                progress_width = int(width * progress)
                self.likes_progress.create_rectangle(0, 0, progress_width, 20,
                                                  fill="#FF69B4", outline="")
                
                # Ajouter un effet de brillance
                self.likes_progress.create_rectangle(0, 0, progress_width, 10,
                                                  fill="#FF99CC", outline="", stipple="gray50")

    def on_like_event(self, likes_count: int):
        """Appelé quand un nouveau like est reçu"""
        self.update_likes_progress(likes_count, 1000)  # Objectif fixe de 1000 likes

class QuestionnaireManager:
    """Gestionnaire des questionnaires multiples"""
    def __init__(self, questionnaires_dir="questionnaires"):
        self.questionnaires_dir = questionnaires_dir
        self.index_file = os.path.join(questionnaires_dir, "index.json")
        self.current_questionnaire_index = 0
        self.questionnaires_list = []
        
        # Vérifier si le dossier existe
        if not os.path.exists(questionnaires_dir):
            os.makedirs(questionnaires_dir)
            print(f"Dossier '{questionnaires_dir}' créé avec succès!")
            
        # Charger l'index s'il existe, sinon le créer
        self.load_questionnaires_index()
            
    def load_questionnaires_index(self):
        """Charge la liste des questionnaires disponibles"""
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    self.questionnaires_list = json.load(f)
                print(f"Index des questionnaires chargé: {len(self.questionnaires_list)} questionnaires disponibles")
            except Exception as e:
                print(f"Erreur lors du chargement de l'index: {e}")
                self.create_default_index()
        else:
            print("Index des questionnaires non trouvé, création d'un index par défaut")
            self.create_default_index()
            
    def create_default_index(self):
        """Crée un index par défaut avec les questionnaires existants"""
        self.questionnaires_list = []
        
        # Chercher les fichiers existants dans le dossier
        files = [f for f in os.listdir(self.questionnaires_dir) 
                if f.startswith("questionnaire_") and f.endswith(".json")]
        
        # Si des fichiers existent, les ajouter à l'index
        if files:
            for file in sorted(files):
                theme = file.replace("questionnaire_", "").replace(".json", "")
                id = int(theme) if theme.isdigit() else len(self.questionnaires_list) + 1
                self.questionnaires_list.append({"id": id, "theme": f"Questionnaire {id}", "file": file})
        
        # Si aucun fichier n'existe, ajouter les deux questionnaires originaux
        if not self.questionnaires_list:
            self.questionnaires_list = [
                {"id": 1, "theme": "Culture générale", "file": "questionnaire_1.json"},
                {"id": 2, "theme": "Divertissement", "file": "questionnaire_2.json"}
            ]
            
        # Enregistrer l'index
        self.save_index()
    
    def save_index(self):
        """Enregistre l'index des questionnaires"""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.questionnaires_list, f, ensure_ascii=False, indent=4)
            print("Index des questionnaires sauvegardé avec succès!")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'index: {e}")
    
    def get_next_questionnaire_path(self):
        """Retourne le chemin du prochain questionnaire à utiliser"""
        # Charger ou rafraîchir l'index pour s'assurer que nous avons les dernières mises à jour
        self.load_questionnaires_index()
        
        # Vérifier si l'index contient des questionnaires
        if self.questionnaires_list:
            # Incrémenter l'index du questionnaire actuel
            self.current_questionnaire_index = (self.current_questionnaire_index + 1) % len(self.questionnaires_list)
            questionnaire = self.questionnaires_list[self.current_questionnaire_index]
            
            # Construire le chemin du fichier
            if "file" in questionnaire:
                file_path = os.path.join(self.questionnaires_dir, questionnaire["file"])
            else:
                file_path = os.path.join(self.questionnaires_dir, f"questionnaire{questionnaire['id']}.json")
            
            # Vérifier si le fichier existe
            if os.path.exists(file_path):
                print(f"Utilisation du questionnaire {file_path}")
                return file_path
            
            # Si le fichier n'existe pas dans le dossier questionnaires, essayer à la racine
            root_path = questionnaire["file"]
            if os.path.exists(root_path):
                print(f"Utilisation du questionnaire à la racine: {root_path}")
                return root_path
            
            print(f"Questionnaire {file_path} non trouvé, recherche d'une alternative...")
        else:
            print("Aucun questionnaire listé dans l'index.")
                
        # Plan B: rechercher directement les fichiers questionnaire*.json dans le dossier
        questionnaire_files = []
        if os.path.exists(self.questionnaires_dir):
            for file in os.listdir(self.questionnaires_dir):
                if file.startswith("questionnaire") and file.endswith(".json") and "index" not in file:
                    questionnaire_files.append(os.path.join(self.questionnaires_dir, file))
            
            if questionnaire_files:
                selected_file = questionnaire_files[0]  # Prendre le premier trouvé
                print(f"Utilisation du questionnaire trouvé automatiquement: {selected_file}")
                return selected_file
                
        # Plan C: fallback sur les questionnaires à la racine du projet
        root_questionnaires = []
        for i in range(1, 6):  # Chercher questionnaire1.json à questionnaire5.json
            file_path = f"questionnaire{i}.json"
            if os.path.exists(file_path):
                root_questionnaires.append(file_path)
                
        if root_questionnaires:
            selected_path = root_questionnaires[0]  # Prendre le premier disponible
            print(f"Utilisation du questionnaire à la racine: {selected_path}")
            return selected_path
            
        # Dernier recours: utiliser le questionnaire par défaut
        print("Aucun questionnaire trouvé, utilisation du questionnaire par défaut")
        return DEFAULT_QUESTIONNAIRE
    
    def get_current_theme(self):
        """Retourne le thème du questionnaire actuel"""
        # Si on utilise les questionnaires de la racine
        root_questionnaires = []
        for i in range(1, 6):
            file_path = f"questionnaire{i}.json"
            if os.path.exists(file_path):
                root_questionnaires.append(file_path)
                
        if root_questionnaires and 0 <= self.current_questionnaire_index < len(root_questionnaires):
            current_file = root_questionnaires[self.current_questionnaire_index]
            # Déterminer le thème en fonction du nom du fichier
            themes = {
                "questionnaire1.json": "Culture générale 1",
                "questionnaire2.json": "Cinéma et séries",
                "questionnaire3.json": "Culture générale 2",
                "questionnaire4.json": "Culture générale 3",
                "questionnaire5.json": "Musique"
            }
            return themes.get(current_file, "Questionnaire")
        
        # Si on utilise les questionnaires de l'index
        if not self.questionnaires_list:
            return "Culture générale"
            
        return self.questionnaires_list[self.current_questionnaire_index].get("theme", "Questionnaire")

def create_questionnaires():
    """Crée 40 fichiers de questionnaires dans un dossier dédié"""
    
    # Création du dossier pour les questionnaires s'il n'existe pas
    questionnaires_dir = "questionnaires"
    if not os.path.exists(questionnaires_dir):
        os.makedirs(questionnaires_dir)
        print(f"Dossier '{questionnaires_dir}' créé avec succès!")
    
    # Liste des thèmes pour les questionnaires
    themes = [
        "Culture générale", "Cinéma et séries", "Musique", "Sport", "Géographie",
        "Histoire", "Sciences", "Littérature", "Technologie", "Gastronomie",
        "Jeux vidéo", "Animaux", "Art", "Mythologie", "Mode", 
        "Astronomie", "Médecine", "Langue française", "Inventions", "Architecture",
        "Bandes dessinées", "Voitures", "Politique", "Religion", "Économie",
        "Célébrités", "Voyages", "Nature", "Océans", "Mathématiques",
        "Intelligence artificielle", "Culture internet", "Photographie", "Danse", "Théâtre",
        "Philosophie", "Psychologie", "Événements actuels", "Traditions", "Records du monde"
    ]
    
    # Questionnaire modèle
    template_questions = []
    for i in range(1, 16):
        template_questions.append({
            "text": f"Question {i}",
            "answer": f"Réponse {i}",
            "points": 10,
            "time_limit": 40
        })
    
    # Génération des 40 questionnaires
    questionnaires_index = []
    for i, theme in enumerate(themes, 1):
        # Créer le modèle de base du questionnaire
        questionnaire = template_questions.copy()
        
        # Personnaliser le questionnaire selon le thème
        for j in range(len(questionnaire)):
            questionnaire[j]["text"] = f"Question {j+1} sur le thème '{theme}'"
        
        # Enregistrer le questionnaire dans un fichier
        file_name = f"questionnaire_{i}.json"
        file_path = os.path.join(questionnaires_dir, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(questionnaire, f, ensure_ascii=False, indent=4)
        
        # Ajouter à l'index
        questionnaires_index.append({
            "id": i,
            "theme": theme,
            "file": file_name
        })
        
        print(f"Questionnaire {i}: {theme} - créé avec succès!")
    
    # Enregistrer l'index
    with open(os.path.join(questionnaires_dir, "index.json"), 'w', encoding='utf-8') as f:
        json.dump(questionnaires_index, f, ensure_ascii=False, indent=4)
    
    print(f"40 questionnaires créés avec succès dans le dossier '{questionnaires_dir}'!")
    
    # Conserver les fichiers originaux à la racine pour compatibilité
    shutil.copy(os.path.join(questionnaires_dir, "questionnaire_1.json"), "questionnaire1.json")
    shutil.copy(os.path.join(questionnaires_dir, "questionnaire_2.json"), "questionnaire2.json")
    
    print("Fichiers originaux copiés à la racine pour compatibilité.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "create_structure":
        create_questionnaires()
    elif len(sys.argv) > 1 and sys.argv[1] == "gui":
        # Mode interface graphique avec connexion TikTok Live
        logger.info("Mode interface graphique avec connexion TikTok activé")
        
        # Récupérer le numéro de question de départ si spécifié
        start_question = 1
        if len(sys.argv) > 2:
            try:
                start_question = int(sys.argv[2])
                logger.info(f"Démarrage du quiz à partir de la question {start_question}")
            except ValueError:
                logger.warning(f"Numéro de question invalide: {sys.argv[2]}, démarrage à la question 1")
        
        # Initialiser l'interface graphique
        root = tk.Tk()
        quiz_gui = TikTokQuizGUI(root, TIKTOK_USERNAME, start_question=start_question)
        quiz_gui.start()
    else:
        # Mode normal: connexion au live TikTok
        logger.info(f"Démarrage du quiz avec l'utilisateur {TIKTOK_USERNAME}")
        quiz = TikTokQuiz(TIKTOK_USERNAME, DEFAULT_QUESTIONNAIRE)
        quiz.run()