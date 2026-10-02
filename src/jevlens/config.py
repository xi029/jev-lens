from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="JEVLENS_", env_file=".env", extra="ignore")
    provider: Literal["demo", "ollama", "laya", "jev"] = "demo"
    ollama_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen3.5:4b"
    laya_url: str = "http://127.0.0.1:8123"
    laya_model: str = "english"
    laya_api_key: str = ""
    jev_url: str = "https://api.typesafe.ai"
    jev_model: str = "jev-latest"
    jev_api_key: str = ""
    data_dir: Path = Path("data")
    timeout_seconds: float = 120
    laya_state_chars: int = 1600
    laya_balance_options: bool = True
