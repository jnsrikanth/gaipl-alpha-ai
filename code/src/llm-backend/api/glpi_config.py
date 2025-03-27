import os
from dotenv import load_dotenv
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class GLPIConfig:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv('GLPI_URL')
        self.app_token = os.getenv('GLPI_APP_TOKEN')
        self.user_token = os.getenv('GLPI_USER_TOKEN')
        self._validate_config()

    def _validate_config(self):
        if not self.url:
            logger.error("GLPI_URL environment variable not set")
            raise ValueError("GLPI_URL environment variable not set")
        if not self.app_token:
            logger.error("GLPI_APP_TOKEN environment variable not set")
            raise ValueError("GLPI_APP_TOKEN environment variable not set")
        if not self.user_token:
            logger.error("GLPI_USER_TOKEN environment variable not set")
            raise ValueError("GLPI_USER_TOKEN environment variable not set")
        
        logger.info(f"GLPI Configuration loaded. URL: {self.url}")

    def get_config(self) -> Dict[str, str]:
        return {
            'url': self.url,
            'apptoken': self.app_token,
            'usertoken': self.user_token
        }
