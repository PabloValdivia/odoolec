# -*- coding: utf-8 -*-
{
    'name': "Ecuador City",

    'summary': """
                This is a contribution to localize odoo in Ecuador
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Carlos Vizcaya",
    'website': "https://www.ingeint.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localization',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_country_city.xml',
        'views/res_partner.xml',
        'data/res_country.xml',
        'data/res.country.state.csv',
        'data/res.country.city.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
            ],
}
