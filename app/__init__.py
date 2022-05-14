from crypt import methods
import sys
from flask import Flask, render_template, request
import datetime as dt


sys.path.append("/home/paul/git/nanny_pay/app")

from calc.timesheets import update_hours

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass
    from . import db
    db.init_app(app)

    # a simple page that says hello
    @app.route('/timesheets')
    def enter_timesheets():
        today = dt.date.today()
        start_of_week = today - dt.timedelta(days=today.isoweekday() - 1)
        this_week = [start_of_week + dt.timedelta(days=i) for i in range(7)]
        days_of_week = ['Monday','Tuesday','Wednesday',
            'Thursday','Friday','Saturday','Sunday']

        date_dict = dict(zip(days_of_week, this_week))
        employees = db.session.execute("select id, name from employee")

        return render_template(
            'timesheets.html',
            employees=[e for e in employees],
            **date_dict
            )

    @app.route('/enter-timesheets', methods=["POST", "GET"])
    def data():
        form = request.form
        # return form
        dateHours = {}
        for str_dt, hours in form.items():
            if not str_dt == 'employee':
                if not hours == '':
                    dateHours[dt.date.fromisoformat(str_dt)] = float(hours)
        update_hours(form['employee'], dateHours)
        return form

    return app
