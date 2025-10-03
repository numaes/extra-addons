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
{
    'name': 'Website Order Attachments',
    'version': '19.0.1.0.1',
    'category': 'eCommerce',
    'author': 'Techvaria',
    'company': 'Techvaria',
    'maintainer': 'Techvaria',
    'website': "https://techvaria.com",
    'summary': 'Attribute-Driven File Attachments for eCommerce Orders.',
    'description': 'Customer can upload files for product extra options.'
                   'Attached files will be stored in Sale Order.'
                   'File naming will be updated acoording to product information.',
    'depends': [
        'website_sale', 'sale_management',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/attributes_views.xml',
        'views/line_attachment_views.xml',
        'views/sale_order_views.xml',
        'views/website_sale_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'ts_website_order_attachments/static/src/js/attachment.js',
        ],
    },
    'images': [
        'static/description/screen.jpg',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
