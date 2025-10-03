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

from odoo import models, fields


class LineAttachment(models.Model):
    _name = 'line.attachment'
    _inherits = {
        'ir.attachment': 'attachment_id',
    }
    _inherit = 'mail.thread'
    _description = 'Order Line Attachment'
    _rec_name = 'file_name'

    order_line_id = fields.Many2one(
        'sale.order.line',
        string='Line',
    )
    ptav_id = fields.Many2one(
        'product.template.attribute.value',
        string='Value',
    )
    attachment_id = fields.Many2one(
        'ir.attachment',
        string='File',
        ondelete="cascade",
        required=True
    )
    file_name = fields.Char(
        string='File Name',
        related='attachment_id.name'
    )
    order_id = fields.Many2one(
        'sale.order',
        string="Order",
        related='order_line_id.order_id'
    )

    def unlink(self):
        self.attachment_id.unlink()
        res = super().unlink()
        return res

    def action_download_attachment(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self.attachment_id.id}?download=true',
            'target': 'current',
        }
