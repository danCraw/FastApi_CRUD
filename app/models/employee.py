from typing import Optional
from uuid import UUID

from pydantic import validator

from app.core import config
from app.models.base import BaseSchema


class EmployeeBase(BaseSchema):
    name: str
    surname: str
    department: str
    position: str

    @validator("department")
    def department_is_exist(cls, v):
        if v not in config.DEPARTMENTS:
            raise ValueError('Department does not exist. Allowed positions:' + str(*config.DEPARTMENTS))
        return v

    @validator("position")
    def position_is_exist(cls, v):
        if v not in config.POSITIONS:
            raise ValueError('Position does not exist. Allowed positions:' + str(*config.POSITIONS))
        return v


class EmployeeIn(EmployeeBase):
    id: Optional[str]


class EmployeeOut(EmployeeBase):
    id: UUID
