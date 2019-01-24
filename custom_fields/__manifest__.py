# -*- coding: utf-8 -*-
{
    'name': "Custom Fields",

    'summary': """
        Creates a custom field in Quotes, Purchase and Invoice""",

    'description': """
        Creates a custom field in Quotes, Purchase and Invoice 
    """,

    'author': "Linescripts Softwares Pvt.Ltd.",
    'website': "http://www.linescripts.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'purchase', 'account', 'crm', 'sale_crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}