from sqlalchemy import Column, Integer, String, \
    Float, DateTime, Date, Boolean, JSON
from models.base import Base


class Employee(Base):
    __tablename__ = 'employee'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    state = Column(String)
    address = Column(String)
    ssn = Column(String)
    hire_date = Column(Date)
    filing_status = Column(String)
    wage = Column(Float)
    sick_leave_rate = Column(Float)
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
    net_pay = Column(Float)
    income_tax = Column(Float)
    medicare = Column(Float)
    social_security = Column(Float)
    state_taxes = Column(JSON)
    employer_medicare = Column(Float)
    employer_social_security = Column(Float)
    employer_unemployment = Column(Float)
    employer_state_taxes = Column(JSON)


class SickLeave(Base):
    __tablename__ = 'sick_leave'
    __table_args__ = {'extend_existing': True}

    date = Column(Date, primary_key=True)
    id = Column(Integer, primary_key=True)
    accrued_leave = Column(Float)
