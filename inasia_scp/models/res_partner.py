# -*- coding:utf-8 -*-

from odoo import api, fields, models


class Contacts(models.Model):
    _inherit = 'res.partner'
    
    incoterm_id = fields.Many2one('account.incoterms')
    supplier_category_id = fields.Many2one('scp.supplier.category')
    
    has_export_licence = fields.Boolean("Export Licence")
    business_licence = fields.Char("Business Licence")
    delivery_time = fields.Integer("Delivery Time")
    shop_num = fields.Char("Shop No.")
    is_shop = fields.Boolean("Is a shop")
    
    supplier_licence = fields.Binary("Supplier Licence")