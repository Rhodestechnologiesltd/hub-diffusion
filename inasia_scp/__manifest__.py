# -*- coding: utf-8 -*-
# Part of Rhodes Technologies.
{
    "name": "Inasia Supply Chain Platform",
    "author": "Khalid Joomun (Rhodes Technologies Ltd)",
    "website": "https://www.rhodesmea.com",
    "support": "khalid@rhodes.mu",
    "category": "Tools",
    "description": """Supply Chain Platform (SCP) for Inasia""",
    "version": "1.0.1",
    "depends": ["mail",
                "contacts",
                "calendar",
                "product",
                "sale_management",
                "purchase",
                "portal",],
    "data": [
        # "security/security.xml",
        "security/ir.model.access.csv",
        'data/company_data.xml',
        # "data/ir_cron_data.xml",
        # "data/mail_template.xml",
        # "data/paper_format.xml",
        # "views/menu.xml",
        # "views/scp_cart.xml",
        "views/res_partner.xml",
        "views/product_template.xml",
        "views/sale_order.xml",
        "views/purchase_order.xml",
        # "views/res_config_settings_inherit.xml",
        # "views/res_users_inherit.xml",
    ],
    'assets': {},
    "application": True,
    "installable": True,
    "auto_install": False,
}
