# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class AccountAnalyticTag(models.Model):
    _inherit = 'account.analytic.tag'

    employee_id = fields.Many2one('hr.employee','Empleado')

    @api.model
    def create(self, values):
        res = super(AccountAnalyticTag, self).create(values)
        total = 0
        for line in res.analytic_distribution_ids:
            total = total + line.percentage
        # #if total != 100:
        # #    raise ValidationError(str(total)+ ' La Distribucion debe sumar 100')
        # if res.active_analytic_distribution:
        #     res.name = self.env['ir.sequence'].next_by_code('dis.analytic') or '/'
        return res