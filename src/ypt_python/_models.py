from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel


def _get(data: dict, *keys: str, default: object = None) -> object:
    for key in keys:
        if key in data and data[key] is not None:
            return data[key]
    return default


class Subject(BaseModel):
    id: int
    title: str
    study_ms: int
    order: int = 0
    color: int = 0
    archived: bool = False

    @property
    def study_hours(self) -> float:
        return self.study_ms / 3_600_000

    @classmethod
    def from_raw(cls, data: dict) -> Subject:
        return cls(
            id=int(_get(data, "id", "sid", "subjectId", "subjectID", "si", default=0)),
            title=str(_get(data, "tt", "t", "title", "subject", "subjectName", "subjectTitle", default="")),
            study_ms=int(_get(data, "sm", "studyMs", "studyMS", "studyTime", "todayStudyMs",
                              "todayStudyMS", "todayStudyTime", "todayMs", "totalStudyMs", "ms", default=0)),
            order=int(_get(data, "or", default=0)),
            color=int(_get(data, "co", "c", default=0)),
            archived=bool(_get(data, "dl", default=False)),
        )


class SubjectLogEntry(BaseModel):
    subject_id: int = 0
    subject_title: str = ""
    study_ms: int = 0
    subject_book_index: int | None = None

    @property
    def study_hours(self) -> float:
        return self.study_ms / 3_600_000

    @classmethod
    def from_raw(cls, data: dict, sbs: list[dict] | None = None) -> SubjectLogEntry:
        subject_id = int(_get(data, "si", "sid", "subjectId", "subjectID", "id", default=0))
        subject_title = str(_get(data, "subject", "subjectName", "title", "tt", "t", default=""))
        study_ms = int(_get(data, "sm", "studyMs", "sd", "ms", "durationMs", default=0))
        sbi = _get(data, "sbi", "subjectIndex", "subjectBookIndex")

        if subject_title == "" and sbi is not None and sbs is not None:
            idx = int(sbi)
            if 0 <= idx < len(sbs):
                subject_title = str(_get(sbs[idx], "t", "title", "subject", "subjectName", default=""))

        return cls(
            subject_id=subject_id,
            subject_title=subject_title,
            study_ms=study_ms,
            subject_book_index=int(sbi) if sbi is not None else None,
        )


class DayLog(BaseModel):
    study_ms: int = 0
    rest_ms: int = 0
    max_study_ms: int = 0
    added_ms: int = 0
    date: str = ""
    subjects: list[SubjectLogEntry] = []

    @property
    def study_hours(self) -> float:
        return self.study_ms / 3_600_000

    @property
    def rest_hours(self) -> float:
        return self.rest_ms / 3_600_000

    @classmethod
    def from_raw(cls, data: dict) -> DayLog:
        sbs = data.get("sbs")
        entries_raw = _get(data, "ls", "ss", default=[])
        subjects = [SubjectLogEntry.from_raw(e, sbs) for e in entries_raw] if isinstance(entries_raw, list) else []
        return cls(
            study_ms=int(_get(data, "sm", default=0)),
            rest_ms=int(_get(data, "rm", default=0)),
            max_study_ms=int(_get(data, "mm", default=0)),
            added_ms=int(_get(data, "ad", default=0)),
            date=str(_get(data, "dt", default="")),
            subjects=subjects,
        )


class Group(BaseModel):
    id: int
    title: str = ""
    category: str = ""
    owner: str = ""
    slogan: str = ""
    member_count: int = 0

    @classmethod
    def from_raw(cls, data: dict) -> Group:
        return cls(
            id=int(_get(data, "id", "gd", default=0)),
            title=str(_get(data, "t", default="")),
            category=str(_get(data, "c", default="")),
            owner=str(_get(data, "on", default="")),
            slogan=str(_get(data, "sn", default="")),
            member_count=int(_get(data, "mc", default=0)),
        )


class RankMember(BaseModel):
    nickname: str = ""
    user_id: int = 0
    study_ms: int = 0
    studicon_id: int = 0

    @property
    def study_hours(self) -> float:
        return self.study_ms / 3_600_000

    @classmethod
    def from_raw(cls, data: dict) -> RankMember:
        dl = data.get("dl", {})
        return cls(
            nickname=str(_get(data, "n", default="")),
            user_id=int(_get(data, "ud", default=0)),
            study_ms=int(_get(dl, "sm", default=_get(data, "sd", default=0))),
            studicon_id=int(_get(data, "si", default=0)),
        )


class GroupMember(BaseModel):
    user_id: int = 0
    nickname: str = ""
    category: str = ""
    study_ms: int = 0
    studying: bool = False

    @property
    def study_hours(self) -> float:
        return self.study_ms / 3_600_000

    @classmethod
    def from_raw(cls, data: dict) -> GroupMember:
        dl = data.get("dl", {})
        return cls(
            user_id=int(_get(data, "ud", default=0)),
            nickname=str(_get(data, "n", default="")),
            category=str(_get(data, "ct", default="")),
            study_ms=int(_get(dl, "sm", default=0)),
            studying=bool(_get(data, "im", default=False)),
        )


class LoginResponse(BaseModel):
    jwt: str = ""
    nickname: str = ""
    email: str | None = None
    category_code: str = ""
    category_id: int = 0
    country_id: int = 0
    subjects: list[Subject] = []
    day_log: DayLog | None = None

    _ATTR_MAP: ClassVar[dict[str, str]] = {}

    @classmethod
    def from_raw(cls, data: dict) -> LoginResponse:
        ss = data.get("ss", [])
        subjects = [Subject.from_raw(s) for s in ss] if isinstance(ss, list) else []
        dl_raw = data.get("dl")
        return cls(
            jwt=str(_get(data, "jwt", default="")),
            nickname=str(_get(data, "n", default="")),
            email=data.get("e"),
            category_code=str(_get(data, "ct", default="")),
            category_id=int(_get(data, "ci", default=0)),
            country_id=int(_get(data, "coid", default=0)),
            subjects=subjects,
            day_log=DayLog.from_raw(dl_raw) if isinstance(dl_raw, dict) else None,
        )


class CategoryRank(BaseModel):
    rank: int | None = None

    @classmethod
    def from_raw(cls, data: dict) -> CategoryRank:
        mr = data.get("mr")
        return cls(rank=int(mr) if mr is not None else None)


class CategoryRankList(BaseModel):
    members: list[RankMember] = []
    total_count: int = 0

    @classmethod
    def from_raw(cls, data: dict) -> CategoryRankList:
        ms = data.get("ms", [])
        return cls(
            members=[RankMember.from_raw(m) for m in ms] if isinstance(ms, list) else [],
            total_count=int(_get(data, "tc", default=0)),
        )
