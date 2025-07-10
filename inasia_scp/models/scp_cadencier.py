# -*- coding:utf-8 -*-
# Part of Rhodes Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date
import json
# import random


class Cadencier(models.Model):
    _name = 'scp.cadencier'
    _description = 'Cadencier'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char("Description")
    # container_id = fields.Many2one('scp.container',"Container")
    supplier_id = fields.Many2one('res.partner', string="Supplier")
    order_line_ids = fields.One2many('sale.order.line', 'cadencier_id', string='Order Lines')