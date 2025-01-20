Hashicorp-vault-python
=========================

Hashicorp vault is a Python-Django app for the improvement application security leveraging secrets

Installation
------------

    * pip install hashicorp-vault-django
    * Add ``hashicorp_vault`` to your ``INSTALLED_APPS``

::

Setup in settings
-----------------

    * make config directory at project root level and create application.yml file inside config directory 
    * application.yml sample for vault configuration
        * vault:
              host: vault url  # https
              secret_engine: mount path  # secrests-config
              application: application path # secrets-ai
              username: username
              password: password
    * if your secrets stored in `/vault/secrets/secrets-config/kv/secrets-ai/` then use secrets-config as secret_engine and secrets-ai as application in vault configuration
    * consume vault secrets in your settings.py file 
          from hashicorp_vault.vault import get_vault_secrets

          vault_secrets = get_vault_secrets(BASE_DIR)

          DATABASES = {
            "default": {
                "ENGINE": config["datasource"]["DATABASE_ENGINE"],
                "NAME": vault_secrets.get("db_database"),
                "USER": vault_secrets.get("db_user"),
                "PASSWORD": vault_secrets.get("db_password"),
                "HOST": vault_secrets.get("host"),
                "PORT": vault_secrets.get("db_port"),
                "OPTIONS": {"charset": "utf8mb4"},
            },
        }
    * Use secret keys to access to secret values from vault
::


Compatibility
-------------
{py3.8, py3.10}-django{4.* above}
