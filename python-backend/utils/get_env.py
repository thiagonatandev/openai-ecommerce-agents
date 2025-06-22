from dotenv import load_dotenv
import os
from pathlib import Path

# Caminho para o .env que está na raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

def load_config():
    return {
        "POSTGRES_USER": os.getenv("POSTGRES_USER"),
        "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "POSTGRES_DB": os.getenv("POSTGRES_DB"),
        "POSTGRES_PORT": os.getenv("POSTGRES_PORT"),
        "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
        "REDIS_HOST": os.getenv("REDIS_HOST"),
        "REDIS_PORT": os.getenv("REDIS_PORT")
    }
