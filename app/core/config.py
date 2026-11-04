from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Reads values from environment variables, or from a local .env file.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str

    # LLM (local Ollama). Defaults work without touching .env.
    llm_model: str = "llama3.2"
    ollama_base_url: str = "http://localhost:11434"
    llm_timeout_seconds: float = 60
    llm_max_attempts: int = 2


settings = Settings()
