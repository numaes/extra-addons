from odoo import fields, models


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    def _compute_toll_count(self):
        for record in self:
            record.tolls_count = self.env['tls.toll'].search_count([('vehicle_id', '=', record.id)])

    tolls_count = fields.Integer(compute="_compute_toll_count", string='Road Toll Count')

    def return_action_to_open(self):
        """ OVERRIDE
            This opens the xml view specified in xml_id for the current vehicle """
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            dot = '.' in xml_id and xml_id.split('.')
            res = self.env['ir.actions.act_window']._for_xml_id(F"{dot and dot[0] or 'fleet'}.{dot and dot[1] or xml_id}")
            res.update(
                context=dict(self.env.context, default_vehicle_id=self.id, group_by=False),
                domain=[('vehicle_id', '=', self.id)])
            return res
        return False
