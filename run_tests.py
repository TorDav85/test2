#!/usr/bin/env python
"""
Script pour exécuter tous les tests du projet Quiz TikTok
"""

import unittest
import sys

if __name__ == "__main__":
    # Découvrir et exécuter tous les tests dans le dossier tests/
    test_suite = unittest.defaultTestLoader.discover('tests')
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Sortir avec un code d'erreur si des tests ont échoué
    sys.exit(not result.wasSuccessful()) 