import datetime as dt
from email.policy import default
from app import app, db
from sqlalchemy.dialects.postgresql import JSON


class Employee(db.Model):
    __tablename__ = 'employee'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    state = db.Column(db.String)
    address = db.Column(db.String)
    ssn = db.Column(db.String)
    hire_date = db.Column(db.DateTime, default=dt.datetime.utcnow())
    filing_status = db.Column(db.String)
    wage = db.Column(db.Float)
    sick_leave_rate = db.Column(db.Float)
    active = db.Column(db.Boolean)
    update_ts = db.Column(db.DateTime)


class EmployeeTax(db.Model):
    __tablename__ = 'employee_tax'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    federal_tax = db.Column(JSON)
    state_tax = db.Column(JSON)
    local_tax = db.Column(JSON)


class Timesheets(db.Model):
    __tablename__ = 'timesheets'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, primary_key=True)
    update_ts = db.Column(db.DateTime)
    hours = db.Column(db.Float)


class Payroll(db.Model):
    __tablename__ = 'payroll'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, primary_key=True)
    update_ts = db.Column(db.DateTime)
    gross_pay = db.Column(db.Float)
    net_pay = db.Column(db.Float)
    income_tax = db.Column(db.Float)
    medicare = db.Column(db.Float)
    social_security = db.Column(db.Float)
    state_taxes = db.Column(JSON)
    employer_medicare = db.Column(db.Float)
    employer_social_security = db.Column(db.Float)
    employer_unemployment = db.Column(db.Float)
    employer_state_taxes = db.Column(JSON)


class SickLeave(db.Model):
    __tablename__ = 'sick_leave'
    __table_args__ = {'extend_existing': True}

    date = db.Column(db.DateTime, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    accrued_leave = db.Column(db.Float)
