from db import session
from models.taxes import FederalTaxes, StandardDeduction


def get_taxes(tax, filing_status='Single'):
    taxes = []
    tax_config = session.query(
        FederalTaxes).filter(
            FederalTaxes.tax_type==tax # noqa
        ).filter(
            FederalTaxes.filing_status==filing_status # noqa
        )

    for row in tax_config:

        taxes.append(
            {
                'threshold': row.__dict__['tax_threshold'],
                'rate': row.__dict__['tax_rate'],
                'limit': row.__dict__['annual_limit'],
            }
        )
    return taxes


def get_standard_deduction(status, tax_year):
    data = session.query(StandardDeduction).filter(
        StandardDeduction.filing_status==status # noqa
    ).filter(
        StandardDeduction.year==tax_year # noqa
    )
    deduction = 0
    for row in data:
        deduction = row.__dict__['deduction']
    return deduction


def calc_federal_tax(
    income,
    filing_status='Single',
    period=52,
    tax_year='2022'
        ):

    total_tax = {'ss': 0, 'medicare': 0, "income": 0}
    income_tax = get_taxes('income_tax', filing_status)
    medicare = get_taxes('medicare')
    social_security = get_taxes('social_security')
    deduction = get_standard_deduction(filing_status, tax_year) / period

    # calculate medicare first
    total_tax['medicare'] = round(income * medicare[0]['rate'], 2)
    # next social security
    total_tax['ss'] = round(income * social_security[0]['rate'], 2)
    # finally calculate income tax
    taxable_income = max(0, income - deduction)
    if taxable_income:
        for tax in income_tax:
            threshold = tax['threshold'] / period
            total_tax['income'] += tax['rate'] * min(threshold, taxable_income)
            taxable_income = max(0, taxable_income - threshold)
    total_tax['income'] = round(total_tax['income'], 2)
    return total_tax
