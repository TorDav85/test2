"""
Fonctions de validation pour le Quiz TikTok.
Sécurise le traitement des données externes.
"""

import os
import json
from logger_setup import logger
from config import MAX_FILE_SIZE_MB

def validate_file_size(file_path, max_size_mb=MAX_FILE_SIZE_MB):
    """
    Vérifie que la taille du fichier ne dépasse pas la limite spécifiée.
    
    Args:
        file_path (str): Chemin du fichier à vérifier
        max_size_mb (float): Taille maximale autorisée en Mo
        
    Returns:
        bool: True si la taille est acceptable, False sinon
        
    Raises:
        ValueError: Si le fichier est trop volumineux
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
        
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        raise ValueError(f"Fichier trop volumineux: {file_size_mb:.2f}MB > {max_size_mb}MB")
    
    return True

def validate_question_format(question_data):
    """
    Vérifie qu'une question contient les champs requis et qu'ils sont valides.
    
    Args:
        question_data (dict): Données de la question à valider
        
    Returns:
        bool: True si le format est valide
        
    Raises:
        ValueError: Si le format est invalide
    """
    # Vérifier les champs obligatoires
    required_fields = ["text", "answer"]
    for field in required_fields:
        if field not in question_data:
            raise ValueError(f"Champ obligatoire manquant: {field}")
    
    # Vérifier le type des champs
    if not isinstance(question_data["text"], str) or not question_data["text"]:
        raise ValueError("Le texte de la question doit être une chaîne non vide")
    
    if not isinstance(question_data["answer"], str) or not question_data["answer"]:
        raise ValueError("La réponse doit être une chaîne non vide")
    
    # Vérifier les champs optionnels
    if "points" in question_data and not isinstance(question_data["points"], int):
        raise ValueError("Le nombre de points doit être un entier")
    
    if "time_limit" in question_data and not isinstance(question_data["time_limit"], int):
        raise ValueError("La limite de temps doit être un entier")
    
    if "revealed_indices" in question_data:
        if not isinstance(question_data["revealed_indices"], list):
            raise ValueError("Les indices révélés doivent être une liste")
        
        for idx in question_data["revealed_indices"]:
            if not isinstance(idx, int):
                raise ValueError("Les indices révélés doivent être des entiers")
    
    return True

def validate_questions_file(file_path):
    """
    Valide le contenu d'un fichier de questions.
    
    Args:
        file_path (str): Chemin vers le fichier de questions
        
    Returns:
        list: Liste des questions validées
        
    Raises:
        ValueError: Si le fichier est invalide
    """
    # Vérifier la taille du fichier
    validate_file_size(file_path)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Format JSON invalide: {str(e)}")
    
    # Vérifier que le contenu est une liste
    if not isinstance(questions_data, list):
        raise ValueError("Le fichier de questions doit contenir une liste")
    
    # Vérifier chaque question
    for i, question in enumerate(questions_data):
        try:
            validate_question_format(question)
        except ValueError as e:
            raise ValueError(f"Question {i+1} invalide: {str(e)}")
    
    return questions_data

def sanitize_input(text, max_length=MAX_FILE_SIZE_MB):
    """
    Nettoie une entrée utilisateur pour éviter les injections.
    
    Args:
        text (str): Texte à nettoyer
        max_length (int): Longueur maximale autorisée
        
    Returns:
        str: Texte nettoyé
    """
    if not isinstance(text, str):
        return ""
    
    # Supprimer les caractères non imprimables
    cleaned = ''.join(c for c in text if c.isprintable())
    
    # Tronquer si trop long
    return cleaned[:max_length] 