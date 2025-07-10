from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.model
    def action_confirm(self):
        confirm = super(SaleOrder, self).action_confirm()
        if self.company_id.pc_sale:
            for line in self.order_line:
                line.product_id.list_price = line.price_unit
        return confirm

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    previous_selling_price = fields.Float(string='Previous Selling Price', compute='_compute_previous_selling_price')
    price_change = fields.Selection([('increase', 'Increase'), ('decrease', 'Decrease')],
                                    string='Price Change')

    @api.depends('product_id','price_unit')
    def _compute_previous_selling_price(self):
        for line in self:
            previous_price_change = self.env['product.price.change'].search([
                ('product_id', '=', line.product_id.id),
                ('change_type', '=', 'sale_price')
            ], limit=1, order='change_date desc')
            if previous_price_change:
                line.previous_selling_price = previous_price_change.old_list_price
                if previous_price_change.old_list_price > line.price_unit:
                    line.price_change = 'decrease'
                elif previous_price_change.old_list_price < line.price_unit:
                    line.price_change = 'increase'
            else:
                line.previous_selling_price = 0

    def action_open_price_change(self):
        return {
            'name': 'Price Changes',
            'type': 'ir.actions.act_window',
            'res_model': 'product.price.change',
            'view_mode': 'tree',
            'domain': [('product_id', 'in', self.mapped('product_id.id')), ('change_type', '=', 'sale_price')],
            'context': self.env.context,
            'view_id': self.env.ref("price_change.view_sale_product_price_change_tree").id,
            'target': 'new'
        }
