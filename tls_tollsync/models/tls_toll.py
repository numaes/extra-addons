import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class TollRecord(models.Model):
    _name = 'tls.toll'
    _inherits = {'fleet.vehicle.log.services': 'cost_id'}
    _rec_name = 'entry_date'
    _description = "Toll road record"
    _order = 'entry_date desc'

    def _get_widget_param(self):
        self.hide_route_widget = self.env["tls.tools"].get_params(['tls.route_disable'])[0]

    def _get_route_booster_param(self):
        self.use_booster_widget = self.env["tls.tools"].get_params(['tls.use_route_booster'])[0]

    tid = fields.Char("Transaction ID")
    provider = fields.Many2one('tls.toll.provider', "Module", index=True, help="Information-providing module")
    inv_ref = fields.Many2one('account.move', "Vendor Bill", help="Invoice related to this toll")
    use_booster_widget = fields.Boolean("Use Booster Widget", compute="_get_route_booster_param")
    hide_route_widget = fields.Boolean("Disable Route Widget", compute="_get_widget_param")
    entry_name = fields.Char("Entry station", help="Name of the entry station")
    entry_lat = fields.Float("Entry lat", digits=(3, 6), help="Geographical coordinates: Latitude")
    entry_lng = fields.Float("Entry lng", digits=(3, 6), help="Geographical coordinates: Longitude")
    entry_date = fields.Datetime("Start of journey", default=fields.Datetime.now())
    exit_name = fields.Char("Exit station", help="Name of the exit station")
    exit_lat = fields.Float("Exit lat", digits=(3, 6), help="Geographical coordinates: Latitude")
    exit_lng = fields.Float("Exit lng", digits=(3, 6), help="Geographical coordinates: Longitude")
    distance = fields.Float("Distance", digits=(4, 1), help="Journey distance, km")
    route_image = fields.Binary("Route image", help="Image file for Route widget")
    description = fields.Char("Cost Description")
    notes = fields.Text("Notes")
    # INHERITS
    cost_id = fields.Many2one('fleet.vehicle.log.services', 'Service', required=True, ondelete='cascade')
    cost_amount = fields.Monetary(related='cost_id.amount', string="Amount", store=True, readonly=False)

    @api.model
    def default_get(self, default_fields):
        res = super(TollRecord, self).default_get(default_fields)
        service = self.env.ref('tls_tollsync.type_service_toll', raise_if_not_found=False)
        res.update({
            'service_type_id': service and service.id or False,
            'state': 'done'})
        return res

    @api.model
    def get_booster_map(self, toll_id=None):
        toll, tools = toll_id and self.browse(toll_id) or self, self.env["tls.tools"]
        if toll and toll.route_image:
            return {'success': 'success', 'message': None}

        def request_map():
            res = tools.request(F"{api_url}/map", headers={'Authorization': token}, json={'orig': orig, 'dest': dest})
            need_token_refresh = isinstance(res, dict) and res.get('status_code') and res['status_code'] == 401
            return need_token_refresh and {'need_token_refresh': True} or res.json()

        api_url, sys_token = tools.get_params(['tls.booster_api_url', 'tls.booster_token'])
        token = sys_token or tools.booster_login(get_token=True)
        orig = {'lat': toll.entry_lat, 'lng': toll.entry_lng}
        dest = {'lat': toll.exit_lat, 'lng': toll.exit_lng}
        resp = toll and token and request_map() or {}  # REQUEST
        if resp.get('need_token_refresh'):
            token = tools.booster_login(get_token=True)
            resp = token and request_map()  # REQUEST
        if resp.get('success') and resp.get('base64'):
            _logger.debug('Map image received from the Tollsync.eu')
            toll.write({'route_image': resp['base64']})
        return {'success': resp.get('success'), 'message': resp.get('message')}

    @api.model
    def get_base64_map(self, toll_id=None):
        toll = toll_id and self.browse(toll_id) or self
        route_image = toll and toll.route_image
        return route_image and 'data:image/png;base64,' + route_image.decode('ascii')

    @api.onchange('entry_name', 'exit_name')
    def get_description(self):
        if self.entry_name and self.exit_name:
            self.update({'description': F"{self.entry_name} — {self.exit_name}"})

    @api.onchange('vehicle_id', 'entry_date')
    def get_related_driver(self):
        if self.vehicle_id and self.entry_date:
            res = self.env['fleet.vehicle.assignation.log'].search([
                ('vehicle_id', '=', self.vehicle_id.id), ('date_start', '<=', self.entry_date)], order='date_start desc', limit=1)
            self.purchaser_id = res and res.driver_id or self.vehicle_id.driver_id

    @api.constrains('description')
    def copy_description(self):
        for toll in self:
            if toll.cost_id and toll.description:
                toll.cost_id.write({'description': toll.description})

    @api.constrains('entry_date')
    def copy_entry_date(self):
        for toll in self:
            if toll.cost_id and toll.cost_id.date != toll.entry_date:
                toll.cost_id.write({'date': toll.entry_date})

    @api.constrains('entry_lat', 'entry_lng', 'exit_lat', 'exit_lng')
    def drop_map_img(self):
        for toll in self:
            if toll.route_image:
                toll.write({'route_image': False})
