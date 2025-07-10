# -*- coding: utf-8 -*-
# Part of Rhodes Technologies.

from odoo import models, fields, api


class Settings(models.TransientModel):
    _inherit = 'res.config.settings'