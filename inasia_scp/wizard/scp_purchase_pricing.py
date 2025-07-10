# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PurchasePricing(models.TransientModel):
    _name = 'scp.purchase.pricing'

    name = fields.Char("Title")
