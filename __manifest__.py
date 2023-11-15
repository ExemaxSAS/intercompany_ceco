# -*- coding:utf-8 -*-

{
    'name': 'Intercompany CECO',
    'version': '15.0',
    'depends': [
        'base', 'account', 'hr',
    ],
    'author': 'Gabriela Riquelme, Ignacio Buioli, Ivan Arriola, Israel Perez - Exemax',
    'website': 'http://www.exemax.com.ar',
    'summary': 'Analítica de empresas vinculadas',
    'category': 'Extra Tools',
    'description': '''
    ''',
    'data': [
        'views/account_intercompany_cost_view.xml',
        'views/hr_employee_inherit_view.xml',
        'views/account_account.xml',
        'views/resultados.xml',
        'views/revenue.xml',
        'views/template.xml',
        'views/account_analytic_account.xml',
        'views/aa_account_company.xml',
        'views/aa_account_department.xml',
        'views/aa_account_unit.xml',
        'views/aa_account_linepl.xml',
        'views/aa_account_cost.xml',
        'views/aa_account_region.xml',
        'views/aa_account_pais.xml',
        'views/account_analytic_tag_inherit.xml',
	    'data/params.xml',
	    'data/rules.xml',        
        'security/ir.model.access.csv',
    ],
}
