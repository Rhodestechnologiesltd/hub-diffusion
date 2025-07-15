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


class SaleOrder(models.Model):
    _inherit = "sale.order"

    supplier_ids = fields.Many2many('res.partner', string='Suppliers')
    purchase_ids = fields.One2many('purchase.order', 'sale_id', string="Related PO")
    # supplier_invoice_id = fields.Many2one('purchase.order', string="Related PO")
    # supplier_invoice_ref = fields.Char(related="supplier_invoice_id.invoice_ref", string="Supplier CI")
    # supplier_incoterm_id = fields.Many2one('account.incoterms', related='supplier_id.incoterm_id')
    purchase_expected_arrival = fields.Date("Expected CRD")
    cargo_ready_date = fields.Date("CRD")
    loading_port = fields.Many2one('scp.port', "Port of Loading")
    discharge_port = fields.Many2one('scp.port', "Port of Discharge")
    departure_date = fields.Date("ETD")
    arrival_date = fields.Date("ETA")
    vessel_id = fields.Many2one('scp.vessel', "Vessel")
    container_num = fields.Char(string="Container No.")
    seal_num = fields.Char(string="Seal No.")
    shipping_mark = fields.Char(string="Shipping Mark")

    contact_person = fields.Many2one('res.partner', string="Contact Person")
    forwarder_id = fields.Many2one('res.partner', string="Forwarder")
    shipper_id = fields.Many2one('res.partner', string="Shipper")
    consignee_id = fields.Many2one('res.partner', string="Consignee")
    notify_id = fields.Many2one('res.partner', string="Notify")
    shipping_company_id = fields.Many2one('res.partner', string="Shipping Company")
    booking_num = fields.Char(string="Booking No.")
    freight = fields.Char(string="Freight")
    
    gross_weight = fields.Float(string="Gross Weight")
    net_weight = fields.Float(string="Net Weight")
    package = fields.Float(string="Package")
    order_qty = fields.Integer(string="Quantity")
    order_value = fields.Float(string="Total Value")
    
    qc_schedule = fields.Date(string="QC Schedule")
    loading_date = fields.Date(string="Loading Date")
    
    is_purchase_generated = fields.Boolean("RFQ Generated")
    is_purchase_confirmed = fields.Boolean("PO Confirmed")
    
    is_price_validated = fields.Boolean("Prices Confirmed")
    
    cadencier_state = fields.Selection([('stage1',"Stage 1"),
                                        ('stage2',"Stage 2"),
                                        ('stage3',"Stage 3"),
                                        ('stage4',"Stage 4"),
                                        ('stage5',"Stage 5")], string="Stages", default='stage1')
    
    is_lcl = fields.Boolean(string="LCL")
    container_type = fields.Selection([('lcl', "LCL"),
                                       ('fcl', "FCL")],
                                       string="Container Type")
    container_id = fields.Many2one('scp.container')
    available_volume = fields.Float(related="container_id.volume")
    actual_volume = fields.Float("Volume to fill", compute="_compute_actual_volume", store=True)
    container_capacity = fields.Float("Container Capacity", compute="_compute_container_capacity", store=True)
    
    cargo_desc = fields.Text("Cargo Description")
    
    order_line_count = fields.Integer(compute="_compute_order_line_count", store=True)
    comment = fields.Text("Comments and Instructions")
    
    
    @api.depends('order_line')
    def _compute_order_line_count(self):
        self.order_line_count = len(self.order_line)
        
    @api.depends('order_line')
    def _compute_actual_volume(self):
        volume = 0
        for rec in self:
            for line in rec.order_line:
                volume += line.volume
            rec.actual_volume = volume
    
    @api.depends('actual_volume')
    def _compute_container_capacity(self):
        # if self.id:
        #     if not self.container_id:
        #         raise ValidationError("No Container Selected!")
        for rec in self:
            try:
                capacity = rec.actual_volume/rec.available_volume
            except ZeroDivisionError:
                capacity = 0
            rec.container_capacity = capacity
            
    @api.model
    def create(self, vals):
        vals['comment'] = "Generate RFQ for suppliers"
        sale = super(SaleOrder, self).create(vals)
        return sale
        
    def split_order(self):
        for line in self.order_line:
            if line.supplier_id != self.supplier_id:
                order_vals = {
                    'partner_id': self.partner_id.id,
                    'supplier_id': line.supplier_id.id,
                }
                new_order = self.env['sale.order'].sudo().create(order_vals)
                
    
    def action_confirm_pricing(self):
        action = {
            'name': 'Confirm Pricing',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('inasia_scp.view_scp_sale_pricing_form').id,
            'res_id': self.id,
            'target': 'new',
        }
        return action
    
    def check_pricing_state(self):
        not_validated = self.env['sale.order.line'].sudo().search_count([('order_id', '=', self.id), ('pricing_state', '=', 'draft')])
        if not_validated == 0:
            self.is_price_validated = True
        
    def generate_purchase_order(self):
        for line in self.order_line:
            if line.supplier_id:
                supplier = line.supplier_id
                origin = self.name
                existing_purchase = self.env['purchase.order'].search([('partner_id','=', supplier.id),('state', 'in', ['draft','sent'])], limit=1)
                if existing_purchase:
                    for purchase in existing_purchase:
                        order = purchase
                else:
                    order_vals = {
                        'partner_id': supplier.id,
                        'sale_id': self.id,
                        'origin': origin
                    }
                    order = self.env['purchase.order'].sudo().create(order_vals)
                line_vals = {
                    'product_id': line.product_id.id,
                    'order_id': order.id
                }
                order_line = self.env['purchase.order.line'].sudo().create(line_vals)
                self.is_purchase_generated = True
                self.comment = "Confirm Supplier Pricing"
            else:
                raise ValidationError("No supplier set for %s" % line.product_id.name)
            
    def generate_purchase_order_shop(self):
        for line in self.order_line:
            # PO - Inasia buying from DongBo
            dongbo = self.env.ref('inasia_scp.scp_dongbo')
            inasia = self.env.ref('base.main_company')
            origin = self.name
            if line.supplier_id.is_shop:
                existing_purchase_dongbo = self.env['purchase.order'].search([('company_id', '=', self.env.ref('base.main_company').id),('partner_id','=', dongbo.partner_id.id),('state', 'in', ['draft'])], limit=1)
                if existing_purchase_dongbo:
                    for purchase in existing_purchase_dongbo:
                        order = purchase
                else:
                    order_vals = {
                        'company_id': self.env.ref('base.main_company').id,
                        'partner_id': dongbo.partner_id.id,
                        'sale_id': self.id,
                        'origin': origin
                    }
                    order = self.env['purchase.order'].sudo().create(order_vals)
                line_vals = {
                    'product_id': line.product_id.id,
                    'order_id': order.id
                }
                order_line = self.env['purchase.order.line'].sudo().create(line_vals)
                self.is_purchase_generated = True
                self.comment = "Confirm Supplier Pricing"
            # SO - Dongbo selling to Inasia
                existing_sale_dongbo = self.env['sale.order'].search([('company_id', '=', dongbo.id),('partner_id','=', inasia.partner_id.id),('state', 'in', ['draft'])], limit=1)
                if existing_sale_dongbo:
                    for sale in existing_sale_dongbo:
                        sale_order = sale
                else:
                    order_vals = {
                        'company_id': dongbo.id,
                        'partner_id': inasia.partner_id.id,
                        'origin': origin
                    }
                    sale_order = self.env['sale.order'].sudo().create(order_vals)
                line_vals = {
                    'product_id': line.product_id.id,
                    'order_id': sale_order.id
                }
                sale_order_line = self.env['sale.order.line'].sudo().create(line_vals)
                
            if line.supplier_id:
                supplier = line.supplier_id
                origin = self.name
                if supplier.is_shop:
                    company = self.env.ref('inasia_scp.scp_dongbo')
                else:
                    company = self.env.ref('base.main_company')
                existing_purchase = self.env['purchase.order'].search([('company_id', '=', company.id),('partner_id','=', supplier.id),('state', 'in', ['draft'])], limit=1)
                if existing_purchase:
                    for purchase in existing_purchase:
                        order = purchase
                else:
                    order_vals = {
                        'company_id': company.id,
                        'partner_id': supplier.id,
                        'sale_id': self.id,
                        'origin': origin
                    }
                    order = self.env['purchase.order'].sudo().create(order_vals)
                line_vals = {
                    'product_id': line.product_id.id,
                    'order_id': order.id
                }
                order_line = self.env['purchase.order.line'].sudo().create(line_vals)
                self.is_purchase_generated = True
            else:
                raise ValidationError("No supplier set for %s" % line.product_id.name)
    
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    supplier_id = fields.Many2one(related='product_template_id.supplier_id', string='Supplier')
    volume = fields.Float('Volume', compute='_compute_volume', store=True)
    pricing_state = fields.Selection([('draft', "Not Confirmed"),
                                      ('confirm', "Confirmed")],
                                     default='draft')
    
    @api.depends('product_template_id','product_uom_qty')
    def _compute_volume(self):
        for rec in self:
            rec.volume = rec.product_template_id.package_volume * rec.product_uom_qty
            rec.order_id._compute_actual_volume()
    
    @api.depends('product_template_id','product_uom_qty')
    def update_pricing_state(self):
        self.order_id.check_pricing_state()
    
    def action_validate(self):
        self.pricing_state = 'confirm'
        action = {
            'name': 'Confirm Pricing',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('inasia_scp.view_scp_sale_pricing_form').id,
            'res_id': self.order_id.id,
            'target': 'new',
        }
        return action
    
    
