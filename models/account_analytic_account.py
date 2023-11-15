# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.model
    # def create(self, values):
    #     res = super(AccountAnalyticAccount, self).create(values)
    #     name = str(res.aa_company.code) + '-' + str(res.aa_department.code) + '-' + str(res.aa_linepl.code) + '-' + str(res.aa_unit.code) + '-' + str(res.aa_cost.code) + '-' + str(res.aa_region.code) + '-' + str(res.aa_pais.code)
    #     n = self.env['account.analytic.account'].search([('name', '=', name)])
    #     if n:
    #         raise ValidationError('Ya existe una cuenta analítica con este nombre.')
    #     res.name = str(res.aa_company.code) + '-' + str(res.aa_department.code) + '-' + str(res.aa_linepl.code) + '-' + str(res.aa_unit.code) + '-' + str(res.aa_cost.code) + '-' + str(res.aa_region.code) + '-' + str(res.aa_pais.code)

    #     return res
    def create(self, values):
        res = super(AccountAnalyticAccount, self).create(values)
        name = (
        str(res.aa_company.code) + '-' +
        str(res.aa_department.code) + '-' +
        str(res.aa_linepl.code) + '-' +
        str(res.aa_unit.code) + '-' +
        str(res.aa_cost.code)
        )
        if res.aa_region:
            name += '-' + str(res.aa_region.code)

        if res.aa_pais:
            name += '-' + str(res.aa_pais.code)

        n = self.env['account.analytic.account'].search([('name', '=', name)])
        if n:
            raise ValidationError('Ya existe una cuenta analítica con este nombre.')
        res.name = name

        return res


    @api.onchange('aa_company', 'aa_department', 'aa_unit', 'aa_linepl', 'aa_cost', 'aa_region', 'aa_pais')
    def change_name(self):
        if not self.aa_pais:
            self.aa_pais = ""
            self.name = str(self.aa_company.code) + '-' + str(self.aa_department.code) + '-' + str(self.aa_linepl.code) + '-' + str(self.aa_unit.code) + '-' + str(self.aa_cost.code) + '-' + str(self.aa_region.code)
        elif not self.aa_region and not self.aa_pais:
            self.name = str(self.aa_company.code) + '-' + str(self.aa_department.code) + '-' + str(self.aa_linepl.code) + '-' + str(self.aa_unit.code) + '-' + str(self.aa_cost.code)
        elif self.aa_pais and not self.aa_region:
            self.name = str(self.aa_company.code) + '-' + str(self.aa_department.code) + '-' + str(self.aa_linepl.code) + '-' + str(self.aa_unit.code) + '-' + str(self.aa_cost.code) + '-' + str(self.aa_pais.code)
        else:
            self.name = str(self.aa_company.code) + '-' + str(self.aa_department.code) + '-' + str(self.aa_linepl.code) + '-' + str(self.aa_unit.code) + '-' + str(self.aa_cost.code)

    # @api.onchange('analytic_type')
    # def group_change(self):
    #     if self.analytic_type == 'gasto':
    #         group = self.env['account.analytic.group'].search([('name', '=', 'Gastos')], limit=1)
    #         self.group_id = group.id
    #     elif self.analytic_type == 'costo':
    #         group = self.env['account.analytic.group'].search([('name', '=', 'Costos')], limit=1)
    #         self.group_id = group.id
        
    name = fields.Char('Nombre', required=False)
    aa_company = fields.Many2one('aa.account.company', 'Empresa')
    aa_department = fields.Many2one('aa.account.department', 'Departamento')
    aa_unit = fields.Many2one('aa.account.unit', 'Unidad Operativa')
    aa_linepl = fields.Many2one('aa.account.linepl', 'Línea P&L')
    aa_cost = fields.Many2one('aa.account.cost', 'CENTRO  Costo - Cuenta Analítica')
    aa_region = fields.Many2one('aa.account.region', 'Region')
    aa_pais = fields.Many2one('aa.account.pais', 'Pais')
    aa_linepl_code = fields.Char(related='aa_linepl.code', string='Código de Línea de Producto', readonly=True)
    # parent_account = fields.Many2one('parent.account', 'Cuenta Padre')

    # analytic_type = fields.Selection([('gasto', 'Gasto Administrativo'), ('costo', 'Costo Operaciones')], string='Analytic Type')
    # account_type = fields.Selection([('view', 'Vista'), ('analytic', 'Cuenta Analítica'), ('project', 'Proyecto'), ('template', 'Template')], string='Tipo de Cuenta')