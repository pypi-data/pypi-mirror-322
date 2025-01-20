import logging
from pathlib import Path

import hvac

from .config_loader import load_config

logger = logging.getLogger(__name__)


def get_vault_secrets(BASE_DIR):
    config = load_config(BASE_DIR)
    if not config:
        raise ValueError("Configuration could not be loaded. Ensure the config file exists and is valid.")

    client = hvac.Client(url=config['vault']['host'])

    try:
        auth_response = client.auth.userpass.login(
            username=config['vault']['username'],
            password=config['vault']['password']
        )
        client.token = auth_response['auth']['client_token']
        logger.info("Vault Authentication successful!")
    except Exception as e:
        logger.error(f"Error to authenticate vault: {str(e)}")

    try:
        response = client.secrets.kv.v2.read_secret(
            mount_point=config['vault']['secret_engine'],
            path=config['vault']['application']
        )
        return response['data']['data']
    except Exception as e:
        logger.error(f"Error to fetch secrets: {str(e)}")
