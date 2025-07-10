# -*- coding:utf-8 -*-
# Part of Rhodes Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date


class Port(models.Model):
    _name = 'scp.port'
    _description = 'Ports'
    
    name = fields.Char("Title")
    country_id = fields.Many2one('res.country', "Country")