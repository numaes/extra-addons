from odoo import models, fields, tools

class PendingDeliveryReport(models.Model):
    _name = "sunray.pending.delivery.report"
    _description = "Sale Pending Delivery Report"
    _auto = False
    _rec_name = 'order_id'
    _order = 'date_order desc'

    order_id = fields.Many2one('sale.order', string="Sale Order", readonly=True)
    partner_id = fields.Many2one('res.partner', string="Customer", readonly=True)
    date_order = fields.Datetime(string="Order Date", readonly=True)
    product_id = fields.Many2one('product.product', string="Product", readonly=True)
    product_uom_qty = fields.Float(string="Ordered Quantity", readonly=True)
    qty_delivered = fields.Float(string="Delivered Quantity", readonly=True)
    qty_pending = fields.Float(string="Pending Quantity", readonly=True)
    currency_id = fields.Many2one('res.currency', string="Currency", readonly=True)
    price_unit = fields.Float(string="Unit Price", digits='Product Price', readonly=True)
    price_subtotal = fields.Monetary(string="Subtotal (Tax Excl.)", readonly=True)
    price_total = fields.Monetary(string="Subtotal (Tax Incl.)", readonly=True)
    price_subtotal_pending = fields.Monetary(string="Pending Subtotal (Tax Excl.)", readonly=True)
    user_id = fields.Many2one('res.users', string="Salesperson", readonly=True)
    company_id = fields.Many2one('res.company', string="Company", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    l.id as id,
                    l.order_id as order_id,
                    s.partner_id as partner_id,
                    s.date_order as date_order,
                    l.product_id as product_id,
                    l.product_uom_qty as product_uom_qty,
                    l.qty_delivered as qty_delivered,
                    (l.product_uom_qty - l.qty_delivered) as qty_pending,
                    l.currency_id as currency_id,
                    l.price_unit as price_unit,
                    l.price_subtotal as price_subtotal,
                    l.price_total as price_total,
                    -- Prorated from the line subtotal so discounts and tax-included prices carry over
                    l.price_subtotal * (l.product_uom_qty - l.qty_delivered)
                        / NULLIF(l.product_uom_qty, 0) as price_subtotal_pending,
                    s.user_id as user_id,
                    l.company_id as company_id
                FROM
                    sale_order_line l
                    JOIN sale_order s ON (l.order_id = s.id)
                WHERE
                    s.state = 'sale'
                    AND l.product_uom_qty > l.qty_delivered
                    AND l.display_type IS NULL
            )
        """ % self._table)
