from sqlalchemy import Column, Integer, String, \
    Float, DateTime, Date, Boolean, JSON
from models.base import Base


class Employee(Base):
    __tablename__ = 'employee'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    ssn = Column(String)
    hire_date = Column(Date)
    filing_status = Column(String)
    wage = Column(Float)
    active = Column(Boolean)
    update_ts = Column(DateTime)


class EmployeeTax(Base):
    __tablename__ = 'employee_tax'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    federal_tax = Column(JSON)
    state_tax = Column(JSON)
    local_tax = Column(JSON)


class Timesheets(Base):
    __tablename__ = 'timesheets'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    date = Column(Date, primary_key=True)
    updateTS = Column(DateTime)
    hours = Column(Float)


class Payroll(Base):
    __tablename__ = 'payroll'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    date = Column(Date, primary_key=True)
    update_ts = Column(DateTime)
    gross_pay = Column(Float)
    income_tax = Float(Float)
