    #  -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Price Change',
    'version' : '1.0',
    'summary': 'Price change log',
    'sequence': -20,
    'description': "Price change log",
    'category': 'Inventory',
    'website': 'https://rhodesemea.com/',
    'depends': ['product','sale','stock'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/res_config_settings_view.xml',
        'views/price_change_view.xml',
        'views/sale_order_view.xml',
        # 'views/price_change.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
