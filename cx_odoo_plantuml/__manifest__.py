{
    "name": "Odoo UML PlantUML Export",
    "version": "14.0.1.0.0",
    "summary": "Export Odoo to UML PlantUML Module Diagram Structure",
    "author": "Cetmix, Ivan Sokolov",
    "maintainer": "Cetmix",
    "license": "LGPL-3",
    "category": "Extra Tools",
    "website": "https://cetmix.com",
    "live_test_url": "https://cetmix.com",
    "description": """
    Export Odoo Module Information diagram into to PlantUML UML
    """,
    'images': ['static/description/banner.png'],
    "depends": [
        "base_setup"
    ],
    'external_dependencies': {
    },
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/ir_module.xml",
        "views/res_config_settings.xml",
        "wizard/export_plantuml.xml",
    ],
    "installable": True,
    "application": True,
}
