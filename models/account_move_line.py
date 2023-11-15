# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit='account.move.line'

    grupo_id= fields.Many2one('intercompany.cost.groups',string='Grupo costo', compute="_search_grupo_account", store=True)
    subgrupo_id = fields.Many2one('intercompany.cost.subgroups', string='Subgrupo costo', compute="_search_subgrupo_account", store=True)

    def _search_grupo_account(self):
        for rec in self:
            _logger.info('CUENTAS id:' + str(rec.account_id.id))
            account= self.env['account.account'].search([('id','=',rec.account_id.id)])
            if account:
                _logger.info('CUENTAS:' + str(account))
                rec.grupo_id=account.grupo

    def _search_subgrupo_account(self):
        for rec in self:
            account = self.env['account.account'].search([('id', '=', rec.account_id.id)])
            if account:
                rec.subgrupo_id = account.subgrupo
