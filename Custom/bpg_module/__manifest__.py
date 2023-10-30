# -*- coding: utf-8 -*-
{
    'name': "BPG Module",

    'summary': """
        Visit dan vetting kapal""",

    'description': """
        Form ini diisi oleh Karyawan BPG
    """,

    'author': "Alwan",
    'website': "https://barokahperkasagroup.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','shipping','hr'],

    # always loaded
    'data': [
        'security/bpg_security.xml',
        'security/ir.model.access.csv',
        'views/visit_management_view.xml',
        'views/finding.xml',
        'views/list_items.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
