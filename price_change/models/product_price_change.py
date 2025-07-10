from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class ProductPriceChange(models.Model):
    _name = 'product.price.change'
    _description = 'Product Price Change'

    product_id = fields.Many2one('product.template', string='Product', required=True, ondelete='cascade')
    old_list_price = fields.Float(string='Old Selling Price')
    new_list_price = fields.Float(string='New Selling Price')
    old_standard_price = fields.Float(string='Old Buying Price')
    new_standard_price = fields.Float(string='New Buying Price')
    change_date = fields.Datetime(string='Change Date', required=True, default=fields.Datetime.now)
    change_type = fields.Selection(
        [('sale_price', 'Sale Price Change'), ('buying_price', 'Buying Price Change')],
        string='Change Type',
        required=True
    )
    value_change = fields.Selection(
        [('increase', 'Increase'), ('decrease', 'Decrease')],
        string='Value Change',
    )
    user_id = fields.Many2one('res.users', string='Changed By', required=True, default=lambda self: self.env.user)

