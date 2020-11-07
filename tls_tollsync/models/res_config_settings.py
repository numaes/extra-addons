from odoo import api, fields, models

TOOLS = 'tls.tools'


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tls_google_maps_api_key = fields.Char("Google Maps Platform API Key", config_parameter='base_geolocalize.google_map_api_key')
    tls_route_disable = fields.Boolean("Disable Route Widget", config_parameter='tls.route_disable')
    # TOLLSYNC.EU
    tls_use_route_booster = fields.Boolean("Use Tollsync.eu booster", config_parameter='tls.use_route_booster')
    tls_booster_confirmed = fields.Boolean("TLS_test_confirmed", config_parameter='tls.booster_confirmed')
    tls_booster_password = fields.Char("Tollsync.eu password", config_parameter='tls.booster_password')
    tls_booster_login = fields.Char("Login details", config_parameter='tls.booster_login')

    @api.onchange('tls_booster_login', 'tls_booster_password')
    def tls_onchange_booster_details(self):
        login, password = self.env[TOOLS].get_params(['tls.booster_login', 'tls.booster_password'])
        if self.tls_booster_login != login or self.tls_booster_password != password:
            self.tls_drop_booster_confirmed()

    def tls_test_connect(self):
        if self.env[TOOLS].booster_login(self.tls_booster_login, self.tls_booster_password):
            self.env[TOOLS].set_params({'tls.booster_confirmed': True})

    def tls_retest_connect(self):
        self.tls_drop_booster_confirmed()
        self.tls_test_connect()

    def tls_drop_booster_confirmed(self):
        if self.tls_booster_confirmed:
            self.tls_booster_confirmed = False
