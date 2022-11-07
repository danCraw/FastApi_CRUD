import pytest
import requests

from app.models.employee import EmployeeIn


@pytest.fixture()
def employee_data() -> EmployeeIn:
    return EmployeeIn(id='11111111-1111-1111-1111-111111111111', name='name', surname='surname', department='testing',
                      position='senior')


pytestmark = pytest.mark.asyncio
base_url = 'http://0.0.0.0:8000/api/v1/employees'


async def test_create(employee_data: EmployeeIn):
    employee = {
        'id': str(employee_data.id),
        'name': employee_data.name,
        'surname': employee_data.surname,
        'department': employee_data.department,
        'position': employee_data.position
    }
    response = requests.post(base_url + '/', json=employee)
    assert response.status_code == 200
    assert response.json() == employee


async def test_read(employee_data: EmployeeIn):
    response = requests.get(base_url + '/%7Bid%7D?', params={'employee_id': str(employee_data.id)}, )
    assert response.status_code == 200
    assert response.json() == {
        'id': str(employee_data.id),
        'name': employee_data.name,
        'surname': employee_data.surname,
        'department': employee_data.department,
        'position': employee_data.position
    }


async def test_read_wrong_id():
    response = requests.get(base_url + '/%7Bid%7D?', params={'employee_id': '21111111-1111-1111-1111-111111111111'}, )
    assert response.status_code == 404


async def test_update(employee_data: EmployeeIn):
    employee = {
        'id': str(employee_data.id),
        'name': employee_data.name,
        'surname': 'new surname',
        'department': employee_data.department,
        'position': employee_data.position
    }
    response = requests.put(base_url + '/', json=employee)
    assert response.status_code == 200
    assert response.json() == employee


async def test_update_wrong_id(employee_data: EmployeeIn):
    employee = {
        'id': '21111111-1111-1111-1111-111111111111',
        'name': employee_data.name,
        'surname': 'new surname',
        'department': employee_data.department,
        'position': employee_data.position
    }
    response = requests.put(base_url + '/', json=employee)
    assert response.status_code == 404


async def test_delete(employee_data: EmployeeIn):
    get_response = requests.get(base_url + '/%7Bid%7D?', params={'employee_id': str(employee_data.id)})
    response = requests.delete(base_url + '/%7Bid%7D?', params={'employee_id': str(employee_data.id)})
    assert response.status_code == 200
    assert response.json() == get_response.json()
    get_response = requests.get(base_url + '/%7Bid%7D?', params={'employee_id': str(employee_data.id)})
    assert get_response.status_code == 404


async def test_delete_wrong_id(employee_data: EmployeeIn):
    response = requests.delete(base_url + '/%7Bid%7D?', params={'employee_id': str(employee_data.id)})
    assert response.status_code == 404
