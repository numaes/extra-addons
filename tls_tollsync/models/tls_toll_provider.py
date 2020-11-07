from odoo import models, fields


class TollProvider(models.Model):
    _name = 'tls.toll.provider'
    _description = "Toll road provider"

    def _compute_count(self):
        for rec in self:
            rec.count = self.env['tls.toll'].search_count([('provider', '=', rec.id)])

    name = fields.Char("Provider")
    code = fields.Char("Provider code", readonly=True)
    count = fields.Integer("Tolls", compute='_compute_count')
    vendor = fields.Many2one('res.partner', "Vendor")
    last_sync = fields.Datetime("Last syncing date")
