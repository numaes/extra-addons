# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.
{
    'name': 'Catch Weight Management',
    'version': '14.0.0.0',
    'sequence': 1,
    'category': 'Warehouse',
    'summary': 'Catch Weight Management',
    'description': """
    This module is for activating Catch weight management
""",
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'website': 'http://www.technaureus.com/',
    'price': 0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'depends': [
        'sale'
    ],
    'data': [
        'security/catch_weight_security.xml',
        'views/res_config_settings_views.xml',
        'views/product_views.xml',

    ],
    'images': ['images/main_screenshot.gif'],
    'installable': True,
    'auto_install': False,
    'application': True
}
