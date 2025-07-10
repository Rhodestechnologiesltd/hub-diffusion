# -*- coding: utf-8 -*-
# Part of Rhodes Technologies Ltd.

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    pc_sale = fields.Boolean(string='Update product prices when confirming SO')
    pc_manual = fields.Boolean(string='Record price change when changing manually')
    allow_manual_change = fields.Boolean(string='Allow changing prices manually')
