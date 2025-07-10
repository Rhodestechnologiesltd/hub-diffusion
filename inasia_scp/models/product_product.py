# -*- coding:utf-8 -*-

from odoo import api, fields, models


class Product(models.Model):
    _inherit = 'product.product'
    
    minimum_qty = fields.Float(string="MOQ")
    supplier_id = fields.Many2one('res.partner', string="Supplier")
    
    @api.depends('supplier_id')
    def update_supplier(self):
        self.product_tmpl_id.supplier_id = self.supplier_id.id
    
    
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    minimum_qty = fields.Float(string="MOQ")
    supplier_id = fields.Many2one('res.partner', string="Supplier")
    
    @api.depends('supplier_id')
    def update_supplier(self):
        self.product_variant_id.supplier_id = self.supplier_id.id