# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class AccountIntercompanyCost(models.Model):
    _name = 'account.intercompany.cost'
    _description = 'Costo entre empresas'

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('post', 'Publicado')
    ], 'Estado', default = 'draft')
    name = fields.Char('Nombre', required=True)
    date_from = fields.Date('Fecha desde', required=True)
    date_to = fields.Date('Fecha hasta', required=True)
    responsible_user = fields.Many2one('res.users','Responsable', required=True)
    analytic_line_ids = fields.Many2many('account.analytic.line', 'Cuentas analíticas', compute='_compute_analytic_line')

    @api.depends('date_from', 'date_to')
    def _compute_analytic_line(self):
        aline_ids = self.env['account.analytic.line'].search([('employee_id','!=',False),('date','>=', self.date_from),('date','<=', self.date_to)])
        self.analytic_line_ids = aline_ids

    def post_intercompany_cost(self):
        responsible_user = self.env.user
        