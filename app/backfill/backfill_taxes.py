from app import db
import click
from flask.cli import with_appcontext


federal_taxes_query = """
    insert into federal_taxes(year, tax_type, tax_rate,
        tax_threshold, filing_status, annual_limit)
    values
        ('2022', 'income_tax', 0.1, 10275, 'Single',0),
        ('2022', 'income_tax', 0.12, 41775, 'Single',0),
        ('2022', 'income_tax', 0.22, 89075, 'Single',0),
        ('2022', 'income_tax', 0.24, 170050, 'Single',0),
        ('2022', 'income_tax', 0.32, 215950, 'Single',0),
        ('2022', 'income_tax', 0.35, 539900, 'Single',0),
        ('2022', 'income_tax', 0.37, 999999999, 'Single',0),
        ('2022', 'income_tax', 0.1, 20550, 'Married',0),
        ('2022', 'income_tax', 0.12, 83550, 'Married',0),
        ('2022', 'income_tax', 0.22, 178150, 'Married',0),
        ('2022', 'income_tax', 0.24, 340100, 'Married',0),
        ('2022', 'income_tax', 0.32, 431900, 'Married',0),
        ('2022', 'income_tax', 0.35, 647850, 'Married',0),
        ('2022', 'income_tax', 0.37, 999999999, 'Married',0),
        ('2022', 'social_security', 0.062, 0, 'Single',8500),
        ('2022', 'medicare', 0.0145, 0, 'Single',0);

    insert into standard_deduction(year, filing_status, deduction, state)
    values
        ('2022', 'Single', 12950, 'Federal'),
        ('2022', 'Married', 25900, 'Federal'),
        ('2022', 'Head_of_Household', 19400, 'Federal');

    insert into sick_leave(date, id, accrued_leave)
    values
        ('2022-01-01', 1, 0.03333);
"""


ca_state_tax = """
    insert into state_taxes(state, year, tax_type, tax_rate,
        tax_threshold, filing_status, annual_limit, use_deduction)
    values
        ('CA','2022','state_income_tax',0.01, 9325, 'Single',0, True),
        ('CA','2022','state_income_tax',0.02, 22107, 'Single',0, True),
        ('CA','2022','state_income_tax',0.04, 34892, 'Single',0, True),
        ('CA','2022','state_income_tax',0.06, 48435, 'Single',0, True),
        ('CA','2022','state_income_tax',0.08, 61214, 'Single',0, True),
        ('CA','2022','state_income_tax',0.093, 312686, 'Single',0, True),
        ('CA','2022','state_income_tax',0.103, 375221, 'Single',0, True),
        ('CA','2022','state_income_tax',0.113, 625369, 'Single',0, True),
        ('CA','2022','state_income_tax',0.123, 999999999,'Single',0,True),
        ('CA','2022','state_income_tax',0.01, 18650, 'Married',0, True),
        ('CA','2022','state_income_tax',0.02, 44214, 'Married',0, True),
        ('CA','2022','state_income_tax',0.04, 69784, 'Married',0, True),
        ('CA','2022','state_income_tax',0.06, 96870, 'Married',0, True),
        ('CA','2022','state_income_tax',0.08, 122428, 'Married',0, True),
        ('CA','2022','state_income_tax',0.093, 625372, 'Married',0, True),
        ('CA','2022','state_income_tax',0.103, 750442, 'Married',0, True),
        ('CA','2022','state_income_tax',0.113, 1250738,'Married',0, True),
        ('CA','2022','state_income_tax',0.123,999999999,'Married',0,True),
        ('CA','2022','CA_sdi', 0.011, 99999999, 'Single',80080, False),
        ('CA','2022','CA_sdi', 0.011, 99999999, 'Married',80080, False);

    insert into standard_deduction(year, filing_status, deduction, state)
    values
        ('2022', 'Single', 4803, 'CA'),
        ('2022', 'Married', 9606, 'CA'),
        ('2022', 'Head_of_Household', 9606, 'CA');
    """


def backfill_taxes():
    db.session.execute(federal_taxes_query)
    db.session.execute(ca_state_tax)
    db.session.commit()


@click.command('backfill-taxes')
@with_appcontext
def backfill_command():
    backfill_taxes()


@click.command("backfill-wages")
@click.option("--file")
def backfill_wages_command(file):
    # backfill_wages(file)
    print(file)
