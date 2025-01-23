import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".deepseek"
        self.config_file = self.config_dir / "config.json"
        self._ensure_config_exists()

    def _ensure_config_exists(self):
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.config_file.write_text('{"api_key": ""}')

    def save_api_key(self, api_key: str):
        config = {"api_key": api_key}
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

    def load_api_key(self) -> str:
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        return config.get('api_key', '')