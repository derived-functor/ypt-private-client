from __future__ import annotations

from pathlib import Path

from ypt_python._http import HTTPClient
from ypt_python._token_cache import TokenCache
from ypt_python.auth import AuthNamespace
from ypt_python.groups import GroupsNamespace
from ypt_python.logs import LogsNamespace
from ypt_python.ranks import RanksNamespace
from ypt_python.study import StudyNamespace


class YPTClient:
    def __init__(
        self,
        token: str | None = None,
        cache_token: bool = False,
        token_cache_path: Path | str | None = None,
    ) -> None:
        self._cache: TokenCache | None = TokenCache(token_cache_path) if cache_token else None
        if token is None and self._cache is not None:
            token = self._cache.load()
        self._http = HTTPClient(token)
        self.auth = AuthNamespace(self._http, self._cache)
        self.study = StudyNamespace(self._http)
        self.groups = GroupsNamespace(self._http)
        self.ranks = RanksNamespace(self._http)
        self.logs = LogsNamespace(self._http)

    @property
    def token(self) -> str | None:
        return self._http.token

    @token.setter
    def token(self, value: str) -> None:
        self._http.token = value
        if self._cache is not None:
            self._cache.save(value)

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self) -> YPTClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
