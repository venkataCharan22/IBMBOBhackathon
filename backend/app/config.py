"""
Configuration management using pydantic-settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = "Bug2PR"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # Database
    database_url: str = "sqlite:///./bug2pr.db"
    
    # GitHub
    github_token: Optional[str] = None
    github_repo_owner: Optional[str] = None
    github_repo_name: Optional[str] = None
    
    # AI Models - Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"
    
    # AI Models - Google Gemini
    google_api_key: Optional[str] = None
    google_model: str = "gemini-pro"
    
    # AI Models - Groq
    groq_api_key: Optional[str] = None
    groq_model: str = "mixtral-8x7b-32768"
    
    # Vector Store
    chromadb_path: str = "./chromadb"
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # Agent Configuration
    max_iterations: int = 10
    agent_timeout: int = 300
    
    # Logging
    log_level: str = "INFO"
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins string into list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()

# Made with Bob
