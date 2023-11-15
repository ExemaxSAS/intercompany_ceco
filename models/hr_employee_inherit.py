# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    employee_cost_hour_ids = fields.One2many('employee.cost.hour.line', 'hr_employee_id', 'Costos hora') 
    hr_company_payment = fields.Selection([
        ('1', 'ITPROVIDER SRL'),
        ('2', 'ITPSONE MEXICO'),
        ('3', 'ITPS ONE LLC')
    ], string='Paga empresa')

    analytic_dis_id = fields.Many2one('account.analytic.tag', 'Distribución Analítica')

class IntercompanyEmployeeCost(models.Model):
    _name = 'employee.cost.hour.line'

    hr_cost_date = fields.Date('Fecha')
    hr_employee_es_rd = fields.Boolean('Es Relación de Dependencia') 
    hr_employee_id = fields.Many2one('hr.employee','Employee')

    hr_sueldo_facturado = fields.Float('Sueldos a distribuir')
    hr_contribuciones = fields.Float('Contribuciones a distribuir')    
    hr_honorario = fields.Float('Honorarios a distribuir')

    hr_sueldo_info = fields.Float('Sueldos')
    hr_usd = fields.Float('USD')
    hr_byout = fields.Float('Honorarios')
    hr_comisiones = fields.Float('Comisiones')
   # hr_total = fields.Float('Total')
    
   