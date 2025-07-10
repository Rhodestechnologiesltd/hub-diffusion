# -*- coding:utf-8 -*-
# Part of Rhodes Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date


class Vessel(models.Model):
    _name = 'scp.vessel'
    _description = 'Vessels'
    
    name = fields.Char("Name")