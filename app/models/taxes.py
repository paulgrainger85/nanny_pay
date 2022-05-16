from app import app, db


class FederalTaxes(db.Model):
    __tablename__ = 'federal_taxes'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.String, nullable=False)
    tax_type = db.Column(db.String, nullable=False)
    tax_rate = db.Column(db.Float, nullable=False)
    tax_threshold = db.Column(db.Integer)
    filing_status = db.Column(db.String)
    annual_limit = db.Column(db.Integer)


class StateTaxes(db.Model):
    __tablename__ = 'state_taxes'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    tax_type = db.Column(db.String, nullable=False)
    tax_rate = db.Column(db.Float, nullable=False)
    tax_threshold = db.Column(db.Integer)
    filing_status = db.Column(db.String)
    annual_limit = db.Column(db.Integer)
    use_deduction = db.Column(db.BOOLEAN)


class StandardDeduction(db.Model):
    __tablename__ = 'standard_deduction'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    filing_status = db.Column(db.String, nullable=False)
    deduction = db.Column(db.Integer, nullable=False)
