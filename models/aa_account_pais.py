# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class AAAccountPais(models.Model):
    _name = 'aa.account.pais'

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.code) + ' - ' + str(record.name)))
        return result

    name = fields.Char('Nombre')
    code = fields.Char('Código')