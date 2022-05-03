from operator import index
import click
from flask.cli import with_appcontext

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert

from models.base import Base
import models.employee
import models.taxes # noqa


engine = create_engine(
    "postgresql://admin:mypassword123@localhost:15001/default"
)

# SqlAlchemy :: Session setup
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    Base.metadata.create_all(engine)


def upsert(table, data, index_elements):

    stmt = insert(table).values(data)
    stmt = stmt.on_conflict_do_update(
        index_elements=index_elements,
        set_=data,
    )
    session.execute(stmt)
    session.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database")


def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(load_data_command)
    app.cli.add_command(test_print)


insert_statement = """
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

        insert into standard_deduction(year, filing_status, deduction)
        values
            ('2022', 'Single', 12950),
            ('2022', 'Married', 25900),
            ('2022', 'Head_of_Household', 19400);
    """


def load_data():
    session.execute(insert_statement)
    session.commit()


@click.command('load-data')
@with_appcontext
def load_data_command():
    load_data()


@click.command("print-test")
@click.option("--foo")
def test_print(foo):
    print(foo)
