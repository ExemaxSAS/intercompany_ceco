# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
class AccountAccount(models.Model):
    _inherit='account.account'

    #area_uniope=fields.Selection(selection='_get_selection', string='Area/Unidad Operativa')
    grupo=  fields.Many2one('intercompany.cost.groups','Grupo')
    subgrupo =fields.Many2one('intercompany.cost.subgroups','SubGrupo')
    area = fields.Many2one('hr.department', 'Area')
    unidad_operativa = fields.Many2one('hr.employee.add.category', 'Unidad Operativa')
    tipo_cuenta= fields.Selection([ ('sueldo', 'Cuenta sueldo'),('honorario', 'Cuenta honorario'),('contribucion', 'Cuenta contribucion')],'Tipo cuenta')
    pais = fields.Selection([('MEX','MEX'),('USA','USA'),('ARG','ARG')],'Pais')

    _sql_constraints = [('unique_account_areauoptipo', 'unique(area, unidad_operativa, tipo_cuenta,pais)',
                         'Ya se designó una cuenta contable al Area-Unidad Operativa para el tipo de cuenta seleccionado')]

    @api.onchange('grupo')
    def onchange_grupod(self):
        for rec in self:
            return {'domain': {'subgrupo': [('grupo_id', '=', rec.grupo.id)]}}

class AccountIntercompanyCost2(models.Model):
    _inherit = 'account.intercompany.cost'

    _sql_constraints = [('unique_icperiodo', 'check(1=1)', 'No error'),]

class AccountIntercompanyCost2(models.Model):
    _inherit = 'intercompany.cost.line'

    _sql_constraints = [('unique_icperiodo', 'check(1=1)', 'No error'),]

