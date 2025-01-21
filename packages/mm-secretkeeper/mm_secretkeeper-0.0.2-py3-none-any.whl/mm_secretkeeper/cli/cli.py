import getpass
from typing import Annotated

import pyperclip
import typer
from mm_std import hr, print_json, print_plain

from mm_secretkeeper.cli import daemon
from mm_secretkeeper.config import get_config
from mm_secretkeeper.web import run_http_server

BASE_URL = f"http://localhost:{get_config().web_port}"

app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False, add_completion=False)


@app.command(name="start")
def start_command(daemonize: Annotated[bool, typer.Option("-d")] = True) -> None:
    config = get_config()
    if daemonize:
        daemon.start(config)
    else:
        run_http_server(config.web_port)


@app.command("stop")
def stop_command() -> None:
    config = get_config()
    daemon.stop(config)


@app.command(name="lock")
def lock_command() -> None:
    res = hr(f"{BASE_URL}/lock", method="POST")
    print_json(res.json)


@app.command(name="unlock")
def unlock_command() -> None:
    password = getpass.getpass()
    res = hr(f"{BASE_URL}/unlock", method="POST", params={"password": password}, json_params=False)
    print_json(res.json)


@app.command(name="health")
def health_command() -> None:
    res = hr(f"{BASE_URL}/health")
    print_json(res.json)


@app.command(name="list")
def list_command() -> None:
    res = hr(f"{BASE_URL}/list")
    if res.json and res.json.get("keys") and not res.json.get("error"):
        for k in res.json["keys"]:
            print_plain(k)
    else:
        print_json(res)


@app.command(name="get")
def get_command() -> None:
    key = input("key: ")
    res = hr(f"{BASE_URL}/get", method="POST", params={"key": key}, json_params=False)
    if res.json.get("value"):
        value = res.json.get("value")
        print_plain(value)
        pyperclip.copy(value)
    else:
        print_json(res.json)


@app.command(name="add")
def add_command() -> None:
    key = input("key: ")
    value = getpass.getpass("value")
    res = hr(f"{BASE_URL}/add", method="POST", params={"key": key, "value": value})
    print_json(res.json)


@app.command(name="delete")
def delete_command() -> None:
    key = input("key: ")
    res = hr(f"{BASE_URL}/delete", method="POST", params={"key": key}, json_params=False)
    print_json(res.json)


if __name__ == "__main__":
    app()
