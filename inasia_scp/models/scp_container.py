# -*- coding:utf-8 -*-
# Part of Rhodes Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date
import json
# import random


class Container(models.Model):
    _name = 'scp.container'
    _description = 'Container'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char("Title")
    volume = fields.Float("Volume")