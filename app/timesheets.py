import datetime as dt
from typing import Dict

from app import db
from app.utils import upsert
from models.employee import Timesheets


def update_hours(employee_id: int, hours: Dict):
    current_time = dt.datetime.utcnow()
    for date, hours_worked in hours.items():
        row = {
            'id': employee_id,
            'update_ts': current_time,
            'date': date,
            'hours': hours_worked,
        }
        upsert(Timesheets, row, [Timesheets.id, Timesheets.date])


def get_timesheets(employee_id: int, date):
    """
        Get the timesheets, date can either be a single date or a range
        employee_id(int): numerical identifier
        date(date or list): single date to retrieve or tuple of dates
    """
    query = db.session.query(Timesheets).filter(Timesheets.id==employee_id) # noqa
    if type(date) is list:
        query = query.filter(Timesheets.date.between(date[0], date[1]))
    else:
        query = query.filter(Timesheets.date==date) # noqa
    rows = [row.__dict__ for row in query]
    return [
        [r.get('id'), r.get('date'), r.get('hours'), r.get('update_ts')]
        for r in rows
    ]
