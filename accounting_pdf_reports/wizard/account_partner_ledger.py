# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountPartnerLedger(models.TransientModel):
    _name = "account.report.partner.ledger"
    _inherit = "account.common.partner.report"
    _description = "Account Partner Ledger"

    amount_currency = fields.Boolean("With Currency",
                                     help="It adds the currency column on "
                                          "report if the currency differs from "
                                          "the company currency.")
    reconciled = fields.Boolean('Reconciled Entries')

    def _get_report_data(self, data):
        data = self.pre_print_report(data)
        data['form'].update({'reconciled': self.reconciled,
                             'amount_currency': self.amount_currency})
        if data['form']['l10n_ar_afip_no_register'] == 'no_register':
            data['form']['l10n_ar_afip_no_register'] = True
            data['form']['used_context']['l10n_ar_afip_no_register'] = True
        elif data['form']['l10n_ar_afip_no_register'] == 'register':
            data['form']['l10n_ar_afip_no_register'] = False
            data['form']['used_context']['l10n_ar_afip_no_register'] = False
        else:
            del data['form']['l10n_ar_afip_no_register']
        return data

    def _print_report(self, data):
        data = self._get_report_data(data)
        return self.env.ref('accounting_pdf_reports.action_report_partnerledger').with_context(landscape=True).\
            report_action(self, data=data)
