# ©  2008-2021 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from odoo import _, models


class Picking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "barcodes.barcode_events_mixin"]

    def _add_product(self, product, qty=1.0):
        existing_line = self.move_ids_without_package.filtered(lambda r: r.product_id.id == product.id)
        if existing_line:
            existing_line.product_uom_qty += qty
            message = _("The %(product_name)s product quantity was set to %(product_qty)s") % {
                "product_name": product.name,
                "product_qty": existing_line.product_uom_qty,
            }
            res = {"warning": {"title": _("Info"), "type": "notification", "message": message}}
        else:
            vals = {
                "picking_id": self.id,
                "product_id": product.id,
                "product_uom_qty": qty,
                "name": product.display_name,
            }
            self.move_ids_without_package.new(vals)
            message = _("The %s product was added") % (product.name)
            res = {"warning": {"title": _("Info"), "type": "notification", "message": message}}
        return res

    def on_barcode_scanned(self, barcode):
        if self.state != "draft":
            message = _("Status does not allow scanning")
            res = {"warning": {"title": _("Error"), "type": "danger", "message": message}}

            return res

        product = self.env["product.product"].search([("barcode", "=", barcode)])
        if not product:
            product = self.env["product.product"].search([("default_code", "=", barcode)])
        if product:
            res = self._add_product(product)
        else:
            message = _("There is no product with barcode or internal reference %s") % barcode
            res = {"warning": {"title": _("Error"), "type": "danger", "message": message}}

        return res
