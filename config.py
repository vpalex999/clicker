""" Хранит конфигурацию объектов и команд выполнения."""
from typing import Any, Dict, Optional
import yaml


class Config:
    def __init__(self, data: Optional[Dict[str, Any]] = None) -> None:
        self.data = data

    @classmethod
    def from_file(cls, filename: str):
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
            return cls(data)

    @property
    def login(self) -> Optional[str]:
        if self.data:
            try:
                return self.data["login"]
            except KeyError:
                print("The login attribute is not found in config-file")

        return None

    @property
    def password(self) -> Optional[str]:
        if self.data:
            try:
                return self.data["password"]
            except KeyError:
                print("The 'password' attribute is not found in config-file")

        return None

    def __str__(self) -> str:
        return str(self.data)
