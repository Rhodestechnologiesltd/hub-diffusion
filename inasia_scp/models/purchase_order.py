# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import random
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.http import request
from odoo.osv import expression
from odoo.tools import float_is_zero


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sale_id = fields.Many2one('sale.order', string="Related SO")
    invoice_ref = fields.Char("Invoice Ref.")
    supplier_proforma = fields.Binary("Supplier PI")
    supplier_invoice = fields.Binary("Supplier Invoice")
    
    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")
    
    def action_confirm_pricing(self):
        action = {
            'name': 'Confirm Pricing',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('inasia_scp.view_scp_purchase_pricing_form').id,
            'res_id': self.id,
            'target': 'new',
        }
        return action
    
    
class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    
    pricing_state = fields.Selection([('draft', "Not Confirmed"),
                              ('confirm', "Confirmed")],
                             default='draft')
    
    def action_validate(self):
        self.pricing_state = 'confirm'
        action = {
            'name': 'Confirm Pricing',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('inasia_scp.view_scp_purchase_pricing_form').id,
            'res_id': self.order_id.id,
            'target': 'new',
        }
        return action