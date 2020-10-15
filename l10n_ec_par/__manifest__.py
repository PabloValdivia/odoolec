# -*- coding: utf-8 -*-
{
    'name': "Ecuador Localization",

    'summary': """
        This is a contribution to localize odoo in Ecuador """,

    'description': """
        Tax Payer Types
        Tax ID Types
        RUC Validation
        Standard Ecuador fields
    """,

    'author': "Orlando Curieles - Osiris Roman",
    'website': "http://www.ingeint.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localization',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'mail',
                'contacts'
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/company.xml',
        'views/partner.xml',
        'data/payertype_data.xml'
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
