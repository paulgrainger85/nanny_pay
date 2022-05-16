import datetime as dt
from app import app, db
from flask import render_template, request

from timesheets import update_hours


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


@app.route('/payroll', methods=['POST', 'GET'])
def payroll():
    employees = db.session.execute("select id, name from employee")
    return render_template(
        'preview-payroll.html',
        employees=[e for e in employees],
    )


# @app.route('/preview-payroll.html', methods=['POST'])
# def preview_payroll():
#     form = request.form
