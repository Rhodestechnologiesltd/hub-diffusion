from odoo import models, fields, api, _


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    changed_sales_price = fields.Float(string='New SalesPrice', compute='_compute_price_unit', store=True)
    margin_percent = fields.Float("Selling Margin (%)")
    partner_id_margin_percentage = fields.Float(string='Customer Margin', related='order_partner_id.margin_percentage')

    @api.depends('product_id', 'product_uom', 'product_uom_qty', 'order_partner_id.margin_percentage')
    def _compute_price_unit(self):
        for line in self:
            if line.qty_invoiced > 0 or (line.product_id.expense_policy == 'cost' and line.is_expense):
                continue
            if not line.product_uom or not line.product_id:
                line.price_unit = 0.0
            else:
                line = line.with_company(line.company_id)
                line.changed_sales_price = line.purchase_price * (1 + line.order_partner_id.margin_percentage)
                line.price_unit = line.purchase_price * (1 + line.order_partner_id.margin_percentage)
