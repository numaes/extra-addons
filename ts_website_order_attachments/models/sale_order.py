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

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    attachments_count = fields.Integer(
        string='Attachments',
        compute='_compute_attachments_count')

    def _compute_attachments_count(self):
        """Total No. of attachments"""
        for rec in self:
            rec.attachments_count = self.env['line.attachment'].search_count(
                [('order_line_id', 'in', rec.order_line.ids)])

    def action_open_line_attachments(self):
        action = self.env['ir.actions.actions']\
            ._for_xml_id('ts_website_order_attachments.action_line_attachment')
        action['context'] = {
            'create': 0,
            'edit': 0,
            'delete': 0,
            'duplicate': 0,
            'search_default_groupby_orderline': 1,
        }
        action['domain'] = [('order_line_id', 'in', self.order_line.ids)]
        return action
