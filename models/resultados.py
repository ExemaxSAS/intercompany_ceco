from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

grupo_GGRG= 10

class TypeResults(models.Model):
    _name = 'type.results'

    resultado=fields.Char('Resultado',required=True)
    grupo = fields.Many2many('intercompany.cost.groups', string='Grupo',required=True)

class ResultadosInterco(models.Model):
    _name = 'resultados.interco'

    mes = fields.Selection(
                [('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'),
                 ('7', 'julio'), ('8', 'Agosto'), ('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'),
                 ('12', 'Diciembre')])
    anio = fields.Integer('Año', required=True, store=True)

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('checkpoint', 'Checkpoint'),
        ('post', 'Publicado')
    ], 'Estado', default='draft')

    revenue_interco_total= fields.Float('Costos Interco', store=False, compute="calc_revenue")
    revenue_interco_usa = fields.Float('Costos Interco USA', store=False, compute="calc_revenue_usa")
    revenue_interco_mex = fields.Float('Costos Interco MEX', store=False, compute="calc_revenue_mex")
    revenue_interco_arg = fields.Float('Costos Interco ARG', store=False, compute="calc_revenue_arg")

    revenue_b1_usa= fields.Float('Costos Interco B1 USA', store=False, compute="calc_revenue_b1_usa")
    revenue_b1_mex = fields.Float('Costos Interco B1 MEX', store=False, compute="calc_revenue_b1_mex")
    revenue_b1_arg = fields.Float('Costos Interco B1 ARG', store=False,compute="calc_revenue_b1_arg")

    revenue_nt_usa = fields.Float('Costos Interco NT USA', store=False, compute="calc_revenue_nt_usa")
    revenue_nt_mex = fields.Float('Costos Interco NT MEX', store=False,compute="calc_revenue_nt_mex")
    revenue_nt_arg = fields.Float('Costos Interco NT ARG', store=False,compute="calc_revenue_nt_arg")

    revenue_mkt_usa = fields.Float('Costos Interco MKT USA', store=False, compute="calc_revenue_mkt_usa")
    revenue_mkt_mex = fields.Float('Costos Interco MKT MEX', store=False,compute="calc_revenue_mkt_mex")
    revenue_mkt_arg = fields.Float('Costos Interco MKT ARG', store=False,compute="calc_revenue_mkt_arg")

    revenue_s4_usa = fields.Float('Costos Interco S4 USA', store=False, compute="calc_revenue_s4_usa")
    revenue_s4_mex = fields.Float('Costos Interco S4 MEX', store=False, compute="calc_revenue_s4_mex")
    revenue_s4_arg = fields.Float('Costos Interco S4 ARG', store=False, compute="calc_revenue_s4_arg")

    revenue_tlatam_usa = fields.Float('Costos Interco TALENT LATAM USA', store=False, compute="calc_revenue_tlatam_usa")
    revenue_tlatam_mex = fields.Float('Costos Interco TALENT LATAM MEX', store=False,compute="calc_revenue_tlatam_mex" )
    revenue_tlatam_arg = fields.Float('Costos Interco TALENT LATAM ARG', store=False, compute="calc_revenue_tlatam_arg")

    revenue_tusa_usa = fields.Float('Costos Interco TALENT USA USA', store=False, compute="calc_revenue_tusa_usa")
    revenue_tusa_mex = fields.Float('Costos Interco TALENT USA MEX', store=False, compute="calc_revenue_tusa_mex")
    revenue_tusa_arg = fields.Float('Costos Interco TALENT USA ARG', store=False, compute="calc_revenue_tusa_arg")

    icdirecto_total= fields.Float('Total IC Directo')
    icdirecto_usa = fields.Float('IC directo USA')
    icdirecto_mex = fields.Float('IC directo MEX')
    #icdirecto_arg = fields.Float('Recruiting ARG')

    recruiting_total= fields.Float('Total Recruiting')
    recruiting_usa = fields.Float('Recupero Rec USA CD')
    recruiting_mex = fields.Float('Recupero Rec MEX CD')
    recruiting_arg = fields.Float('Recupero ARG')

    mkt_total = fields.Float('Total MKT directo')
    mkt_usa = fields.Float('Recupero MKT USA CD')
    mkt_mex = fields.Float('Recupero MKT MEX CD')
    mkt_arg = fields.Float('Recupero MKT ARG')

    op_total = fields.Float('Total OP directo')
    op_usa = fields.Float('Recupero OP USA CD')
    op_mex = fields.Float('Recupero OP MEX CD')
    op_arg = fields.Float('Recupero OP ARG')

    sales_total = fields.Float('Total SALES directo')
    sales_usa = fields.Float('Recupero SALES USA CD')
    sales_mex = fields.Float('Recupero SALES MEX CD')
    sales_arg = fields.Float('Recupero SALES ARG')

    presales_total = fields.Float('Total PRESALES directo')
    presales_usa = fields.Float('Recupero PRESALES USA')
    presales_mex = fields.Float('Recupero PRESALES MEX')
    presales_arg = fields.Float('Recupero PRESALES ARG')

    ciun_total = fields.Float('Total Comisiones MKT UN')
    ciun_usa = fields.Float('Recupero CI UN USA')
    ciun_mex = fields.Float('Recupero CI UN MEX')
    ciun_arg = fields.Float('Recupero CI UN ARG')

    comun_total = fields.Float('Total Comisiones UN')
    comun_usa = fields.Float('Recupero Comisiones UN USA')
    comun_mex = fields.Float('Recupero Comisiones UN MEX')

    ci_total = fields.Float('Total CI')
    ci_usa = fields.Float('Recupero CI USA')
    ci_mex = fields.Float('Recupero CI MEX')
    ci_arg = fields.Float('Recupero CI ARG')

    comi_total = fields.Float('Total Comisiones Talent')
    comi_usa = fields.Float('Recupero Comisiones Talent USA')
    comi_mex = fields.Float('Recupero Comisiones Talent MEX')

    comimkt_total = fields.Float('Total Comisiones MKT')
    comimkt_usa = fields.Float('Recupero Comisiones MKT USA')
    comimkt_mex = fields.Float('Recupero Comisiones MKT MEX')

    leadsmkt_total = fields.Float('Total Leads MKT')
    leadsmkt_usa = fields.Float('Recupero Leads MKT USA')
    leadsmkt_mex = fields.Float('Recupero Leads MKT MEX')

    def calc_revenue(self):
        #busco el total para sacar proporcional por pais
        request = "SELECT  SUM(total) tot_revenue_interco  FROM  revenue_interco" \
                  " WHERE mes='" + str(self.mes) + "' and anio=" + str(self.anio)
        self.env.cr.execute(request)
        for record in self.env.cr.dictfetchall():
            self.revenue_interco_total= record['tot_revenue_interco']

    def _calc_revenue_pais(self, pais, costo):
        tot_pais=0
        revenue_pais=0

        request = "SELECT "+ costo +" as tot_revenue_interco  FROM  revenue_interco" \
                  " WHERE mes='" + str(self.mes) + "' and anio=" + str(self.anio) + " and pais='" + pais + "'"
        self.env.cr.execute(request)
        for record in self.env.cr.dictfetchall():
            tot_pais=record['tot_revenue_interco']
        _logger.info('REVENUE PAIS :' + pais +' COSTO ' + costo + '-'+  str(tot_pais))
        _logger.info('REVENUE total : COSTO ' + costo + '-' + str(self.revenue_interco_total))
        if tot_pais and self.revenue_interco_total>0:
            revenue_pais= tot_pais /self.revenue_interco_total
        return revenue_pais

    def calc_revenue_mex(self):
        self.revenue_interco_mex= self._calc_revenue_pais("MEX","total")

    def calc_revenue_usa(self):
        self.revenue_interco_usa= self._calc_revenue_pais("USA","total")

    def calc_revenue_arg(self):
        self.revenue_interco_arg= self._calc_revenue_pais("ARG","total")

    def calc_revenue_b1_usa(self):
        self.revenue_b1_usa=self._calc_revenue_pais("USA","totb1")

    def calc_revenue_b1_mex(self):
        self.revenue_b1_mex=self._calc_revenue_pais("MEX","totb1")

    def calc_revenue_b1_arg(self):
        self.revenue_b1_arg=self._calc_revenue_pais("ARG","totb1")

    def calc_revenue_nt_usa(self):
        self.revenue_nt_usa = self._calc_revenue_pais("USA", "totnt")

    def calc_revenue_nt_mex(self):
        self.revenue_nt_mex = self._calc_revenue_pais("MEX", "totnt")

    def calc_revenue_nt_arg(self):
        self.revenue_nt_arg = self._calc_revenue_pais("ARG", "totnt")

    def calc_revenue_mkt_usa(self):
        self.revenue_mkt_usa = self._calc_revenue_pais("USA", "totmkt")

    def calc_revenue_mkt_mex(self):
        self.revenue_mkt_mex =  self._calc_revenue_pais("MEX", "totmkt")

    def calc_revenue_mkt_arg(self):
        self.revenue_mkt_arg =  self._calc_revenue_pais("ARG", "totmkt")

    def calc_revenue_s4_usa(self):
        self.revenue_s4_usa = self._calc_revenue_pais("ARG", "tots4")

    def calc_revenue_s4_mex(self):
        self.revenue_s4_mex = self._calc_revenue_pais("MEX", "tots4")

    def calc_revenue_s4_arg(self):
        self.revenue_s4_arg = self._calc_revenue_pais("ARG", "tots4")

    def calc_revenue_tlatam_usa(self):
        self.revenue_tlatam_usa=self._calc_revenue_pais("USA", "tottalentlatam")

    def calc_revenue_tlatam_mex(self):
        self.revenue_tlatam_mex=self._calc_revenue_pais("MEX", "tottalentlatam")

    def calc_revenue_tlatam_arg(self):
        self.revenue_tlatam_arg=self._calc_revenue_pais("ARG", "tottalentlatam")

    def calc_revenue_tusa_usa(self):
        self.revenue_tusa_usa=self._calc_revenue_pais("USA","tottalentusa")

    def calc_revenue_tusa_mex(self):
        self.revenue_tusa_mex=self._calc_revenue_pais("MEX","tottalentusa")

    def calc_revenue_tusa_arg(self):
        self.revenue_tusa_arg=self._calc_revenue_pais("ARG","tottalentusa")
    def process_results(self):
        # mejora, recorrer type_results y ejecutar procesos segun , es por subgrupos, es ctaingreso, es RG
        # ***********  PROCESO IC DIRECTO *******************
        icdirecto = self.env['type.results'].search([('resultado', '=', 'IC DIRECTO')], limit=1)
        if icdirecto:
            # Si encuentra la configuracion busco los grupos
            suma_resultado = 0
            for grupo in icdirecto.grupo:
                # por cada grupo, busco las cuentas relacionadas
                suma_grupo_mex = 0
                cuentas_mex = self.env['account.account'].search([('grupo', '=', grupo.id),('pais','=','MEX')])
                _logger.info('GRUPO:' + grupo.name + 'CUENTAS MEX:' + str(cuentas_mex))
                for cuenta in cuentas_mex:
                    request = "SELECT  SUM(debit) as debit_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + "  and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio)
                    _logger.info('QUERY:' + request)
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['debit_account']:
                            suma_grupo_mex += record['debit_account']
                    #-------------USA
                    suma_grupo_usa=0
                    cuentas_usa = self.env['account.account'].search([('grupo', '=', grupo.id), ('pais', '=', 'USA')])
                    _logger.info('GRUPO:' + grupo.name + 'CUENTAS USA:' + str(cuentas_usa))
                    for cuenta in cuentas_usa:
                        request = "SELECT  SUM(debit) as debit_account  FROM account_move_line " \
                                  " WHERE account_id = " + str(cuenta.id) + "  and date_part('month',date)=" + str(
                            self.mes) + " and date_part('year',date)=" + str(self.anio)
                        _logger.info('QUERY:' + request)
                        self.env.cr.execute(request)
                        for record in self.env.cr.dictfetchall():
                            if record['debit_account']:
                                suma_grupo_usa += record['debit_account']
                # mando a log el total por grupo
                _logger.info('TOTAL grupo:' + str(suma_grupo_usa))
                suma_resultado += suma_grupo_usa + suma_grupo_mex
            # calculos finales-----
            self.icdirecto_total = suma_resultado
            self.icdirecto_mex = suma_grupo_mex
            self.icdirecto_usa = suma_grupo_usa

        # *******************- fin IC DIRECTO***************
        #***********  PROCESO RECRUITING *******************
        recruiting = self.env['type.results'].search([('resultado', '=', 'RECRUITING')], limit=1)
        if recruiting:
            # Si encuentra la configuracion busco los grupos
            suma_resultado = 0
            for grupo in recruiting.grupo:
                # por cada grupo, busco las cuentas relacionadas
                suma_grupo = 0
                cuentas = self.env['account.account'].search([('grupo', '=', grupo.id)])
                _logger.info('GRUPO:' + grupo.name + 'CUENTAS:' + str(cuentas))
                for cuenta in cuentas:
                    request = "SELECT  SUM(debit) as debit_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + "  and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio)
                    _logger.info('QUERY:' + request)
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['debit_account']:
                            suma_grupo += record['debit_account']
                # mando a log el total por grupo
                _logger.info('TOTAL grupo:' + str(suma_grupo))
                suma_resultado += suma_grupo
            # calculos finales-----
            self.recruiting_total = suma_resultado
            self.recruiting_mex = suma_resultado * self.revenue_interco_mex
            self.recruiting_usa = suma_resultado * self.revenue_interco_usa
            self.recruiting_arg = suma_resultado * self.revenue_interco_arg

        #*******************- fin recruiting***************
        #---------------- PROCESO MKT -----------------
        mkt = self.env['type.results'].search([('resultado', '=', 'MKT')], limit=1)
        if mkt:
            suma_mkt, suma_b1, suma_nt, suma_s4, suma_tusa, suma_tlatam = 0, 0, 0, 0, 0, 0
            for grupo in mkt.grupo:
                suma_b1= self.calc_subgrupos('B1',grupo.id)
                suma_nt = self.calc_subgrupos('NT', grupo.id)
                suma_mkt = self.calc_subgrupos('MKT', grupo.id)
                suma_s4 = self.calc_subgrupos('S4', grupo.id)
                suma_tusa = self.calc_subgrupos('TUSA', grupo.id)
                suma_tlatam = self.calc_subgrupos('TLATAM', grupo.id)

            # calculos finales-----
            _logger.info('GRUPO MKT:')
            _logger.info('  b1:' + str(suma_b1 * self.revenue_b1_usa))
            _logger.info('  nt:' + str(suma_nt * self.revenue_nt_usa))
            _logger.info('  mkt:' + str(suma_mkt * self.revenue_mkt_usa))
            _logger.info('  s4:' + str(suma_s4 * self.revenue_s4_usa))
            _logger.info('  tlatam:' + str(suma_tlatam * self.revenue_tlatam_usa))
            _logger.info('  tusa:' + str(suma_tusa * self.revenue_tusa_usa))
            self.mkt_usa = (suma_b1 * self.revenue_b1_usa) + (suma_nt * self.revenue_nt_usa) + (suma_mkt * self.revenue_mkt_usa) + (suma_s4 * self.revenue_s4_usa) + (suma_tlatam * self.revenue_tlatam_usa) +(suma_tusa * self.revenue_tusa_usa)
            self.mkt_mex = (suma_b1 * self.revenue_b1_mex) + (suma_nt * self.revenue_nt_mex) + (suma_mkt*self.revenue_mkt_mex) + (suma_s4*self.revenue_s4_mex) + (suma_tlatam*self.revenue_tlatam_mex) +(suma_tusa*self.revenue_tusa_mex)
            #self.mkt_arg =  (suma_b1 * self.revenue_b1_mex) + (suma_nt * self.revenue_nt_arg) + (suma_mkt*self.revenue_mkt_arg) + (suma_s4*self.revenue_s4_arg) + (suma_tlatam*self.revenue_tlatam_arg) +(suma_tusa*self.revenue_tusa_arg)
            self.mkt_total = self.mkt_usa + self.mkt_mex
        # ---------------- PROCESO OP -----------------
        op = self.env['type.results'].search([('resultado', '=', 'OP')], limit=1)
        if op:
            suma_mkt,suma_b1,suma_nt, suma_s4,suma_tusa, suma_tlatam= 0,0,0,0,0,0

            for grupo in op.grupo:
                suma_b1 = self.calc_subgrupos('B1', grupo.id)
                suma_nt = self.calc_subgrupos('NT', grupo.id)
                suma_mkt = self.calc_subgrupos('MKT', grupo.id)
                suma_s4 = self.calc_subgrupos('S4', grupo.id)
                suma_tusa = self.calc_subgrupos('TUSA', grupo.id)
                suma_tlatam = self.calc_subgrupos('TLATAM', grupo.id)
            # calculos finales-----
            _logger.info('GRUPO OP')
            _logger.info('  b1:' + str(suma_b1 * self.revenue_b1_usa))
            _logger.info('  nt:' + str(suma_nt * self.revenue_nt_usa))
            _logger.info('  mkt:' + str(suma_mkt * self.revenue_mkt_usa))
            _logger.info('  s4:' + str(suma_s4 * self.revenue_s4_usa))
            _logger.info('  tlatam:' + str(suma_tlatam * self.revenue_tlatam_usa))
            _logger.info('  tusa:' + str(suma_tusa * self.revenue_tusa_usa))
            self.op_usa = (suma_b1 * self.revenue_b1_usa) + (suma_nt * self.revenue_nt_usa) + (
                        suma_mkt * self.revenue_mkt_usa) + (suma_s4 * self.revenue_s4_usa) + (
                                       suma_tlatam * self.revenue_tlatam_usa) + (suma_tusa * self.revenue_tusa_usa)
            self.op_mex = (suma_b1 * self.revenue_b1_mex) + (suma_nt * self.revenue_nt_mex) + (
                        suma_mkt * self.revenue_mkt_mex) + (suma_s4 * self.revenue_s4_mex) + (
                                       suma_tlatam * self.revenue_tlatam_mex) + (suma_tusa * self.revenue_tusa_mex)
        #    self.op_arg = (suma_b1 * self.revenue_b1_mex) + (suma_nt * self.revenue_nt_arg) + (
        #                suma_mkt * self.revenue_mkt_arg) + (suma_s4 * self.revenue_s4_arg) + (
        #                               suma_tlatam * self.revenue_tlatam_arg) + (suma_tusa * self.revenue_tusa_arg)
            self.op_total = self.op_usa + self.op_mex
        # ---------------- PROCESO SALES -----------------
        sales = self.env['type.results'].search([('resultado', '=', 'SALES')], limit=1)
        if sales:
            suma_mkt, suma_b1, suma_nt, suma_s4, suma_tusa, suma_tlatam = 0, 0, 0, 0, 0, 0

            for grupo in sales.grupo:
                suma_b1 = self.calc_subgrupos('B1', grupo.id)
                suma_nt = self.calc_subgrupos('NT', grupo.id)
                suma_mkt = self.calc_subgrupos('MKT', grupo.id)
                suma_s4 = self.calc_subgrupos('S4', grupo.id)
                suma_tusa = self.calc_subgrupos('TUSA', grupo.id)
                suma_tlatam = self.calc_subgrupos('TLATAM', grupo.id)
            # calculos finales-----
            _logger.info('GRUPO SALES:')
            _logger.info('  b1:' + str(suma_b1 * self.revenue_b1_usa))
            _logger.info('  nt:' + str(suma_nt * self.revenue_nt_usa))
            _logger.info('  mkt:' + str(suma_mkt * self.revenue_mkt_usa))
            _logger.info('  s4:' + str(suma_s4 * self.revenue_s4_usa))
            _logger.info('  tlatam:' + str(suma_tlatam * self.revenue_tlatam_usa))
            _logger.info('  tusa:' + str(suma_tusa * self.revenue_tusa_usa))
            self.sales_usa = (suma_b1 * self.revenue_b1_usa) + (suma_nt * self.revenue_nt_usa) + (
                    suma_mkt * self.revenue_mkt_usa) + (suma_s4 * self.revenue_s4_usa) + (
                                  suma_tlatam * self.revenue_tlatam_usa) + (suma_tusa * self.revenue_tusa_usa)
            self.sales_mex = (suma_b1 * self.revenue_b1_mex) + (suma_nt * self.revenue_nt_mex) + (
                    suma_mkt * self.revenue_mkt_mex) + (suma_s4 * self.revenue_s4_mex) + (
                                  suma_tlatam * self.revenue_tlatam_mex) + (suma_tusa * self.revenue_tusa_mex)
            #self.sales_arg = (suma_b1 * self.revenue_b1_mex) + (suma_nt * self.revenue_nt_arg) + (
            #        suma_mkt * self.revenue_mkt_arg) + (suma_s4 * self.revenue_s4_arg) + (
            #                      suma_tlatam * self.revenue_tlatam_arg) + (suma_tusa * self.revenue_tusa_arg)
            self.sales_total = self.sales_usa + self.sales_mex
        # ---------------- PROCESO PRESALES -----------------
        presales = self.env['type.results'].search([('resultado', '=', 'PRESALES')], limit=1)
        if presales:
            suma_mkt, suma_b1, suma_nt, suma_s4, suma_tusa, suma_tlatam = 0, 0, 0, 0, 0, 0

            for grupo in presales.grupo:
                suma_b1 = self.calc_subgrupos('B1', grupo.id)
                suma_nt = self.calc_subgrupos('NT', grupo.id)
                suma_mkt = self.calc_subgrupos('MKT', grupo.id)
                suma_s4 = self.calc_subgrupos('S4', grupo.id)
                suma_tusa = self.calc_subgrupos('TUSA', grupo.id)
                suma_tlatam = self.calc_subgrupos('TLATAM', grupo.id)
            # calculos finales-----
            _logger.info('GRUPO PRESALES')
            _logger.info('  b1:' + str(suma_b1 * self.revenue_b1_usa))
            _logger.info('  nt:' + str(suma_nt * self.revenue_nt_usa))
            _logger.info('  mkt:' + str(suma_mkt * self.revenue_mkt_usa))
            _logger.info('  s4:' + str(suma_s4 * self.revenue_s4_usa))
            _logger.info('  tlatam:' + str(suma_tlatam * self.revenue_tlatam_usa))
            _logger.info('  tusa:' + str(suma_tusa * self.revenue_tusa_usa))
            self.presales_usa = (suma_b1 * self.revenue_b1_usa) + (suma_nt * self.revenue_nt_usa) + (
                    suma_mkt * self.revenue_mkt_usa) + (suma_s4 * self.revenue_s4_usa) + (
                                     suma_tlatam * self.revenue_tlatam_usa) + (suma_tusa * self.revenue_tusa_usa)
            self.presales_mex = (suma_b1 * self.revenue_b1_mex) + (suma_nt * self.revenue_nt_mex) + (
                    suma_mkt * self.revenue_mkt_mex) + (suma_s4 * self.revenue_s4_mex) + (
                                     suma_tlatam * self.revenue_tlatam_mex) + (suma_tusa * self.revenue_tusa_mex)
            #self.presales_arg = (suma_b1 * self.revenue_b1_mex) + (suma_nt * self.revenue_nt_arg) + (
            #        suma_mkt * self.revenue_mkt_arg) + (suma_s4 * self.revenue_s4_arg) + (
            #                         suma_tlatam * self.revenue_tlatam_arg) + (suma_tusa * self.revenue_tusa_arg)
            self.presales_total = self.presales_usa + self.presales_mex
        # ---------------- PROCESO CI -----------------
        ciun = self.env['type.results'].search([('resultado', '=', 'CI-UN')], limit=1)
        if ciun:
            suma_mkt, suma_b1, suma_nt, suma_s4, suma_tusa, suma_tlatam = 0, 0, 0, 0, 0, 0

            for grupo in ciun.grupo:
                suma_b1 = self.calc_subgrupos('B1', grupo.id)
                suma_nt = self.calc_subgrupos('NT', grupo.id)
                suma_mkt = self.calc_subgrupos('MKT', grupo.id)
                suma_s4 = self.calc_subgrupos('S4', grupo.id)
                suma_tusa = self.calc_subgrupos('TUSA', grupo.id)
                suma_tlatam = self.calc_subgrupos('TLATAM', grupo.id)
            # calculos finales-----
            _logger.info('GRUPO CIUN')
            _logger.info('  b1:' + str(suma_b1 * self.revenue_b1_usa))
            _logger.info('  nt:' + str(suma_nt * self.revenue_nt_usa))
            _logger.info('  mkt:' + str(suma_mkt * self.revenue_mkt_usa))
            _logger.info('  s4:' + str(suma_s4 * self.revenue_s4_usa))
            _logger.info('  tlatam:' + str(suma_tlatam * self.revenue_tlatam_usa))
            _logger.info('  tusa:' + str(suma_tusa * self.revenue_tusa_usa))
            self.ciun_usa = (suma_b1 * self.revenue_b1_usa) + (suma_nt * self.revenue_nt_usa) + (
                    suma_mkt * self.revenue_mkt_usa) + (suma_s4 * self.revenue_s4_usa) + (
                                     suma_tlatam * self.revenue_tlatam_usa) + (suma_tusa * self.revenue_tusa_usa)
            self.ciun_mex = (suma_b1 * self.revenue_b1_mex) + (suma_nt * self.revenue_nt_mex) + (
                    suma_mkt * self.revenue_mkt_mex) + (suma_s4 * self.revenue_s4_mex) + (
                                     suma_tlatam * self.revenue_tlatam_mex) + (suma_tusa * self.revenue_tusa_mex)
            #self.ciun_arg = (suma_b1 * self.revenue_b1_mex) + (suma_nt * self.revenue_nt_arg) + (
            #        suma_mkt * self.revenue_mkt_arg) + (suma_s4 * self.revenue_s4_arg) + (
            #                         suma_tlatam * self.revenue_tlatam_arg) + (suma_tusa * self.revenue_tusa_arg)
            self.ciun_total = self.op_usa + self.op_mex
        #---------------fin proceso CI-UN--------------------

        # ---------------- PROCESO comisiones Talent  -----------------
        comtalent = self.env['type.results'].search([('resultado', '=', 'COMISIONES TALENT')], limit=1)
        if comtalent:
            # en excel solo toma a un grupo para cda cuenta contable, igual hago la suma por si hubieran mas
            # -------------USA
            suma_grupo_usa = 0
            suma_grupo_mex = 0
            for grupo in comtalent.grupo:
                cuentas_usa = self.env['account.account'].search([('grupo', '=', grupo.id), ('pais', '=', 'USA')])
                _logger.info('GRUPO:' + grupo.name + 'CUENTAS USA:' + str(cuentas_usa))
                for cuenta in cuentas_usa:
                    request = "SELECT  SUM(debit) as debit_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + "  and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio)
                    _logger.info('QUERY:' + request)
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['debit_account']:
                            suma_grupo_usa += record['debit_account']
                # -------------MEX
                cuentas_mex = self.env['account.account'].search([('grupo', '=', grupo.id), ('pais', '=', 'MEX')])
                _logger.info('GRUPO:' + grupo.name + 'CUENTAS MEX:' + str(cuentas_usa))
                for cuenta in cuentas_mex:
                    request = "SELECT  SUM(debit) as debit_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + "  and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio)
                    _logger.info('QUERY:' + request)
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['debit_account']:
                            suma_grupo_mex += record['debit_account']

            # calculos finales-----
            _logger.info('GRUPO COMISIONES UN')
            _logger.info(' total:' + str(suma_grupo_usa))
            self.comi_usa = suma_grupo_usa
            self.comi_mex =  suma_grupo_mex
            self.comi_total = suma_grupo_usa + suma_grupo_mex
        # ---------------fin proceso Comisiones-Talent--------------------
        # ---------------- PROCESO comisiones mkt  -----------------
        commkt = self.env['type.results'].search([('resultado', '=', 'COMISIONES MKT')], limit=1)
        if commkt:
            # en excel solo toma a un grupo para cda cuenta contable, igual hago la suma por si hubieran mas
            # -------------USA
            suma_grupo_usa = 0
            suma_grupo_mex = 0
            for grupo in commkt.grupo:
                cuentas_usa = self.env['account.account'].search([('grupo', '=', grupo.id), ('pais', '=', 'USA')])
                _logger.info('GRUPO:' + grupo.name + 'CUENTAS USA:' + str(cuentas_usa))
                for cuenta in cuentas_usa:
                    request = "SELECT  SUM(debit) as debit_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + "  and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio)
                    _logger.info('QUERY:' + request)
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['debit_account']:
                            suma_grupo_usa += record['debit_account']
                # -------------MEX
                cuentas_mex = self.env['account.account'].search([('grupo', '=', grupo.id), ('pais', '=', 'MEX')])
                _logger.info('GRUPO:' + grupo.name + 'CUENTAS MEX:' + str(cuentas_usa))
                for cuenta in cuentas_mex:
                    request = "SELECT  SUM(debit) as debit_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + "  and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio)
                    _logger.info('QUERY:' + request)
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['debit_account']:
                            suma_grupo_mex += record['debit_account']

            # calculos finales-----
            _logger.info('GRUPO COMISIONES MKT')
            _logger.info(' total:' + str(suma_grupo_usa))
            self.comimkt_usa_usa = suma_grupo_usa
            self.comimkt_mex = suma_grupo_mex
            self.comimkt_total = suma_grupo_usa + suma_grupo_mex
        #***************  FIN comisiones kmt **************
        # ---------------- PROCESO leads mkt  UN  -----------------
        leads = self.env['type.results'].search([('resultado', '=', 'LEADS MKT')], limit=1)
        if leads:
            # en excel muestran solo mkt asi que no diferencio por subgrupo. trato atodo el grupo como MKT
            suma_grupo_usa = 0
            suma_grupo_mex = 0
            for grupo in leads.grupo:
                # -------------USA
                cuentas_usa = self.env['account.account'].search([('grupo', '=', grupo.id), ('pais', '=', 'USA')])
                _logger.info('GRUPO:' + grupo.name + 'CUENTAS USA:' + str(cuentas_usa))
                for cuenta in cuentas_usa:
                    request = "SELECT  SUM(debit) as debit_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + "  and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio)
                    _logger.info('QUERY:' + request)
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['debit_account']:
                            suma_grupo_usa += record['debit_account']
                # -------------MEX
                cuentas_mex = self.env['account.account'].search([('grupo', '=', grupo.id), ('pais', '=', 'MEX')])
                _logger.info('GRUPO:' + grupo.name + 'CUENTAS MEX:' + str(cuentas_usa))
                for cuenta in cuentas_mex:
                    request = "SELECT  SUM(debit) as debit_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + "  and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio)
                    _logger.info('QUERY:' + request)
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['debit_account']:
                            suma_grupo_mex += record['debit_account']

                # calculos finales-----
                _logger.info('GRUPO LEADS MKT')
                _logger.info(' total:' + str(suma_grupo_usa))
                self.leadsmkt_usa = suma_grupo_usa
                self.leadsmkt_mex = suma_grupo_mex
                self.leadsmkt_total = suma_grupo_usa + suma_grupo_mex
        # ---------------- PROCESO comisiones UN  -----------------
        com = self.env['type.results'].search([('resultado', '=', 'COMISIONES UN')], limit=1)
        if com:
            # en excel muestran solo mkt asi que no diferencio por subgrupo. trato atodo el grupo como MKT
            suma_grupo_usa = 0
            suma_grupo_mex = 0
            for grupo in com.grupo:
                # -------------USA
                cuentas_usa = self.env['account.account'].search(
                    [('grupo', '=', grupo.id), ('pais', '=', 'USA')])
                _logger.info('GRUPO:' + grupo.name + 'CUENTAS USA:' + str(cuentas_usa))
                for cuenta in cuentas_usa:
                    request = "SELECT  SUM(debit) as debit_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + "  and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio)
                    _logger.info('QUERY:' + request)
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['debit_account']:
                            suma_grupo_usa += record['debit_account']
                # -------------MEX
                cuentas_mex = self.env['account.account'].search(
                    [('grupo', '=', grupo.id), ('pais', '=', 'MEX')])
                _logger.info('GRUPO:' + grupo.name + 'CUENTAS MEX:' + str(cuentas_usa))
                for cuenta in cuentas_mex:
                    request = "SELECT  SUM(debit) as debit_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + "  and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio)
                    _logger.info('QUERY:' + request)
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['debit_account']:
                            suma_grupo_mex += record['debit_account']

                # calculos finales-----
                _logger.info('GRUPO COMISIONES UN')
                _logger.info(' total:' + str(suma_grupo_usa))
                self.comun_usa = suma_grupo_usa
                self.comun_mex = suma_grupo_mex
                self.comun_total = suma_grupo_usa + suma_grupo_mex

        #*************** CALCULO CI*************************
        # CALCULA SOBRE SUMA DE GRUPOS COMO EN RECRUITING
        comisiones = self.env['type.results'].search([('resultado', '=', 'CI')], limit=1)
        if comisiones:
            # Si encuentra la configuracion busco los grupos
            suma_resultado = 0
            for grupo in comisiones.grupo:
                # por cada grupo, busco las cuentas relacionadas
                suma_grupo = 0
                cuentas = self.env['account.account'].search([('grupo', '=', grupo.id)])
                _logger.info('GRUPO:' + grupo.name + 'CUENTAS:' + str(cuentas))
                for cuenta in cuentas:
                    request = "SELECT  SUM(debit) as debit_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + "  and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio)
                    _logger.info('QUERY:' + request)
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['debit_account']:
                            suma_grupo += record['debit_account']
                # mando a log el total por grupo
                _logger.info('TOTAL grupo:' + str(suma_grupo))
                suma_resultado += suma_grupo
            # calculos finales-----
            self.ci_mex = (suma_resultado * self.revenue_interco_mex)
            self.ci_usa = (suma_resultado * self.revenue_interco_usa)
            #self.ci_arg = (suma_resultado * self.revenue_interco_arg)
            self.ci_total = self.ci_mex + self.ci_usa

        self.state = 'checkpoint'

    #**********************  FIN PROCESO******************
    def calc_subgrupos(self,subgrupo, grupo_id):
        suma_subgrupo = 0
        request_cta="SELECT cta.id as id FROM account_account as cta INNER JOIN intercompany_cost_subgroups as subgrup ON subgrup.grupo_id= cta.grupo " \
                    "WHERE grupo=" + str(grupo_id) + " and subgrup.distribucion_costo='"+ subgrupo +"'"

        _logger.info('QUERY:' + request_cta)
        self.env.cr.execute(request_cta)
        for record_cta in self.env.cr.dictfetchall():
            request = "SELECT  SUM(debit) as debit_account  FROM account_move_line " \
                      " WHERE account_id = " + str(record_cta['id']) +  "  and date_part('month',date)=" + str(self.mes) +" and date_part('year',date)=" + str(self.anio)
            _logger.info('QUERY:' + request)
            self.env.cr.execute(request)
            for record in self.env.cr.dictfetchall():
                if record['debit_account']:
                    suma_subgrupo += record['debit_account']
        # mando a log el total por subgrupo
        _logger.info('-------TOTAL' + subgrupo + ':' + str(suma_subgrupo))
        return suma_subgrupo

    #def busca


