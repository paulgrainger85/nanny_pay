from xmlrpc.client import Boolean
from sqlalchemy import Column, Integer, String, Float, BOOLEAN
from models.base import Base


class FederalTaxes(Base):
    __tablename__ = 'federal_taxes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(String, nullable=False)
    tax_type = Column(String, nullable=False)
    tax_rate = Column(Float, nullable=False)
    tax_threshold = Column(Integer)
    filing_status = Column(String)
    annual_limit = Column(Integer)


class StateTaxes(Base):
    __tablename__ = 'state_taxes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(String, nullable=False)
    year = Column(String, nullable=False)
    tax_type = Column(String, nullable=False)
    tax_rate = Column(Float, nullable=False)
    tax_threshold = Column(Integer)
    filing_status = Column(String)
    annual_limit = Column(Integer)
    use_deduction = Column(BOOLEAN)


class StandardDeduction(Base):
    __tablename__ = 'standard_deduction'

    id = Column(Integer, primary_key=True)
    year = Column(String, nullable=False)
    state = Column(String, nullable=False)
    filing_status = Column(String, nullable=False)
    deduction = Column(Integer, nullable=False)
