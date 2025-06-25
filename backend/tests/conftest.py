import pytest
import asyncio
import logging
import os
import sys
from pathlib import Path

# Ajouter le path backend/app pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture(scope="session")
def event_loop():
    """Fixture pour gérer l'event loop asyncio"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def test_logger():
    """Logger pour les tests"""
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.DEBUG)
    
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger

@pytest.fixture
def mock_config():
    """Configuration mock pour les tests"""
    return {
        'google_sheet_url': 'https://test-url',
        'api_timeout': 30
    }