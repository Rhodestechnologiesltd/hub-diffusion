# -*- coding: utf-8 -*-
# Part of Rhodes Technologies Ltd.

from odoo import models, fields, api


class PriceChangeSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    pc_sale = fields.Boolean(string='Update product prices when confirming SO', related='company_id.pc_sale', readonly=False)
    pc_manual = fields.Boolean(string='Record price change when changing manually', related='company_id.pc_manual', readonly=False)
    allow_manual_change = fields.Boolean(string='Allow changing prices manually', related='company_id.allow_manual_change', readonly=False)
