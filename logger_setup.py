"""
Configuration du système de logging pour le Quiz TikTok.
Remplace les print par des logs structurés pour une meilleure traçabilité.
"""

import logging
import os
from datetime import datetime

def setup_logger(name="quiz_tiktok", log_level=logging.INFO, 
                 log_to_file=True, log_dir="logs"):
    """
    Configure et retourne un logger avec le nom spécifié.
    
    Args:
        name (str): Nom du logger
        log_level: Niveau de log (INFO, DEBUG, ERROR...)
        log_to_file (bool): Si True, les logs sont également écrits dans un fichier
        log_dir (str): Répertoire des fichiers de log
        
    Returns:
        logger: Instance de logger configurée
    """
    # Créer le logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Format de date pour les logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Ajout du StreamHandler pour afficher les logs dans la console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Ajout du FileHandler si demandé
    if log_to_file:
        # Créer le répertoire de logs s'il n'existe pas
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Nom du fichier avec date
        log_filename = f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_path = os.path.join(log_dir, log_filename)
        
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

# Logger principal de l'application
logger = setup_logger()

def get_logger(module_name):
    """
    Obtient un logger pour un module spécifique
    
    Args:
        module_name (str): Nom du module
        
    Returns:
        logger: Logger pour le module
    """
    return logging.getLogger(f"quiz_tiktok.{module_name}") 