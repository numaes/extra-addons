{
    'name': "Toll Sync",
    'category': 'Human Resources/Fleet',
    'version': "14.0.3",
    'summary': "Manage your road tolls",
    'license': "AGPL-3",
    'author': "Tollsync.eu",
    'website': "https://tollsync.eu",
    'images': ['static/description/tls_thumb.jpg'],
    'depends': [
        'base',
        'fleet',
        'account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/tollsync_service.xml',
        'data/tollsync_data.xml',
        'views/assets.xml',
        'views/tls_toll.xml',
        'views/fleet_vehicle.xml',
        'views/res_config_settings.xml'
    ],
    'qweb': [
        'static/src/xml/toll_tree_button.xml',
        'static/src/xml/widgets.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}
