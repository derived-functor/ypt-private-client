from ypt_python._http import HTTPClient
from ypt_python._models import CategoryRankList, Group, GroupMember


class GroupsNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    async def browse(
        self,
        category_id: int = 0,
        page: int = 1,
        country_id: int | None = None,
        order_type: str = "promotedAt",
        only_available: bool = False,
        only_open: bool = False,
        only_cam: bool = False,
    ) -> list[Group]:
        params: dict[str, object] = {
            "category_id": category_id,
            "order_type": order_type,
            "only_available": str(only_available).lower(),
            "only_open": str(only_open).lower(),
            "only_cam": str(only_cam).lower(),
            "page": page,
            "p": "true",
        }
        if country_id is not None:
            params["country_id"] = country_id
        data = await self._http.get("/group/list-new-2", params=params)
        gs = data.get("gs", [])
        return [Group.from_raw(g) for g in gs] if isinstance(gs, list) else []

    async def my_groups(self) -> list[Group]:
        data = await self._http.get("/group/groups/v2")
        seen: set[int] = set()
        groups: list[Group] = []
        for key in ("gs", "ms", "cs", "ps"):
            arr = data.get(key, [])
            if not isinstance(arr, list):
                continue
            for raw in arr:
                g = Group.from_raw(raw)
                if g.id not in seen:
                    seen.add(g.id)
                    groups.append(g)
        return groups

    async def members(
        self,
        group_id: int,
        country_id: int,
    ) -> list[GroupMember]:
        data = await self._http.get(
            "/logs/group/members/v2",
            params={
                "groupID": group_id,
                "countryID": country_id,
                "isLooking": "true",
                "version": 810046,
            },
        )
        ms = data.get("ms", [])
        return [GroupMember.from_raw(m) for m in ms] if isinstance(ms, list) else []
