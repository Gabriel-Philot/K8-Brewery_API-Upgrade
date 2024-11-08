
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
    current_dir = Path(__file__).resolve().parent.parent
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
def print_header(message: str):
    print('*' * 60)
    print('*' + ' ' * 58 + '*')
    print('*' + ('>>> ' + message + ' <<<').center(58) + '*')
    print('*' + ' ' * 58 + '*')
    print('*' * 60)

from IPython.display import display


def display_result(result):
    display(result)


##############################################################################################





# def load_config() -> Dict:
#     """Load configuration from YAML file"""
#     config_path = Path("/usr/local/airflow/dags/crypto/configs/crypto_config.yaml")
#     try:
#         with open(config_path) as f:
#             config = yaml.safe_load(f)
#             environment = os.getenv('AIRFLOW_ENV', 'development')
#             return config[environment]
#     except Exception as e:
#         raise Exception(f"Failed to load config: {str(e)}")


# def validate_prices(data: Dict, config: Dict) -> None:
#     """Validate price data structure and values"""
#     required_coins = set(config['validation']['required_coins'])
#     if not all(coin in data for coin in required_coins):
#         raise DataValidationError(f"Missing required coins. Expected: {required_coins}")

#     min_price = config['validation']['min_price']
#     for coin, details in data.items():
#         if 'usd' not in details:
#             raise DataValidationError(f"Missing USD price for {coin}")
#         if details['usd'] <= min_price:
#             raise DataValidationError(f"Invalid price for {coin}: {details['usd']}")