from sqlalchemy import Column, String, Table
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import metadata

Employee = Table(
                'employees',
                metadata,
                Column("id", UUID(), primary_key=True),
                Column("name", String(65), nullable=False),
                Column("surname", String(65), nullable=False),
                Column("position", String(65), nullable=False),
                Column("department", String(65), nullable=False),
                )
