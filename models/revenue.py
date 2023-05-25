from odoo import models, fields, api
import datetime
import logging

_logger = logging.getLogger(__name__)

class RevenueInterco(models.Model):
    _name = 'revenue.interco'

    mes=fields.Selection([('1', 'Enero'),('2', 'Febrero'),('3','Marzo'),('4','Abril'),('5','Mayo'),('6','Junio'),
                          ('7','julio'),('8','Agosto'),('9','Septiembre'),('10','Octubre'),('11','Noviembre'),('12','Diciembre')],required=True)
    anio=fields.Integer('Año',required=True, store=True)
    periodo=fields.Char('Periodo',store=True,compute="_compute_periodo")
    pais=fields.Selection( [('ARG', 'Argentina'),
         ('MEX', 'Mexico'),('USA','USA')],required=True)
    totb1= fields.Float('Total B1',store=True)
    totmkt = fields.Float('Total MKT',store=True)
    totnt = fields.Float('Total NT',store=True)
    tots4 = fields.Float('Total S4',store=True)
    tottalentlatam = fields.Float('Total Talent Latam',store=True)
    tottalentusa = fields.Float('Total Talent USA',store=True)
    
    #guardo % para poder mostrar en vista pivot
    #los dejo en readonly porque permite editar valor
    total=  fields.Float('TOTAL Interco',  store=True)
    porc_B1 = fields.Float('% B1',store=False,compute="_comp_porcb1")
    porc_MKT = fields.Float('% MKT',store=False,compute="_comp_porcmkt")
    porc_NT = fields.Float('% NT',store=False,compute="_comp_porc_nt")
    porc_S4 = fields.Float('% S4',store=False,compute="_comp_porcs4")
    porc_talentlatam = fields.Float('% Talent Latam',store=False,compute="_comp_porc_tlatam")
    porc_talentusa = fields.Float('% Talent USA',store=False,compute="_comp_por_tusa")
    

    _sql_constraints = [('unique_revenue_mesaniopais', 'unique(mes, anio, pais)',
                         'Ya existe un registro para el período y pais seleccionado')]

    @api.depends('anio','mes')
    def _compute_periodo(self):
        for rec in self:
            if rec.anio:
                rec.periodo= rec.mes + ' '+ str(rec.anio)


    @api.onchange('totb1','totmkt','totnt','tots4','tottalentlatam','tottalentusa')
    def actu_porcentajes(self):
        total= self.totb1+ self.totmkt + self.totnt + self.tots4+ self.tottalentlatam + self.tottalentusa
      #  totalrg = self.totb1  + self.totnt + self.tots4 + self.tottalentlatam + self.tottalentusa
        if total>0:
            self.total=total
            self.porc_B1 = self.totb1  * 100/total
            self.porc_MKT= self.totmkt * 100/total
            self.porc_NT = self.totnt  * 100/total
            self.porc_S4 = self.tots4  * 100/total
            self.porc_talentusa  =self.tottalentusa * 100/total
            self.porc_talentlatam=self.tottalentlatam * 100/total


    def _comp_porcb1(self):
        for rec in self:
            total = rec.totb1 + rec.totmkt + rec.totnt + rec.tots4 + rec.tottalentlatam + rec.tottalentusa
            if total:
              rec.porc_B1 = rec.totb1 * 100 / total
            else:
                rec.porc_B1=0

    def _comp_porcmkt(self):
        for rec in self:
            total = rec.totb1 + rec.totmkt + rec.totnt + rec.tots4 + rec.tottalentlatam + rec.tottalentusa
            if total:
                rec.porc_MKT = rec.totmkt * 100 / total
            else:
                rec.porc_MKT=0

    def _comp_porc_nt(self):
        for rec in self:
            total = rec.totb1 + rec.totmkt + rec.totnt + rec.tots4 + rec.tottalentlatam + rec.tottalentusa
            if total:
                rec.porc_NT = rec.totnt * 100 / total
            else:
                rec.porc_NT = 0

    def _comp_porcs4(self):
        for rec in self:
            total = rec.totb1 + rec.totmkt + rec.totnt + rec.tots4 + rec.tottalentlatam + rec.tottalentusa
            if total:
                rec.porc_S4 = rec.tots4 * 100 / total
            else:
                rec.porc_S4=0

    def _comp_porc_tlatam(self):
        for rec in self:
            total = rec.totb1 + rec.totmkt + rec.totnt + rec.tots4 + rec.tottalentlatam + rec.tottalentusa
            if total:
                rec.porc_talentlatam = rec.tottalentlatam * 100 / total
            else:
                rec.porc_talentlatam=0

    def _comp_por_tusa(self):
        for rec in self:
            total = rec.totb1 + rec.totmkt + rec.totnt + rec.tots4 + rec.tottalentlatam + rec.tottalentusa
            if total:
                rec.porc_talentusa = rec.tottalentusa * 100 / total
            else:
                rec.porc_talentusa=0