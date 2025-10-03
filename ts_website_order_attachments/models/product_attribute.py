# -*- coding: utf-8 -*-
#############################################################################
#
#    Techvaria Solutions Pvt. Ltd.
#
#    Copyright (C) 2025-Techvaria Solutions(<https://techvaria.com>)
#    Author: Techvaria Solutions Pvt. Ltd.(info@techvaria.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import fields, models, api


class ProductAttribute(models.Model):
    """ This class extends the 'product.attribute' model in Odoo.
        It adds custom field to check if file upload allowed."""
    _inherit = "product.attribute"

    is_file_upload_allowed = fields.Boolean(
        string='Allow File Upload?',
        help='If enabled, allows file upload in ecommerce cart page.'
    )

    @api.onchange('display_type')
    def _onchange_display_type(self):
        self.ensure_one()
        self.is_file_upload_allowed = False
