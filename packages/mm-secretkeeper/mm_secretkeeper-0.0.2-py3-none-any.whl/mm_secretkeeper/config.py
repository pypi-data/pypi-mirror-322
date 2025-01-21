from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel


class Config(BaseModel):
    base_dir: Path
    web_port: int
    daemon_pid: Path
    daemon_stdout: Path
    daemon_stderr: Path

    @staticmethod
    def init() -> Config:
        base_dir = Path("~/.local/mm-secretkeeper").expanduser()
        base_dir.mkdir(parents=True, exist_ok=True)

        if not base_dir.exists():
            base_dir.mkdir(parents=True)
        web_port = 18001

        daemon_pid = base_dir / "process.pid"
        daemon_stdout = base_dir / "stdout.log"
        daemon_stderr = base_dir / "stderr.log"

        return Config(
            base_dir=base_dir,
            web_port=web_port,
            daemon_pid=daemon_pid,
            daemon_stdout=daemon_stdout,
            daemon_stderr=daemon_stderr,
        )


_config = Config.init()


def get_config() -> Config:
    return _config
