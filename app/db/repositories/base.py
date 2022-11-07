import abc
import uuid
from typing import Dict, List, Union

import databases
import sqlalchemy
from asyncpg import Record

from app.db.base import database
from app.models.base import BaseIdSchema
from app.models.employee import BaseSchema


class BaseRepository(abc.ABC):
    def __init__(self, db: databases.Database = database, *args, **kwargs) -> None:
        self._db = db
        super()

    @property
    @abc.abstractmethod
    def _table(self) -> sqlalchemy.Table:
        pass

    @property
    @abc.abstractmethod
    def _schema_out(self):
        pass

    @property
    @abc.abstractmethod
    def _schema_in(self):
        pass

    @staticmethod
    def generate_uuid() -> uuid.UUID:
        return uuid.uuid4()

    def _preprocess_create(self, values: Dict) -> Dict:
        if values.get('id', None) is None:
            values["id"] = self.generate_uuid()
        return values

    async def _list(self) -> List[Record]:
        query = self._table.select()
        return await self._db.fetch_all(query=query)

    async def list(self) -> List:
        rows = await self._list()
        return [self._schema_out(**dict(dict(row).items())) for row in rows]

    async def create(self, values: Union[BaseSchema, Dict]) -> _schema_out:
        if isinstance(values, dict):
            values = self._schema_in(**values)
        dict_values = self._preprocess_create(dict(values))

        await self._db.execute(query=self._table.insert(), values=dict_values)
        return self._schema_out(**dict_values)

    async def get(self, id: Union[int, str]) -> _schema_out:
        row = await self._db.fetch_one(query=self._table.select().where(self._table.c.id == id))
        if row:
            return self._schema_out(**dict(dict(row).items()))
        else:
            return row

    async def update(self, values: Union[BaseIdSchema, Dict]) -> _schema_out:
        if isinstance(values, dict):
            values = self._schema_in(**values)
        dict_values = self._preprocess_create(dict(values))
        row = await self.get(dict_values['id'])
        if row:
            await self._db.execute(query=self._table.update().where(self._table.c.id == dict_values['id']),
                                   values=dict_values)
            return self._schema_out(**dict_values)
        return row

    async def delete(self, id: Union[int, str]) -> _schema_out:
        row = await self.get(id)
        if row:
            await self._db.execute(query=self._table.delete().where(self._table.c.id == id))
        return row
