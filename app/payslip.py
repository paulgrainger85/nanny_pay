from employee import calc_employee_tax


class Payslip:

    def __init__(self, employeeId, date):
        self.employeeId = employeeId
        self.date = date

    def __str__(self):
        s = "***************\n"
        s += f"payslip for {self.employeeId}\n"
        s += "***************"

    def getWages(self):
        pass

    def getTaxes(self):
        pass
