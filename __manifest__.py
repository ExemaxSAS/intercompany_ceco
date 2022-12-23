# -*- coding:utf-8 -*-

{
    'name': 'Intercompany CECO',
    'version': '15.0',
    'depends': [
        'base', 'account', 'hr',
    ],
    'author': 'Gabriela Riquelme, Ignacio Buioli, Ivan Arriola - Exemax',
    'website': 'http://www.exemax.com.ar',
    'summary': 'Analítica de empresas vinculadas',
    'category': 'Extra Tools',
    'description': '''
    ''',
    'data': [
        'security/ir.model.access.csv',
        'views/account_intercompany_cost_view.xml',
        'views/hr_employee_inherit_view.xml',
        'views/account_account.xml',
        'views/resultados.xml',
        'views/revenue.xml',
        'views/template.xml',
        'views/resultados.xml',

    ],
}