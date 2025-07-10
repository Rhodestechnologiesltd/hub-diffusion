# -*- coding:utf-8 -*-
# Part of Rhodes Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date
import json
# import random


class SupplierCategory(models.Model):
    _name = 'scp.supplier.category'
    _description = 'Supplier Category'
    
    name = fields.Char("Title")
    margin = fields.Float("Margin")