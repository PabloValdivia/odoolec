# -*- coding: utf-8 -*-
{
    'name': "Ecuador Electronic Invoice",

    'summary': """
                This is a contribution to localize odoo in Ecuador
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "INGEINT SA",
    'website': "https://www.ingeint.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localization',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'account',
                'l10n_ec_par',
                'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/res_company_ei.xml',
        'views/res_partner.xml',
        'views/sri_authorization.xml',
        'views/sri_error_code.xml',
        'views/account_journal.xml',
        'views/account_move.xml',
        'views/sri_parameters.xml',
        'views/sri_tax_code.xml',
        'views/tax.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
