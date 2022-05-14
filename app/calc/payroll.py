import json
import datetime as dt

from db import session, upsert
from models.employee import Payroll, SickLeave, Timesheets
from calc.tax import calc_tax
from calc.employee import get_employee_config


def get_days_in_week(day):
    weekday = day.isoweekday()
    # The start of the week
    start = day - dt.timedelta(days=weekday)
    # build a simple range
    return [start + dt.timedelta(days=d) for d in range(1, 8)]


def run_payroll(id, pay_date):
    dates = get_days_in_week(pay_date)

    timesheet_query = session.query(
        Timesheets).filter(
            Timesheets.id==id # noqa
        ).filter(
            Timesheets.date.between(dates[0], dates[6])
        )
    hours = 0
    for row in timesheet_query:
        hours += row.__dict__['hours']

    employee_config = get_employee_config(id)

    # TODO remove hardcoding of 52 weeks
    taxes = calc_tax(
        hours*employee_config['wage'],
        employee_config['state'],
        employee_config['filing_status'],
        52,
        str(dates[0])[:4]
    )

    social_security = taxes.pop('ss')
    medicare = taxes.pop('medicare')
    income_tax = taxes.pop('irs_income_tax')
    employer_medicare = taxes.pop('employer_medicare')
    employer_social_security = taxes.pop('employer_ss')

    total_taxes = social_security + medicare + income_tax
    for tax in taxes.values():
        total_taxes += tax

    payroll = {
        'id': id,
        'date': pay_date,
        'update_ts': dt.datetime.now(),
        'gross_pay': hours * employee_config.get('pay_rate'),
        'net_pay': (hours * employee_config.get('pay_rate')) - total_taxes,
        'income_tax': income_tax,
        'medicare': medicare,
        'social_security': social_security,
        'state_taxes': json.dumps(taxes),
        'employer_medicare': employer_medicare,
        'employer_social_security': employer_social_security,
    }

    upsert(Payroll, payroll, [Payroll.id, Payroll.date])

    upsert(
        SickLeave,
        {
            'id': id,
            'date': pay_date,
            'accrued_leave': employee_config.get('accrued_leave') +(hours*employee_config.get('sick_leave_rate')) # noqa
        },
        [SickLeave.date, SickLeave.id]
    )
