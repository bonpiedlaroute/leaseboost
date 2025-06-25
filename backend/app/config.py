import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    dvf_api_url: str = ""
    file_cleanup_minutes: int = 5
    max_file_size_mb: int = 10

    carte_loyers_api: str = "https://www.data.gouv.fr/api/1/datasets/"


settings = Settings()
