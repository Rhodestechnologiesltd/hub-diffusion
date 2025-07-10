# -*- coding:utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    minimum_qty = fields.Float(string="MOQ")
    supplier_id = fields.Many2one('res.partner', string="Supplier")
    is_shop = fields.Boolean("Procured from Shop", related='supplier_id.is_shop')
    package_volume = fields.Float("CBM (m3)", compute="_compute_package_volume", store=True)
    pcb = fields.Integer("PCB", default=1)
    
    @api.depends('volume','pcb')
    def _compute_package_volume(self):
        for rec in self:
            pkg_volume = rec.pcb * rec.volume
            rec.package_volume = pkg_volume