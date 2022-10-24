# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    employee_cost_hour_ids = fields.One2many('employee.cost.hour.line', 'hr_employee_id', 'Costos hora') 

class IntercompanyEmployeeCost(models.Model):
    _name = 'employee.cost.hour.line'

    hr_cost_date = fields.Date('Fecha')
    hr_sueldo_facturado = fields.Float('Sueldo/Facturado')
    hr_contribuciones = fields.Float('Contribuciones')
    hr_employee_id = fields.Many2one('hr.employee','Employee')