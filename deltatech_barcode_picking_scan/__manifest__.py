# ©  2008-2021 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

{
    "name": "Barcode Picking",
    "summary": "Add product in picking using barcode scanner",
    "version": "18.0.0.0.0",
    "author": "Terrabit, Voicu Stefan",
    "website": "https://www.terrabit.ro",
    "support": "odoo@terrabit.ro",
    "category": "Inventory",
    "depends": ["stock", "barcodes"],
    "license": "OPL-1",
    "data": [
        "views/picking_views.xml",
    ],
    "images": ["static/description/main_screenshot.png"],
    "development_status": "Production/Stable",
    "maintainers": ["VoicuStefan2001"],
}
