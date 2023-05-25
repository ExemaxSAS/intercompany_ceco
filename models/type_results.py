from odoo import models, fields, api

class TypeResults(models.Model):
    _name = 'type.results'

    resultado=fields.Char('Resultado',required=True)
    grupo = fields.Many2many('intercompany.cost.groups', string='Grupo',required=True)
    subgrupo = fields.Many2many('intercompany.cost.subgroups',sring='SubGrupo')
    group_id = fields.Many2one('account.group' ,string="Tipo de cuenta contable")

    @api.onchange('grupo')
    def onchange_grupod(self):
        for rec in self:
            return {'domain': {'subgrupo': [('grupo_id', 'in', rec.grupo)]}}