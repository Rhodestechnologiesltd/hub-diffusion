# -*- coding: utf-8 -*-
{
    'name': 'sales_price_margin',
    'version': '1.0',
    'category': 'sales_price_margin',
    'summary': 'sales_price_margin',
    'description': 'Sales_price',
    'author': 'Priya Sethuraman',
    'depends': ['sale', 'sale_management','sale_stock', 'sale_margin'],
    'data': [
        'views/res_partner_inherit.xml',
        'views/sale_order_line_inherit.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': '-100',
    'license': 'LGPL-3'
}
