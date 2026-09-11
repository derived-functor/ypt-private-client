from ypt_python._http import HTTPClient
from ypt_python._models import CategoryRank, CategoryRankList


class RanksNamespace:
    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    async def my_rank(self, category_id: int, country_id: int) -> int | None:
        data = await self._http.get(
            "/logs/my-category-rank",
            params={"category_id": category_id, "country_id": country_id},
        )
        return CategoryRank.from_raw(data).rank

    async def category_members(
        self,
        category_id: int,
        country_id: int,
        date: str,
        page: int = 1,
        type_: str = "day",
    ) -> CategoryRankList:
        data = await self._http.get(
            "/logs/category/member/ranks",
            params={
                "date": date,
                "categoryID": category_id,
                "countryID": country_id,
                "page": page,
                "type": type_,
            },
        )
        return CategoryRankList.from_raw(data)
