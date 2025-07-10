from odoo import models, fields, api, _


class PartnerInherit(models.Model):
    _inherit = 'res.partner'

    margin_percentage = fields.Float(string="Margin")

