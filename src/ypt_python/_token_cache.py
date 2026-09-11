from __future__ import annotations

import os
from pathlib import Path

_DEFAULT_PATH = Path("~/.cache/ypt-python/token").expanduser()


class TokenCache:
    """Persists the JWT token to disk so re-authentication is not required."""

    def __init__(self, path: Path | str | None = None) -> None:
        self._path = Path(path).expanduser() if path else _DEFAULT_PATH

    @property
    def path(self) -> Path:
        return self._path

    def load(self) -> str | None:
        try:
            token = self._path.read_text(encoding="utf-8").strip()
        except OSError:
            return None
        return token or None

    def save(self, token: str) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(token.strip(), encoding="utf-8")
        try:
            os.chmod(self._path, 0o600)
        except OSError:
            pass

    def clear(self) -> None:
        try:
            self._path.unlink()
        except OSError:
            pass