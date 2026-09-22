# Part of Odoo. See LICENSE file for full copyright and licensing details.

from pytz import UTC

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"
    _description = "Employee"

    slip_ids = fields.One2many(
        "hr.payslip", "employee_id", string="Payslips", readonly=True
    )
    payslip_count = fields.Integer(
        compute="_compute_payslip_count",
        groups="payroll.group_payroll_user",
    )

    def _compute_payslip_count(self):
        for employee in self:
            employee.payslip_count = len(employee.slip_ids)

    def _get_employee_contract_versions(self, date_from, date_to):
        """Return the contract versions of these employees covering a period.

        [20.0] `hr_contract` used to add `hr.employee._get_contracts(date_from,
        date_to, states)` returning an `hr.contract` recordset. The core `hr`
        module now owns a method of the same name with a different signature —
        `_get_contracts(date_start, date_end, use_latest_version, domain)` — and
        it returns a dict keyed by employee id, not a recordset. Payroll works
        on a flat set of versions, so this wrapper keeps the call sites honest
        instead of shadowing a core method with an incompatible one.
        """
        versions = self.env["hr.version"]
        for employee_versions in self._get_contracts(
            date_start=date_from, date_end=date_to
        ).values():
            versions |= employee_versions
        return versions

    def list_leaves(self, from_datetime, to_datetime, calendar=None, domain=None):
        """Return a list of `(day, hours, resource.calendar.leaves)` tuples.

        [20.0] `resource.mixin.list_leaves` was dropped from the core: what
        survives is `_get_leave_days_data_batch`, which totals days and hours
        and loses the per-day, per-leave detail payroll needs to split a period
        by leave type. The primitives it was built on are still there, so this
        is the 18.0 body with the signatures the 20.0 calendar now takes
        (`resources_per_tz` instead of a bare resource).
        """
        self.ensure_one()
        resource = self.resource_id
        calendar = calendar or self.resource_calendar_id

        # naive datetimes are made explicit in UTC
        if not from_datetime.tzinfo:
            from_datetime = from_datetime.replace(tzinfo=UTC)
        if not to_datetime.tzinfo:
            to_datetime = to_datetime.replace(tzinfo=UTC)

        resources_per_tz = resource._get_resources_per_tz()
        attendances = calendar._attendance_intervals_batch(
            from_datetime, to_datetime, resources_per_tz
        )[resource.id]
        leaves = calendar._leave_intervals_batch(
            from_datetime, to_datetime, resources_per_tz, domain
        )[resource.id]
        result = []
        for start, stop, leave in leaves & attendances:
            hours = (stop - start).total_seconds() / 3600
            result.append((start.date(), hours, leave))
        return result
