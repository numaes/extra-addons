from odoo import models, fields


###################
# Config Settings #
###################
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cetmix_plantuml_server_url = fields.Char(string="Server URL",
                                             config_parameter="cx_odoo_plantuml.cetmix_plantuml_server_url")
    cx_max_selection = fields.Integer(string="Max Selection Options",
                                      help="If the number of options for Selection field exceeds this amount"
                                           " it will be shortened to 'x options'",
                                      config_parameter="cx_odoo_plantuml.max_selection")
