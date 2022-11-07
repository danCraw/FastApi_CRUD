from typing import Type

import sqlalchemy

from app.db.repositories.base import BaseRepository
from app.db.tables.employees import Employee
from app.models.employee import EmployeeIn, EmployeeOut


class EmployeeRepository(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return Employee

    @property
    def _schema_out(self) -> Type[EmployeeOut]:
        return EmployeeOut

    @property
    def _schema_in(self) -> Type[EmployeeIn]:
        return EmployeeIn
