from ypt_python._http import HTTPClient
from ypt_python._models import DayLog


class LogsNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    async def day(self, date: str) -> DayLog:
        data = await self._http.get("/logs/day", params={"date": date})
        return DayLog.from_raw(data.get("dl", {}))
