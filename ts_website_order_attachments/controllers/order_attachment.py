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
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers import main
import base64


class OrderAttachments(main.WebsiteSale):

    @http.route('/shop/add_attachments',
                type='http', auth='public', website=True,
                sitemap=False)
    def add_shop_attachments(self, **post):
        """To add attachment from websites"""
        order = post.get('order')
        main_button_href = post.get('main_button_href')
        attachments = {k: v for k,
                       v in post.items() if k.startswith('attachment')}
        for name, attachment in attachments.items():
            full_name = self.parse_attachment_string(name)
            line_id = full_name.get('line')
            pval_id = full_name.get('pval')
            if full_name and attachment.filename:
                attachment_id = request.env['ir.attachment'].sudo().create({
                    'name':
                        f"Attachment_Product_{full_name.get('product', '')}\
                        _Value_{full_name.get('ptav', '')}",
                    'description': attachment.filename,
                    'type': 'binary',
                    'res_model': 'sale.order',
                    'res_id': int(order),
                    'datas': base64.b64encode(attachment.read()),
                })
                if line_id:
                    request.env['line.attachment'].sudo().create({
                        'order_line_id': int(line_id),
                        'attachment_id': attachment_id.id,
                        'ptav_id': int(pval_id),
                    })
        return request.redirect(main_button_href)

    def parse_attachment_string(self, attachment_string):
        """
        Parse attachment format: attachment_{line_id}_{pval_id}_{name}_{value}
        Args:
            attachment_string (str): format "attachment_1_12_test_option"
        Returns:
            dict: Dict containing line_id, pval_id, product name, ptav name
        """
        parts = attachment_string.split('_')
        if len(parts) != 5:
            return False
        return {
            'line': parts[1],
            'pval': parts[2],
            'product': parts[3],
            'ptav': parts[4]
        }

    @http.route('/shop/attachments', type='jsonrpc', auth='public',
                website=True, sitemap=False)
    def shop_attachments(self, **post):
        """For delete the attachment from order line"""
        attachment = request.env['line.attachment'].sudo().browse(int(post.get(
            "attachment_id")))
        attachment.unlink()
        return True
