import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    dvf_api_url: str = ""
    file_cleanup_minutes: int = 5
    max_file_size_mb: int = 10

    legifrance_client_id: str = os.getenv("LEGIFRANCE_CLIENT_ID")
    legifrance_client_secret: str = os.getenv("LEGIFRANCE_CLIENT_SECRET")
    openai_model : str = "gpt-4.1-mini"

    carte_loyers_api: str = "https://www.data.gouv.fr/api/1/datasets/"
    sheet_id: str = "1EMbc_r7HHA6PoUG2f9SZV7nlAZ3oFhxjum69mr3xkpw"


settings = Settings()
