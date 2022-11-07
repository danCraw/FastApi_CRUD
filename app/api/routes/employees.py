from typing import List

from fastapi import APIRouter, HTTPException

from app.db.repositories.employees import EmployeeRepository
from app.models.employee import EmployeeIn, EmployeeOut

router = APIRouter()


@router.get("/")
async def employees_list() -> List[EmployeeOut]:
    employee_repo: EmployeeRepository = EmployeeRepository()
    employee = await employee_repo.list()
    return employee


@router.get("/{id}")
async def one_employee(employee_id: str) -> EmployeeOut:
    employee_repo: EmployeeRepository = EmployeeRepository()
    employee = await employee_repo.get(employee_id)
    if employee:
        return employee
    else:
        raise HTTPException(status_code=404, detail="Employee with the given Id not found")


@router.post("/")
async def create_employee(employee: EmployeeIn) -> EmployeeOut:
    employee_repo: EmployeeRepository = EmployeeRepository()
    employee = await employee_repo.create(employee)
    return employee


@router.put("/")
async def update_employee(employee: EmployeeIn) -> EmployeeOut:
    employee_repo: EmployeeRepository = EmployeeRepository()
    employee = await employee_repo.update(employee)
    if employee:
        return employee
    else:
        raise HTTPException(status_code=404, detail="Employee with the given Id not found")


@router.delete("/{id}")
async def delete_employee(employee_id: str) -> List[EmployeeOut]:
    employee_repo: EmployeeRepository = EmployeeRepository()
    employee = await employee_repo.delete(employee_id)
    if employee:
        return employee
    else:
        raise HTTPException(status_code=404, detail="Employee with the given Id not found")
