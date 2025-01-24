import os
from dataclasses import dataclass
from pathlib import Path
from typing import Self
import yaml

DEFAULTS = {
    "cors_origins": ["*"],
    "secret_key": "SoMeThInG_-sUp3Rs3kREt!!",
    "algorithm": "HS256",
    "access_token_expire_days": 5,
    "user_db_path": f"{os.path.dirname(__file__)}/users.sqlite3",
    "login_url": "login",
    "token_refresh_url": "refresh_token",
}


@dataclass
class Settings:
    cors_origins: list[str]
    secret_key: str
    algorithm: str
    access_token_expire_days: int
    user_db_path: str
    login_url: str
    token_refresh_url: str

    @classmethod
    def load_settings(cls, **kwargs) -> Self:

        return cls(**{**DEFAULTS, **kwargs})


settings_path = os.getenv("SETTINGS_PATH", "auth.yaml")
print(settings_path)
settings_path = Path(settings_path).resolve()
if settings_path.exists():
    print("Loading settings from", settings_path)
    with open(settings_path) as f:
        settings = Settings.load_settings(**yaml.safe_load(f))
else:
    print("No settings file found, using defaults")
    settings = Settings.load_settings()