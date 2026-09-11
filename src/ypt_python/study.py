from ypt_python._http import HTTPClient
from ypt_python._models import DayLog


class StudyNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    async def start(
        self,
        subject: str,
        device_model: str,
        task_id: int | None = None,
    ) -> DayLog:
        data = await self._http.post(
            "/study/start",
            json={
                "subject": subject,
                "deviceModel": device_model,
                "taskId": task_id,
            },
        )
        return DayLog.from_raw(data.get("dl", {}))

    async def stop(
        self,
        started_at: int,
        device_model: str,
    ) -> DayLog:
        data = await self._http.post(
            "/study/stop",
            json={
                "startedAt": started_at,
                "deviceModel": device_model,
            },
        )
        return DayLog.from_raw(data.get("dl", {}))
