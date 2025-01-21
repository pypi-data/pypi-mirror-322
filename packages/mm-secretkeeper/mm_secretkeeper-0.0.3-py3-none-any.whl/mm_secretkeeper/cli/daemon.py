import os

import daemon
import typer
from daemon.pidfile import TimeoutPIDLockFile

from mm_secretkeeper.config import Config
from mm_secretkeeper.web import run_http_server


def start(config: Config) -> None:
    typer.echo("Starting the sk daemon...")
    pid_file = config.base_dir / "process.pid"
    stdout_file = config.base_dir / "stdout.log"
    stderr_file = config.base_dir / "stderr.log"
    with daemon.DaemonContext(
        working_directory="/",
        pidfile=TimeoutPIDLockFile(pid_file),
        stdout=stdout_file.open("w+"),
        stderr=stderr_file.open("w+"),
    ):
        run_http_server(config.web_port)


def stop(config: Config) -> None:
    """Stop the daemon process."""
    pid_file = config.base_dir / "process.pid"
    if pid_file.exists():
        pid = int(pid_file.read_text())
        try:
            os.kill(pid, 15)  # Send SIGTERM signal
            typer.echo(f"Daemon process (PID {pid}) terminated.")
        except ProcessLookupError:
            typer.echo("Process not found.")
        pid_file.unlink()  # Remove the PID file
    else:
        typer.echo("Daemon is not running (PID file not found).")
