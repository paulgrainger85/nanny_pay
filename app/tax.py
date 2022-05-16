from app import db
from models.taxes import FederalTaxes, StandardDeduction, StateTaxes


def get_taxes(tax, filing_status='Single'):
    taxes = []
    tax_config = db.session.query(
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


def get_state_taxes(state, year, filing_status='Single'):
    taxes = {}
    tax_config = db.session.query(
        StateTaxes).filter(
            StateTaxes.state==state # noqa
        ).filter(
            StateTaxes.year==year # noqa
        ).filter(
            StateTaxes.filing_status==filing_status # noqa
    )
    for row in tax_config:

        tax_type = row.__dict__['tax_type']
        if tax_type not in taxes:
            taxes[tax_type] = []

        taxes[tax_type].append(
            {
                'threshold': row.__dict__['tax_threshold'],
                'rate': row.__dict__['tax_rate'],
                'limit': row.__dict__['annual_limit'],
                'use_deduction': row.__dict__['use_deduction'],
            }
        )
    return taxes


def get_standard_deduction(status, tax_year, state):
    data = db.session.query(StandardDeduction).filter(
        StandardDeduction.filing_status==status # noqa
    ).filter(
        StandardDeduction.year==tax_year # noqa
    ).filter(
        StandardDeduction.state==state # noqa
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
    tax = calc_employee_federal_tax(
        income, filing_status, period, tax_year
    )

    tax.update(calc_employer_federal_tax(
        income, period, tax_year)
    )

    return tax


def calc_employee_federal_tax(
    income,
    filing_status='Single',
    period=52,
    tax_year='2022'
        ):

    total_tax = {'ss': 0, 'medicare': 0, "irs_income_tax": 0}
    income_tax = get_taxes('income_tax', filing_status)
    medicare = get_taxes('medicare')
    social_security = get_taxes('social_security')
    deduction = get_standard_deduction(
        filing_status, tax_year, 'Federal') / period

    # calculate medicare first
    total_tax['medicare'] = round(income * medicare[0]['rate'], 2)
    # next social security
    total_tax['ss'] = round(income * social_security[0]['rate'], 2)
    # finally calculate income tax
    taxable_income = max(0, income - deduction)
    if taxable_income:
        for tax in income_tax:
            threshold = tax['threshold'] / period
            total_tax['irs_income_tax'] += \
                tax['rate'] * min(threshold, taxable_income)
            taxable_income = max(0, taxable_income - threshold)
    total_tax['irs_income_tax'] = round(total_tax['irs_income_tax'], 2)
    return total_tax


def calc_employer_federal_tax(
    income,
    period,
    tax_year,
        ):

    total_tax = {}
    medicare = get_taxes('medicare')
    social_security = get_taxes('social_security')

    total_tax['employer_medicare'] = round(income * medicare[0]['rate'], 2)
    total_tax['employer_ss'] = round(income * social_security[0]['rate'], 2)

    return total_tax


def calc_state_tax(
    income,
    state,
    filing_status='Single',
    period=52,
    tax_year='2022'
        ):

    tax = calc_employee_state_tax(
        income, state, filing_status, period, tax_year)
    tax.update(
        calc_employer_state_tax(
            income, state, period, tax_year)
    )

    return tax


def calc_employee_state_tax(
    income,
    state,
    filing_status='Single',
    period=52,
    tax_year='2022'
        ):

    taxes = get_state_taxes(state, tax_year, filing_status)
    deduction = get_standard_deduction(
        filing_status, tax_year, state) / period

    total_tax = {}

    for tax_type in taxes.keys():
        if taxes[tax_type][0]['use_deduction']:
            taxable_income = max(0, income - deduction)
        else:
            taxable_income = income

        total_tax[tax_type] = 0
        for tax in taxes[tax_type]:
            threshold = tax['threshold'] / period
            total_tax[tax_type] += tax['rate'] * min(threshold, taxable_income)
            taxable_income = max(0, taxable_income - threshold)
        total_tax[tax_type] = round(total_tax[tax_type], 2)
    return total_tax


def calc_employer_state_tax(
    income,
    state,
    period,
    tax_year,
        ):

    return {}


def calc_tax(income, state, filing_status, period, tax_year):
    taxes = {}
    taxes.update(calc_federal_tax(
        income, filing_status, period, tax_year))
    taxes.update(calc_state_tax(
        income, state, filing_status, period, tax_year))
    return taxes
