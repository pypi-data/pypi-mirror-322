from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel


class Config(BaseModel):
    base_dir: Path
    web_port: int

    @staticmethod
    def init() -> Config:
        base_dir = Path("~/.local/mm-secretkeeper").expanduser()
        base_dir.mkdir(parents=True, exist_ok=True)

        if not base_dir.exists():
            base_dir.mkdir(parents=True)
        web_port = 18001

        return Config(base_dir=base_dir, web_port=web_port)


_config = Config.init()


def get_config() -> Config:
    return _config
