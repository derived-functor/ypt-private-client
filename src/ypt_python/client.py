from __future__ import annotations

from ypt_python._http import HTTPClient
from ypt_python.auth import AuthNamespace
from ypt_python.groups import GroupsNamespace
from ypt_python.logs import LogsNamespace
from ypt_python.ranks import RanksNamespace
from ypt_python.study import StudyNamespace


class YPTClient:
    def __init__(self, token: str | None = None) -> None:
        self._http = HTTPClient(token)
        self.auth = AuthNamespace(self._http)
        self.study = StudyNamespace(self._http)
        self.groups = GroupsNamespace(self._http)
        self.ranks = RanksNamespace(self._http)
        self.logs = LogsNamespace(self._http)

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self) -> YPTClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
