# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from dateutil import relativedelta

from odoo.addons.payroll.tests.common import TestPayslipBase


class TestPayrollAccount(TestPayslipBase):
    """[20.0] This case used to stand on demo data — `base.res_partner_12`,
    `base.res_bank_1`, `base.res_partner_address_27`, `hr.dep_rd` and payroll's
    own demo salary rules. Odoo 20 does not load demo data unless asked for it,
    and asking for it brings its own noise, so the case now builds on the
    fixture `payroll` already maintains for its own suite and adds only what it
    is really about: the accounts, the journal and the entries they produce.
    """

    def setUp(self):
        super().setUp()

        # Activate company currency
        self.env.user.company_id.currency_id.active = True

        self.payslip_action_id = self.ref("payroll.hr_payslip_menu")

        self.hr_employee_john = self.richard_emp

        self.account_debit = self.env["account.account"].create(
            {
                "name": "Debit Account",
                "code": "334411",
                "account_type": "expense",
                "reconcile": True,
            }
        )
        self.account_credit = self.env["account.account"].create(
            {
                "name": "Credit Account",
                "code": "114433",
                "account_type": "expense",
                "reconcile": True,
            }
        )

        self.account_journal = self.env["account.journal"].create(
            {
                "name": "Vendor Bills - Test",
                "code": "TEXJ",
                "type": "purchase",
                "default_account_id": self.account_debit.id,
                "refund_sequence": True,
            }
        )

        self.hr_structure_softwaredeveloper = self.developer_pay_structure
        self.hr_contract_john = self.richard_contract
        self.hr_contract_john.journal_id = self.account_journal.id

    def _update_account_in_rule(self, debit, credit):
        self.rule_hra.write({"account_debit": debit, "account_credit": credit})

    def _prepare_payslip(self, employee):
        date_from = datetime.now()
        date_to = datetime.now() + relativedelta.relativedelta(
            months=+1, day=1, days=-1
        )
        self.hr_payslip = self.env["hr.payslip"].create(
            {
                "employee_id": self.hr_employee_john.id,
                "contract_id": self.hr_contract_john.id,
                "struct_id": self.hr_structure_softwaredeveloper.id,
            }
        )
        res = self.hr_payslip.get_payslip_vals(date_from, date_to, employee.id)
        vals = {
            "struct_id": res["value"]["struct_id"],
            "contract_id": res["value"]["contract_id"],
            "name": res["value"]["name"],
        }
        vals["worked_days_line_ids"] = [
            (0, 0, i) for i in res["value"]["worked_days_line_ids"]
        ]
        vals["input_line_ids"] = [(0, 0, i) for i in res["value"]["input_line_ids"]]
        vals.update({"contract_id": self.hr_contract_john.id})
        self.hr_payslip.write(vals)
        return self.hr_payslip

    def test_00_hr_payslip(self):
        """checking the process of payslip."""
        self._update_account_in_rule(self.account_debit, self.account_credit)
        self._prepare_payslip(self.hr_employee_john)

        # I assign the amount to Input data.
        payslip_input = self.env["hr.payslip.input"].search(
            [("payslip_id", "=", self.hr_payslip.id)]
        )
        payslip_input.write({"amount": 5.0})

        # I verify the payslip is in draft state.
        self.assertEqual(self.hr_payslip.state, "draft", "State not changed!")

        # I click on "Compute Sheet" button.
        self.hr_payslip.with_context(
            {},
            lang="en_US",
            tz=False,
            active_model="hr.payslip",
            department_id=False,
            active_ids=[self.payslip_action_id],
            section_id=False,
            active_id=self.payslip_action_id,
        ).compute_sheet()

        # I want to check cancel button.
        # So I first cancel the sheet then make it set to draft.
        self.hr_payslip.action_payslip_cancel()
        self.assertEqual(self.hr_payslip.state, "cancel", "Payslip is rejected.")
        self.hr_payslip.action_payslip_draft()

        self.hr_payslip.action_payslip_done()

        # I verify that the Accounting Entries are created.
        self.assertTrue(self.hr_payslip.move_id, "Accounting Entries should be created")

        # I verify that the payslip is in done state.
        self.assertEqual(self.hr_payslip.state, "done", "State not changed!")

    def test_hr_payslip_no_accounts(self):
        self._prepare_payslip(self.hr_employee_john)

        # I click on "Compute Sheet" button.
        self.hr_payslip.with_context(
            {},
            lang="en_US",
            tz=False,
            active_model="hr.payslip",
            department_id=False,
            active_ids=[self.payslip_action_id],
            section_id=False,
            active_id=self.payslip_action_id,
        ).compute_sheet()

        # Confirm Payslip (no account moves)
        self.hr_payslip.action_payslip_done()
        self.assertFalse(self.hr_payslip.move_id, "Accounting Entries has been created")

        # I verify that the payslip is in done state.
        self.assertEqual(self.hr_payslip.state, "done", "State not changed!")
