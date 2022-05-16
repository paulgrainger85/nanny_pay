import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

sys.path.append("/home/paul/git/nanny_pay/app")


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes # noqa
from app.models import employee, taxes # noqa

from backfill.backfill_taxes import backfill_command # noqa
from backfill.backfill_taxes import backfill_wages_command # noqa
app.cli.add_command(backfill_command)
app.cli.add_command(backfill_wages_command)
