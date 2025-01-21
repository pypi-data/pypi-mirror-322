from pathlib import Path

import sqlcipher3
from pydantic import BaseModel

from mm_secretkeeper.config import get_config


class Health(BaseModel):
    db_path: str
    db_path_exists: bool
    unlocked: bool = False
    secrets: int | None = None
    error: str | None = None


class KeeperResult(BaseModel):
    success: bool = False
    error: str | None = None


class KeysResult(BaseModel):
    keys: list[str] | None = None
    error: str | None = None


class KeyResult(BaseModel):
    value: str | None = None
    error: str | None = None


class Keeper:
    db_path: Path
    password: str | None = None

    def __init__(self, base_dir: Path) -> None:
        self.db_path = base_dir / "data.db"

    def health(self) -> Health:
        secrets, error = None, None
        if self.password:
            try:
                conn = self._connection()
                cursor = conn.execute("SELECT COUNT(*) FROM secrets;")
                secrets = cursor.fetchone()[0]
                conn.close()
            except Exception as e:
                error = str(e)
        return Health(
            db_path=str(self.db_path),
            db_path_exists=Path(self.db_path).is_file(),
            unlocked=bool(self.password),
            secrets=secrets,
            error=error,
        )

    def init_db(self, password: str) -> KeeperResult:
        if self.db_path.exists():
            return KeeperResult(error="Database already exists")

        try:
            conn = self._connection(password)
            conn.execute("CREATE TABLE IF NOT EXISTS secrets (key TEXT PRIMARY KEY, value TEXT);")
            conn.commit()
            conn.close()
            return KeeperResult(success=True)
        except Exception as e:
            return KeeperResult(error=str(e))

    def update_password(self, old_password: str, new_password: str) -> KeeperResult:
        try:
            conn = self._connection(old_password)
            conn.execute(f"PRAGMA rekey = '{new_password}';")
            conn.close()
            return KeeperResult(success=True)
        except Exception as e:
            return KeeperResult(error=str(e))

    def lock(self) -> Health:
        self.password = None
        return self.health()

    def unlock(self, password: str) -> Health:
        try:
            conn = self._connection(password)
            cursor = conn.execute("SELECT COUNT(*) FROM secrets;")
            _secrets_count = cursor.fetchone()[0]
            conn.close()
            self.password = password
            return self.health()
        except Exception:
            return self.health()

    def add(self, key: str, value: str) -> KeeperResult:
        try:
            conn = self._connection()
            conn.execute("INSERT INTO secrets (key, value) VALUES (?, ?);", (key.lower(), value))
            conn.commit()
            conn.close()
            return KeeperResult(success=True)
        except Exception as e:
            return KeeperResult(error=str(e))

    def delete(self, key: str) -> KeeperResult:
        try:
            conn = self._connection()
            conn.execute("DELETE FROM secrets WHERE key = ?;", (key.lower(),))
            conn.commit()
            conn.close()
            return KeeperResult(success=True)
        except Exception as e:
            return KeeperResult(error=str(e))

    def get_keys(self) -> KeysResult:
        try:
            conn = self._connection()
            cursor = conn.execute("SELECT key FROM secrets ORDER BY key;")
            keys = [row[0] for row in cursor]
            conn.close()
            return KeysResult(keys=keys)
        except Exception as e:
            return KeysResult(error=str(e))

    def get_key(self, key: str) -> KeyResult:
        try:
            conn = self._connection()
            cursor = conn.execute("SELECT value FROM secrets WHERE key = ?;", (key.lower(),))
            row = cursor.fetchone()
            conn.close()
            if row:
                return KeyResult(value=row[0])
            return KeyResult(error="Key not found")
        except Exception as e:
            return KeyResult(error=str(e))

    def _connection(self, password: str | None = None) -> sqlcipher3.Connection:
        conn = sqlcipher3.connect(str(self.db_path))
        password = password or self.password
        if not password:
            raise ValueError("Password is not set")
        conn.execute(f"PRAGMA key = '{password}';")
        return conn


_keeper = Keeper(get_config().base_dir)


def get_keeper() -> Keeper:
    return _keeper
