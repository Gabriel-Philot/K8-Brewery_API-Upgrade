
from pathlib import Path
import yaml
import os
from typing import Dict, Any
import logging

def get_environment() -> str:
    """
    Get current environment or return default environment
    
    Args:
        default_env: Environment to use if APP_ENV is not set
    """

    default_env = "development"

    return os.getenv("APP_ENV", default_env)


def load_config() -> Dict[str, Any]:
    """
    Load config from *config.yaml for the current environment
    
    Args:
        default_env: Environment to use if APP_ENV is not set
    """
    current_dir = Path(__file__).resolve().parent
    config_dir = current_dir.parent / "config"
    config_files = list(config_dir.glob("*config.yaml"))
    
    if not config_files:
        raise Exception("No *config.yaml file found in config directory")
    
    config_path = config_files[0]
    
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
            environment = get_environment()
            return config[environment]
    except Exception as e:
        raise Exception(f"Failed to load config from {config_path.name}: {str(e)}")



import logging
def log_header(message: str):
    logging.info('*' * 60)
    logging.info('*' + ' ' * 58 + '*')
    logging.info('*' + ('>>> ' + message + ' <<<').center(58) + '*')
    logging.info('*' + ' ' * 58 + '*')
    logging.info('*' * 60)




