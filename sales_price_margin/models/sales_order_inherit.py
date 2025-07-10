from odoo import models, fields, api, _


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order'

    partner_id_margin_percentage = fields.Float(string='Customer Margin', related='partner_id.margin_percentage')



