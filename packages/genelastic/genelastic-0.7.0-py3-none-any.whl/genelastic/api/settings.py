from environs import Env

env = Env()
env.read_env()


class Config:
    """Flask config class."""

    # Charger toutes les variables d'environnement nécessaires
    GENAPI_ES_URL = env.url("GENAPI_ES_URL").geturl()
    GENAPI_ES_ENCODED_API_KEY = env.str("GENAPI_ES_ENCODED_API_KEY")
    GENAPI_ES_INDEX_PREFIX = env.str("GENAPI_ES_INDEX_PREFIX")
    GENAPI_ES_CERT_FP = env.str("GENAPI_ES_CERT_FP")
