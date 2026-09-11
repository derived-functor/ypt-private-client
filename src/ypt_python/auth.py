from __future__ import annotations

from typing import TYPE_CHECKING

from ypt_python._http import HTTPClient
from ypt_python._models import LoginResponse

if TYPE_CHECKING:
    from ypt_python._token_cache import TokenCache


class AuthNamespace:
    def __init__(self, http: HTTPClient, cache: TokenCache | None = None) -> None:
        self._http = http
        self._cache = cache

    async def login(
        self,
        email: str,
        password: str,
        language: str = "en",
    ) -> LoginResponse:
        data = await self._http.post(
            "/user/sign-in-jwt",
            json={
                "email": email,
                "password": password,
                "loginProvider": "Email",
                "new": True,
                "getx": True,
                "language": language,
            },
        )
        resp = LoginResponse.from_raw(data)
        if resp.jwt:
            self._http.token = resp.jwt
            if self._cache is not None:
                self._cache.save(resp.jwt)
        return resp

    async def reload_info(self) -> LoginResponse:
        data = await self._http.post(
            "/user/v2/reload/info",
            json={
                "pv": 0,
                "cd": {
                    "su": None,
                    "sbu": None,
                    "cu": None,
                    "eu": None,
                    "du": None,
                    "tu": None,
                },
            },
        )
        return LoginResponse.from_raw(data)