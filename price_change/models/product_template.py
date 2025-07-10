from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    price_change_ids = fields.One2many('product.price.change', 'product_id', string='Price Changes')

    @api.model
    def create(self, vals):
        record = super(ProductTemplate, self).create(vals)
        self._check_price_changes(record, vals)
        return record

    def write(self, vals):
        for record in self:
            old_list_price = record.list_price
            old_standard_price = record.standard_price
            super(ProductTemplate, self).write(vals)
            self._check_price_changes(record, vals, old_list_price, old_standard_price)
        return True

    def _check_price_changes(self, record, vals, old_list_price=None, old_standard_price=None):
        if old_list_price is None:
            old_list_price = record.list_price
        
        if old_standard_price is None:
            old_standard_price = record.standard_price

        new_list_price = vals.get('list_price', old_list_price)
        new_standard_price = vals.get('standard_price', old_standard_price)

        # Check for list price change (for both sales and inventory)
        if old_list_price != new_list_price:
            value_change = 'decrease' if old_list_price > new_list_price else 'increase'
            self._create_price_change_record(
                record.id,
                old_list_price,
                new_list_price,
                None,  # No buying price in sales context
                None,  # No buying price in sales context
                'sale_price',
                value_change
            )

        # Check for standard price change (only for inventory)
        if old_standard_price != new_standard_price:
            value_change = 'decrease' if old_standard_price > new_standard_price else 'increase'
            self._create_price_change_record(
                record.id,
                old_list_price,
                new_list_price,
                old_standard_price,
                new_standard_price,
                'buying_price',
                value_change
            )

    def _create_price_change_record(self, product_id, old_list_price, new_list_price, old_standard_price, new_standard_price, change_type, value_change=None):
        self.env['product.price.change'].sudo().create({
            'product_id': product_id,
            'old_list_price': old_list_price,
            'new_list_price': new_list_price,
            'old_standard_price': old_standard_price,
            'new_standard_price': new_standard_price,
            'change_date': fields.Datetime.now(),
            'change_type': change_type,
            'value_change': value_change,
            'user_id': self.env.user.id
        })
