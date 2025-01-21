from typing import Annotated

import uvicorn
from fastapi import FastAPI, Form
from fastapi.params import Depends
from pydantic import BaseModel

from mm_secretkeeper.keeper import Health, Keeper, KeeperResult, KeyResult, KeysResult, get_keeper

app = FastAPI(docs_url="/")

KeeperDepends = Annotated[Keeper, Depends(get_keeper)]


@app.get("/health")
def check_handler(keeper: KeeperDepends) -> Health:
    """Check the health of the database"""
    return keeper.health()


@app.post("/init")
def init_handler(keeper: KeeperDepends, password: Annotated[str, Form()]) -> KeeperResult:
    """Initialize the database"""
    return keeper.init_db(password)


@app.post("/password")
def password_handler(
    keeper: KeeperDepends, old_password: Annotated[str, Form()], new_password: Annotated[str, Form()]
) -> KeeperResult:
    """Update the password"""
    return keeper.update_password(old_password, new_password)


@app.post("/lock")
def lock_handler(keeper: KeeperDepends) -> Health:
    """Lock the database"""
    return keeper.lock()


@app.post("/unlock")
def unlock_handler(keeper: KeeperDepends, password: Annotated[str, Form()]) -> Health:
    """Unlock the database"""
    return keeper.unlock(password)


@app.get("/list")
def list_handler(keeper: KeeperDepends) -> KeysResult:
    """List all keys"""
    return keeper.get_keys()


class NewSecret(BaseModel):
    key: str
    value: str


@app.post("/add")
def add_handler(keeper: KeeperDepends, secret: NewSecret) -> KeeperResult:
    """Add a new secret"""
    return keeper.add(secret.key, secret.value)


@app.post("/get")
def get_handler(keeper: KeeperDepends, key: Annotated[str, Form()]) -> KeyResult:
    """Get a secret by key"""
    return keeper.get_key(key)


@app.post("/delete")
def delete_handler(keeper: KeeperDepends, key: Annotated[str, Form()]) -> KeeperResult:
    """Delete a secret by key"""
    return keeper.delete(key)


def run_http_server(port: int) -> None:
    uvicorn.run(app, host="localhost", port=port)
