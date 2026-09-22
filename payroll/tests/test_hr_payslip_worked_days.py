# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
from datetime import date, datetime

from odoo.tests import Form

from .common import TestPayslipBase


class TestWorkedDays(TestPayslipBase):
    def setUp(self):
        super().setUp()

        if "hr.leave" not in self.env:
            # These cases need `hr_holidays`, which payroll does not depend on:
            # leave data is read only where it happens to exist. Saying so beats
            # failing on a model that was never promised.
            self.skipTest("hr_holidays is not installed")

        self.LeaveRequest = self.env["hr.leave"]
        # [20.0] `hr.leave.type` was folded into `hr.work.entry.type`, and the
        # leave points at it through `work_entry_type_id`, not
        # `holiday_status_id`.
        self.LeaveType = self.env["hr.work.entry.type"]

        # create holiday type
        self.holiday_type = self.LeaveType.create(
            {
                "name": "TestLeaveType",
                # [20.0] A work entry type must have a code, so a leave always
                # names one: the worked-days line carries that code instead of
                # falling back to "GLOBAL" as it did when the leave type had no
                # work entry type behind it.
                "code": "TESTLEAVE",
                # A work entry type counts as working time unless it says
                # otherwise, so a leave type that does not declare itself an
                # absence takes nothing off the worked days.
                "count_as": "absence",
                "allocation_validation_type": "no_validation",
                "leave_validation_type": "no_validation",
            }
        )

        self.full_calendar = self.ResourceCalendar.create(
            {
                # [20.0] `resource.calendar` no longer carries a timezone, and
                # it is created with a default week of duration-based slots. A
                # day cannot mix duration-based and time-based attendances, so
                # the defaults have to go before the hourly ones below.
                "name": "56 Hrs a week",
                "attendance_ids": [(5, 0, 0)],
            }
        )
        # Create a full 7-day week sor our tests don't fail on Sat. and Sun.
        for day in ["0", "1", "2", "3", "4", "5", "6"]:
            self.CalendarAttendance.create(
                {
                    "calendar_id": self.full_calendar.id,
                    # [20.0] `resource.calendar.attendance` has no `name`: a
                    # slot is identified by its day and period.
                    "dayofweek": day,
                    "day_period": "morning",
                    "hour_from": 8,
                    "hour_to": 12,
                }
            )
            self.CalendarAttendance.create(
                {
                    "calendar_id": self.full_calendar.id,
                    "dayofweek": day,
                    "day_period": "afternoon",
                    "hour_from": 13,
                    "hour_to": 17,
                }
            )

    def _common_contract_leave_setup(self):
        self.richard_emp.resource_id.calendar_id = self.full_calendar
        self.richard_emp.version_ids.resource_calendar_id = self.full_calendar

        # I put all eligible contracts (including Richard's) in an "open" state
        self.apply_contract_cron()

        self.env["hr.leave.allocation"].create(
            {
                "name": "Annual Time Off",
                "employee_id": self.richard_emp.id,
                "work_entry_type_id": self.holiday_type.id,
                "number_of_days": 20,
                "state": "confirm",
                "date_from": time.strftime("%Y-01-01"),
                "date_to": time.strftime("%Y-12-31"),
            }
        )

        # Create the leave
        self.LeaveRequest.create(
            {
                "name": "Hol11",
                "employee_id": self.richard_emp.id,
                "work_entry_type_id": self.holiday_type.id,
                "date_from": datetime.combine(date.today(), datetime.min.time()),
                "date_to": datetime.combine(date.today(), datetime.max.time()),
                "number_of_days": 1,
            }
        )

    def test_worked_days_negative(self):
        self._common_contract_leave_setup()

        # Set system parameter
        self.env["ir.config_parameter"].sudo().set_bool(
            "payroll.leaves_positive", False
        )

        # I create an employee Payslip
        frm = Form(self.Payslip)
        frm.employee_id = self.richard_emp
        richard_payslip = frm.save()

        worked_days_codes = richard_payslip.worked_days_line_ids.mapped("code")
        self.assertIn(
            "TESTLEAVE", worked_days_codes, "The leave is in the 'Worked Days' list"
        )
        wdl_ids = richard_payslip.worked_days_line_ids.filtered(
            lambda x: x.code == "TESTLEAVE"
        )
        self.assertEqual(len(wdl_ids), 1, "There is only one line matching the leave")
        self.assertEqual(
            wdl_ids[0].number_of_days,
            -1.0,
            "The days worked value is a NEGATIVE number",
        )
        self.assertEqual(
            wdl_ids[0].number_of_hours,
            -8.0,
            "The hours worked value is a NEGATIVE number",
        )

    def test_leaves_positive(self):
        self._common_contract_leave_setup()

        # Set system parameter
        self.env["ir.config_parameter"].sudo().set_bool(
            "payroll.leaves_positive", True
        )

        # I create an employee Payslip
        frm = Form(self.Payslip)
        frm.employee_id = self.richard_emp
        richard_payslip = frm.save()

        worked_days_codes = richard_payslip.worked_days_line_ids.mapped("code")
        self.assertIn(
            "TESTLEAVE", worked_days_codes, "The leave is in the 'Worked Days' list"
        )
        wdl_ids = richard_payslip.worked_days_line_ids.filtered(
            lambda x: x.code == "TESTLEAVE"
        )
        self.assertEqual(len(wdl_ids), 1, "There is only one line matching the leave")
        self.assertEqual(
            wdl_ids[0].number_of_days, 1.0, "The days worked value is a POSITIVE number"
        )
        self.assertEqual(
            wdl_ids[0].number_of_hours,
            8.0,
            "The hours worked value is a POSITIVE number",
        )
