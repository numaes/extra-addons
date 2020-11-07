import json

from odoo import http
from odoo.http import request


class Google(http.Controller):

    @http.route('/tls/google_maps_api_key', type='json', auth='public', website=True)
    def google_maps_api_key(self):
        api_key = request.env['ir.config_parameter'].sudo().get_param('base_geolocalize.google_map_api_key')
        return json.dumps({'google_maps_api_key': api_key})
