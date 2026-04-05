from __future__ import annotations

from collections.abc import Iterable
from copy import deepcopy
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

from app.core.config import settings
from app.services.seed_data import DEMO_STATE


class InMemoryCollection:
    def __init__(self, initial: list[dict[str, Any]] | None = None) -> None:
        self._items = initial or []

    async def find_all(self) -> list[dict[str, Any]]:
        return deepcopy(self._items)

    async def find_one(self, predicate: dict[str, Any]) -> dict[str, Any] | None:
        for item in self._items:
            if all(_matches(item.get(key), value) for key, value in predicate.items()):
                return deepcopy(item)
        return None

    async def replace_one(self, predicate: dict[str, Any], value: dict[str, Any]) -> None:
        for index, item in enumerate(self._items):
            if all(_matches(item.get(key), expected) for key, expected in predicate.items()):
                self._items[index] = deepcopy(value)
                return
        self._items.append(deepcopy(value))

    async def insert_many(self, items: Iterable[dict[str, Any]]) -> None:
        for item in items:
            self._items.append(deepcopy(item))

    async def delete_many(self, predicate: dict[str, Any]) -> None:
        self._items = [
            item for item in self._items if not all(_matches(item.get(key), value) for key, value in predicate.items())
        ]


class MongoCollection:
    def __init__(self, collection) -> None:
        self._collection = collection

    async def find_all(self) -> list[dict[str, Any]]:
        return await self._collection.find({}, {"_id": 0}).to_list(length=None)

    async def find_one(self, predicate: dict[str, Any]) -> dict[str, Any] | None:
        return await self._collection.find_one(predicate, {"_id": 0})

    async def replace_one(self, predicate: dict[str, Any], value: dict[str, Any]) -> None:
        await self._collection.replace_one(predicate, value, upsert=True)

    async def insert_many(self, items: Iterable[dict[str, Any]]) -> None:
        item_list = list(items)
        if not item_list:
            return
        await self._collection.insert_many(item_list)

    async def delete_many(self, predicate: dict[str, Any]) -> None:
        await self._collection.delete_many(predicate)


def _matches(current: Any, expected: Any) -> bool:
    if isinstance(current, list) and not isinstance(expected, list):
        return expected in current
    return current == expected


class Database:
    def __init__(self) -> None:
        self.client = None
        self.db = None
        self.collections = {
            name: InMemoryCollection(initial=deepcopy(values))
            for name, values in DEMO_STATE.items()
        }

        if not settings.use_in_memory_store:
            self.client = AsyncIOMotorClient(settings.mongodb_uri)
            self.db = self.client[settings.mongodb_db_name]

    def collection(self, name: str) -> InMemoryCollection | MongoCollection:
        if self.db is not None:
            return MongoCollection(self.db[name])
        return self.collections[name]

    async def ensure_seed_data(self) -> None:
        if self.db is None:
            return

        for name, values in DEMO_STATE.items():
            collection = self.db[name]
            if not values:
                continue

            operations = []
            for item in values:
                identifier = item.get("id")
                if identifier is not None:
                    operations.append(UpdateOne({"id": identifier}, {"$set": item}, upsert=True))
                    continue

                user_id = item.get("user_id")
                item_date = item.get("date") or item.get("target_date")
                if user_id and item_date:
                    operations.append(
                        UpdateOne(
                            {"user_id": user_id, "date": item_date, "target_date": item.get("target_date")},
                            {"$set": item},
                            upsert=True,
                        )
                    )

            if operations:
                await collection.bulk_write(operations)
            else:
                await collection.insert_many(values)


database = Database()
