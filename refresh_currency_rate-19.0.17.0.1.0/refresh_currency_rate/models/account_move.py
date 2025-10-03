from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_refresh_currency_rate(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_("Only draft invoices can refresh currency rates"))
            
        if self.currency_id == self.company_id.currency_id:
            raise UserError(_("No need to refresh rate for company currency"))
        
        date = self.invoice_date or fields.Date.context_today(self)
        currency_rates = self.currency_id._get_rates(self.company_id, date)
        rate = currency_rates.get(self.currency_id.id)
        
        if not rate:
            raise UserError(_("No exchange rate found for %s on %s. Please configure rates first.") 
                            % (self.currency_id.name, date))
        
        # Update the currency rate and recompute related fields
        for line in self.line_ids:
            line._compute_amount_currency()

        self._compute_amount()

        # Log the rate refresh action
        self.message_post(body=_("Exchange rate refreshed to %s for currency %s.") % (rate, self.currency_id.name))
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Currency Rate Updated'),
                'message': _('Exchange rate has been successfully updated to %s') % rate,
                'sticky': False,
            }
        }
    