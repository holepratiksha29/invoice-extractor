# app/core/config.py

from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    TENANT_ID: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    OUTLOOK_USER: str
    PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()

# app/ directory (parent of core/)
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
DATA_DIR = os.path.join(BASE_DIR, "data")

ATTACHMENTS_DIR = os.path.join(DATA_DIR, "attachments")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
OUTPUT_DIR = os.path.join(DATA_DIR, "output_json")

# Ensure folders exist
for path in [ATTACHMENTS_DIR, IMAGES_DIR, OUTPUT_DIR]:
    os.makedirs(path, exist_ok=True)

