from sqlalchemy import Column, Integer, String, Float
from models.base import Base


class FederalTaxes(Base):
    __tablename__ = 'federal_taxes'

    id = Column(Integer, primary_key=True)
    year = Column(String, nullable=False)
    tax_type = Column(String, nullable=False)
    tax_rate = Column(Float, nullable=False)
    tax_threshold = Column(Integer)
    filing_status = Column(String)
    annual_limit = Column(Integer)


class StandardDeduction(Base):
    __tablename__ = 'standard_deduction'

    id = Column(Integer, primary_key=True)
    year = Column(String, nullable=False)
    filing_status = Column(String, nullable=False)
    deduction = Column(Integer, nullable=False)
