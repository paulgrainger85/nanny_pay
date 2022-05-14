import datetime as dt
from sqlalchemy import func

from db import session, upsert
from models.employee import Employee, SickLeave


def get_employee_config(id, include_sensitive=False):
    employee = session.query(Employee).filter(
        Employee.id==id # noqa
    )
    for row in employee:
        config = row.__dict__
        config.pop('_sa_instance_state')
        if not include_sensitive:
            config.pop('ssn')

    sick_leave = session.query(func.sum(SickLeave.accrued_leave)).filter(
        SickLeave.id==id # noqa
    ).scalar()

    config.update({'accrued_sick_leave': sick_leave})
    return config


def add_new_employee(**kwargs):
    qry = session.query("select max(id) as id from employee")
    for row in qry:
        eid = 1 + row.__dict__['id']

    new_employee = kwargs
    new_employee.update({'id': eid})

    if not new_employee.get('hire_date'):
        new_employee.update({'hire_date': dt.date.today()})

    upsert(Employee, new_employee, [Employee.id])

    return new_employee

