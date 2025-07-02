"""
Configuration centralisée pour le Quiz TikTok Live.
Ce fichier contient toutes les constantes et paramètres configurable de l'application.
"""

import os

# Paramètres TikTok
TIKTOK_USERNAME = "@tiketokefrance"

# Paramètres des fichiers et chemins
SCORES_FILE = "quiz_scores.json"
QUESTIONNAIRES_DIR = "questionnaires"
DEFAULT_QUESTIONNAIRE = "questionnaire1.json"

# Paramètres du quiz
DEFAULT_TIME_LIMIT = 40  # secondes
DEFAULT_POINTS = 10
SCORE_EXPIRATION_HOURS = 24
LEADERBOARD_SIZE = 10  # nombre de joueurs dans le classement

# Paramètres de validation
MAX_FILE_SIZE_MB = 5  # taille maximale du fichier de questions en Mo
MAX_ANSWER_LENGTH = 100  # longueur maximale d'une réponse utilisateur
ANSWER_SIMILARITY_THRESHOLD = 0.8  # seuil de similitude pour les réponses légèrement incorrectes

# Paramètres d'interface (uniquement référence, ne pas modifier ici)
BACKGROUND_COLOR = "#232323"  
TEXT_COLOR = "white"
TIMER_COLOR = "#FF3333"
SUCCESS_COLOR = "green"
WARNING_COLOR = "orange"

# Configuration du TTS (Text-to-Speech)
TTS_ENABLED = True  # Réactivé avec la nouvelle gestion des threads
TTS_VOICE_RATE = 200  # Augmentation de la vitesse (était à 150)
TTS_VOICE_VOLUME = 0.5  # Volume baissé (était à 0.8) 