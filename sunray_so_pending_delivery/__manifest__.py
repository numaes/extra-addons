{
    'name': 'Sale Pending Delivery | Sales Pending Dispatch',
    'version': '18.0.1.0.0',
    'summary': 'Shows sales orders and order lines that are pending for delivery in a fast, SQL-based report.',
    'description': """
        Show a Sale Pending Delivery Report.
        
        Features:
        - SQL View based report used for high performance.
        - Lists Sale Order Lines pending for delivery.
        - Grouped by Sale Order.
        - Restricted to sales users, honouring the multi-company and own-documents rules.
    """,
    'category': 'Sales',
    "author": "Sunray Datalinks Pvt. Ltd.",
    "website": "https://www.sunraydatalinks.com/",
    'depends': ['base', 'sale_management', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rules.xml',
        'views/pending_delivery_views.xml',

    ],
    "images": [
        "static/description/banner.gif",
        # "static/description/icon.png",
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
