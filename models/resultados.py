from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class TypeResults(models.Model):
    _name = 'type.results'

    resultado=fields.Char('Resultado',required=True)
    grupo = fields.Many2many('intercompany.cost.groups', string='Grupo',required=True)
    ctacontable_B1_mex=fields.Many2one('account.account',string='Cta Recupero B1 MEX')
    ctacontable_MKT_mex = fields.Many2one('account.account', string='Cta Recupero MKT MEX')
    ctacontable_NT_mex = fields.Many2one('account.account', string='Cta Recupero NT MEX')
    ctacontable_S4_mex = fields.Many2one('account.account', string='Cta Recupero S4 MEX')
    ctacontable_talent_mex = fields.Many2one('account.account', string='Cta Recupero TLatam')

    ctacontable_B1_usa = fields.Many2one('account.account', string='Cta Recupero B1 USA')
    ctacontable_MKT_usa = fields.Many2one('account.account', string='Cta Recupero MKT USA')
    ctacontable_NT_usa = fields.Many2one('account.account', string='Cta Recupero NT USA')
    ctacontable_S4_usa = fields.Many2one('account.account', string='Cta Recupero S4 USA')
    ctacontable_talent_usa = fields.Many2one('account.account', string='Cta Recupero TUSA')

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

    revenue_interco_total= fields.Float('Costos Interco', store=False, compute="calc_revenue", digits=(6,2))
    revenue_interco_usa = fields.Float('Costos Interco USA', store=False, compute="calc_revenue_usa",digits=(6,2))
    revenue_interco_mex = fields.Float('Costos Interco MEX', store=False, compute="calc_revenue_mex",digits=(6,2))
    revenue_interco_arg = fields.Float('Costos Interco ARG', store=False, compute="calc_revenue_arg",digits=(6,2))

    revenue_b1_usa= fields.Float('Costos Interco B1 USA', store=False, compute="calc_revenue_b1_usa",digits=(6,2))
    revenue_b1_mex = fields.Float('Costos Interco B1 MEX', store=False, compute="calc_revenue_b1_mex",digits=(6,2))
    revenue_b1_arg = fields.Float('Costos Directo OP', store=False,compute="calc_revenue_b1_arg",digits=(6,2))
    revenue_interco_total_b1 = fields.Float('Costos Interco B1', store=False,compute="calc_revenue_total_b1",digits=(6,2))

    revenue_nt_usa = fields.Float('Costos Interco NT USA', store=False, compute="calc_revenue_nt_usa",digits=(6,2))
    revenue_nt_mex = fields.Float('Costos Interco NT MEX', store=False,compute="calc_revenue_nt_mex",digits=(6,2))
    revenue_nt_arg = fields.Float('Costos Interco NT ARG', store=False,compute="calc_revenue_nt_arg",digits=(6,2))
    revenue_interco_total_nt = fields.Float('Costos Interco NT', store=False,compute="calc_revenue_total_nt",digits=(6,2))

    revenue_mkt_usa = fields.Float('Costos Interco MKT USA', store=False, compute="calc_revenue_mkt_usa",digits=(6,2))
    revenue_mkt_mex = fields.Float('Costos Interco MKT MEX', store=False,compute="calc_revenue_mkt_mex",digits=(6,2))
    revenue_mkt_arg = fields.Float('Costos Interco MKT ARG', store=False,compute="calc_revenue_mkt_arg",digits=(6,2))
    revenue_interco_total_mkt = fields.Float('Costos Interco MKTcalc_revenue_total_latam', store=False, compute="calc_revenue_total_mkt",
                                            digits=(6, 2))

    revenue_s4_usa = fields.Float('Costos Interco S4 USA', store=False, compute="calc_revenue_s4_usa",digits=(6,2))
    revenue_s4_mex = fields.Float('Costos Interco S4 MEX', store=False, compute="calc_revenue_s4_mex",digits=(6,2))
    revenue_s4_arg = fields.Float('Costos Interco S4 ARG', store=False, compute="calc_revenue_s4_arg",digits=(6,2))
    revenue_interco_total_s4 = fields.Float('Costos Interco S4', store=False, compute="calc_revenue_total_s4",
                                             digits=(6, 2))

    revenue_tlatam_usa = fields.Float('Costos Interco TALENT LATAM USA', store=False, compute="calc_revenue_tlatam_usa",digits=(6,2))
    revenue_tlatam_mex = fields.Float('Costos Interco TALENT LATAM MEX', store=False,compute="calc_revenue_tlatam_mex" ,digits=(6,2))
    revenue_tlatam_arg = fields.Float('Costos Interco TALENT LATAM ARG', store=False, compute="calc_revenue_tlatam_arg",digits=(6,2))
    revenue_interco_total_latam = fields.Float('Costos Interco talent latam', store=False, compute="calc_revenue_total_latam",
                                            digits=(6, 2))

    revenue_tusa_usa = fields.Float('Costos Interco TALENT USA USA', store=False, compute="calc_revenue_tusa_usa",digits=(6,2))
    revenue_tusa_mex = fields.Float('Costos Interco TALENT USA MEX', store=False, compute="calc_revenue_tusa_mex",digits=(6,2))
    revenue_tusa_arg = fields.Float('Costos Interco TALENT USA ARG', store=False, compute="calc_revenue_tusa_arg",digits=(6,2))
    revenue_interco_total_usa = fields.Float('Costos Interco talent latam', store=False,
                                                compute="calc_revenue_total_usa",
                                                digits=(10, 2))

    icdirecto_total= fields.Float('Total IC Directo')
    icdirecto_usa = fields.Float('IC directo USA')
    icdirecto_mex = fields.Float('IC directo MEX')
    #icdirecto_arg = fields.Float('Recruiting ARG')

    recruiting_total= fields.Float('Total Recruiting')
    recruiting_b1_usa = fields.Float('Recruiting B1 USA')
    recruiting_nt_usa = fields.Float('Recruiting NT USA')
    recruiting_mkt_usa = fields.Float('Recruiting MKT USA')
    recruiting_s4_usa = fields.Float('Recruiting S4 USA')
    recruiting_talent_usa  = fields.Float('Recruiting Talent USA')
    recruiting_b1_mex = fields.Float('Recruiting B1 MEX')
    recruiting_nt_mex = fields.Float('Recruiting NT MEX')
    recruiting_mkt_mex = fields.Float('Recruiting MKT MEX')
    recruiting_s4_mex = fields.Float('Recruiting S4 MEX')
    recruiting_talent_mex = fields.Float('Recruiting Talent Latam')
    recruiting_usa = fields.Float('Rec. Recruiting USA CD')
    recruiting_mex = fields.Float('Rec. Recruiting MEX CD')
    recruiting_arg = fields.Float('Rec. Recruiting ARG')

    mkt_total = fields.Float('Total MKT directo')
    mkt_b1_usa = fields.Float('MKT B1 USA')
    mkt_nt_usa = fields.Float('MKT NT USA')
    mkt_mkt_usa = fields.Float('MKT MKT USA')
    mkt_s4_usa = fields.Float('MKT S4 USA')
    mkt_talent_usa = fields.Float('MKT Talent USA')
    mkt_b1_mex = fields.Float('MKT B1 MEX')
    mkt_nt_mex = fields.Float('MKT NT MEX')
    mkt_mkt_mex = fields.Float('MKT MKT MEX')
    mkt_s4_mex = fields.Float('MKT S4 MEX')
    mkt_talent_mex = fields.Float('MKT Talent Latam')
    mkt_usa = fields.Float('Recupero MKT USA CD')
    mkt_mex = fields.Float('Recupero MKT MEX CD')
    mkt_arg = fields.Float('Recupero MKT ARG')

    op_total = fields.Float('Total OP directo')
    op_b1_usa = fields.Float('OP B1 USA')
    op_nt_usa = fields.Float('OP NT USA')
    op_mkt_usa = fields.Float('OP MKT USA')
    op_s4_usa = fields.Float('OP S4 USA')
    op_talent_usa = fields.Float('OP Talent USA')
    op_b1_mex = fields.Float('OP B1 MEX')
    op_nt_mex = fields.Float('OP NT MEX')
    op_mkt_mex = fields.Float('OP MKT MEX')
    op_s4_mex = fields.Float('OP S4 MEX')
    op_talent_mex = fields.Float('OP Talent Latam')
    op_usa = fields.Float('Recupero OP USA CD')
    op_mex = fields.Float('Recupero OP MEX CD')
    op_arg = fields.Float('Recupero OP ARG')

    sales_total = fields.Float('Total SALES directo')
    sales_b1_mex = fields.Float('SALES B1 MEX')
    sales_nt_mex = fields.Float('SALES NT MEX')
    sales_mkt_mex = fields.Float('SALES MKT MEX')
    sales_s4_mex = fields.Float('SALES S4 MEX')
    sales_talent_mex = fields.Float('SALES Talent Latam')
    sales_b1_usa = fields.Float('SALES B1 USA')
    sales_nt_usa = fields.Float('SALES NT USA')
    sales_mkt_usa = fields.Float('SALES MKT USA')
    sales_s4_usa = fields.Float('SALES S4 USA')
    sales_talent_usa = fields.Float('SALES Talent USA')
    sales_usa = fields.Float('Recupero SALES USA CD')
    sales_mex = fields.Float('Recupero SALES MEX CD')
    sales_arg = fields.Float('Recupero SALES ARG')

    presales_total = fields.Float('Total PRESALES directo')
    presales_b1_usa = fields.Float('PRESALES B1 USA')
    presales_nt_usa = fields.Float('PRESALES NT USA')
    presales_mkt_usa = fields.Float('PRESALES MKT USA')
    presales_s4_usa = fields.Float('PRESALES S4 USA')
    presales_talent_usa = fields.Float('PRESALES Talent USA')
    presales_b1_mex = fields.Float('PRESALES B1 MEX')
    presales_nt_mex = fields.Float('PRESALES NT MEX')
    presales_mkt_mex = fields.Float('PRESALES MKT MEX')
    presales_s4_mex = fields.Float('PRESALES S4 MEX')
    presales_talent_mex = fields.Float('PRESALES Talent Latam')
    presales_usa = fields.Float('Recupero PRESALES USA')
    presales_mex = fields.Float('Recupero PRESALES MEX')
    presales_arg = fields.Float('Recupero PRESALES ARG')

    ciun_total = fields.Float('Total Comisiones MKT UN')
    ciun_b1_mex = fields.Float('CI-UN B1 MEX')
    ciun_nt_mex = fields.Float('CI-UN NT MEX')
    ciun_mkt_mex = fields.Float('CI-UN MKT MEX')
    ciun_s4_mex = fields.Float('CI-UN S4 MEX')
    ciun_talent_mex = fields.Float('CI-UN talent Latam')
    ciun_b1_usa = fields.Float('CI-UN B1 USA')
    ciun_nt_usa = fields.Float('CI-UN NT USA')
    ciun_mkt_usa = fields.Float('CI-UN MKT USA')
    ciun_s4_usa = fields.Float('CI-UN S4 USA')
    ciun_talent_usa = fields.Float('CI-UN Talent Usa')
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
    ci_b1_mex = fields.Float('CI B1 MEX')
    ci_nt_mex = fields.Float('CI NT MEX')
    ci_mkt_mex = fields.Float('CI MKT MEX')
    ci_s4_mex = fields.Float('CI S4 MEX')
    ci_talent_mex = fields.Float('CI talent Latam')
    ci_b1_usa = fields.Float('CI B1 USA')
    ci_nt_usa = fields.Float('CI NT USA')
    ci_mkt_usa = fields.Float('CI MKT USA')
    ci_s4_usa = fields.Float('CI S4 USA')
    ci_talent_usa = fields.Float('CI Talent Usa')

    comi_total = fields.Float('Total Comisiones Talent')
    comi_usa = fields.Float('Recupero Comisiones Talent USA')
    comi_mex = fields.Float('Recupero Comisiones Talent MEX')

    comimkt_total = fields.Float('Total Comisiones MKT')
    comimkt_usa = fields.Float('Recupero Comisiones MKT USA')
    comimkt_mex = fields.Float('Recupero Comisiones MKT MEX')

    leadsmkt_total = fields.Float('Total Leads MKT')
    leadsmkt_usa = fields.Float('Recupero Leads MKT USA')
    leadsmkt_mex = fields.Float('Recupero Leads MKT MEX')
    leadsmkt_b1_mex = fields.Float('Leads MKT B1 MEX')
    leadsmkt_nt_mex = fields.Float('Leads MKT NT MEX')
    leadsmkt_mkt_mex = fields.Float('Leads MKT MKT MEX')
    leadsmkt_s4_mex = fields.Float('Leads MKT S4 MEX')
    leadsmkt_talent_mex = fields.Float('Leads MKT talent Latam')
    leadsmkt_b1_usa = fields.Float('Leads MKT B1 USA')
    leadsmkt_nt_usa = fields.Float('Leads MKT NT USA')
    leadsmkt_mkt_usa = fields.Float('Leads MKT MKT USA')
    leadsmkt_s4_usa = fields.Float('Leads MKT S4 USA')
    leadsmkt_talent_usa = fields.Float('Leads MKT Talent Usa')

    def calc_revenue(self):
        #busco el total para sacar proporcional por pais
        request = "SELECT  SUM(total) tot_revenue_interco  FROM  revenue_interco" \
                  " WHERE mes='" + str(self.mes) + "' and anio=" + str(self.anio)
        self.env.cr.execute(request)
        for record in self.env.cr.dictfetchall():
            self.revenue_interco_total= round(record['tot_revenue_interco'],2)

    def _calc_revenue_pais_conporcentaje(self, pais, costo):
        tot_pais=0.00
        revenue_pais=0.00

        request = "SELECT "+ costo +" as tot_revenue_interco  FROM  revenue_interco" \
                  " WHERE mes='" + str(self.mes) + "' and anio=" + str(self.anio) + " and pais='" + pais + "'"
        self.env.cr.execute(request)
        for record in self.env.cr.dictfetchall():
            tot_pais=record['tot_revenue_interco']
        _logger.info(' PAIS :' + pais +' COSTO ' + costo + '-'+  str(tot_pais))
        if tot_pais and self.revenue_interco_total>0:
            revenue_pais= tot_pais /self.revenue_interco_total
        return revenue_pais

    def _calc_revenue_pais(self, pais, costo):
        tot_pais=0.00
        revenue_pais=0.00

        request = "SELECT "+ costo +" as tot_revenue_interco  FROM  revenue_interco" \
                  " WHERE mes='" + str(self.mes) + "' and anio=" + str(self.anio) + " and pais='" + pais + "'"
        self.env.cr.execute(request)
        for record in self.env.cr.dictfetchall():
            tot_pais=record['tot_revenue_interco']
        _logger.info(' PAIS :' + pais +' COSTO ' + costo + '-'+  str(tot_pais))

        return tot_pais

    def calc_revenue_mex(self):
        self.revenue_interco_mex= self._calc_revenue_pais_conporcentaje("MEX","total")

    def calc_revenue_usa(self):
        self.revenue_interco_usa= self._calc_revenue_pais_conporcentaje("USA","total")

    def calc_revenue_arg(self):
        self.revenue_interco_arg= self._calc_revenue_pais_conporcentaje("ARG","total")

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
    def calc_revenue_total_b1(self):
        self.revenue_interco_total_b1=  round(self.revenue_b1_arg + self.revenue_b1_mex +self.revenue_b1_usa,2)
    def calc_revenue_total_mkt(self):
        self.revenue_interco_total_mkt=  round(self.revenue_mkt_arg + self.revenue_mkt_mex +self.revenue_mkt_usa,2)
#        _logger.info('revenue_mkt_arg:' + str(self.revenue_mkt_arg))
#        _logger.info('revenue_mkt_mex:' + str(self.revenue_mkt_mex))
#        _logger.info('revenue_mkt_usa:' + str(self.revenue_mkt_usa))
#        _logger.info('revenue_interco_total_mkt:' + str(self.revenue_interco_total_mkt))
    def calc_revenue_total_s4(self):
        self.revenue_interco_total_s4=  round(self.revenue_s4_arg + self.revenue_s4_mex +self.revenue_s4_usa,2)
    def calc_revenue_total_nt(self):
            self.revenue_interco_total_nt = round(self.revenue_nt_arg + self.revenue_nt_mex + self.revenue_nt_usa,2)
    def calc_revenue_total_latam(self):
            self.revenue_interco_total_latam = round(self.revenue_tlatam_arg + self.revenue_tlatam_mex + self.revenue_tlatam_usa,2)

            _logger.info('revenue_tlatam_arg:' + str(self.revenue_tlatam_arg))
            _logger.info('revenue_tlatam_mex:' + str(self.revenue_tlatam_mex))
            _logger.info('revenue_tlatam_usa:' + str(self.revenue_tlatam_usa))
            _logger.info('revenue_interco_total_latam:' + str(self.revenue_interco_total_latam))
    def calc_revenue_total_usa(self):
            self.revenue_interco_total_usa = round(self.revenue_tusa_arg + self.revenue_tusa_mex + self.revenue_tusa_usa,2)
            #_logger.info('revenue_tusa_arg:' + str(self.revenue_tusa_arg))
            #_logger.info('revenue_tusa_mex:' + str(self.revenue_tusa_mex))
            #_logger.info('revenue_tusa_usa:' + str(self.revenue_tusa_usa))
            #_logger.info('revenue_interco_total_usa:' + str(self.revenue_interco_total_usa))

    def process_results(self):
        # mejora, recorrer type_results y ejecutar procesos segun , es por subgrupos, es ctaingreso, es RG
        # ***********  PROCESO IC DIRECTO *******************
        icdirecto = self.env['type.results'].search([('resultado', '=', 'IC DIRECTO')], limit=1)
        if icdirecto:
            # Si encuentra la configuracion busco los grupos
            suma_resultado = 0
            suma_grupo_mex = 0
            suma_grupo_usa = 0
            for grupo in icdirecto.grupo:
                # por cada grupo, busco las cuentas relacionadas
                cuentas_mex = self.env['account.account'].search([('grupo', '=', grupo.id),('pais','=','MEX')])
                _logger.info('GRUPO:' + grupo.name + 'CUENTAS MEX:' + str(cuentas_mex))
                for cuenta in cuentas_mex:
                    request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + "  and parent_state='posted' and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio)
                 #   _logger.info('QUERY:' + request)
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['balance_account']:
                            suma_grupo_mex += record['balance_account']
                #-------------USA
                cuentas_usa = self.env['account.account'].search([('grupo', '=', grupo.id), ('pais', '=', 'USA')])
                #_logger.info('GRUPO:' + grupo.name + 'CUENTAS USA:' + str(cuentas_usa))
                for cuenta in cuentas_usa:
                        request = "SELECT  SUM(balance) as credit_account  FROM account_move_line " \
                                  " WHERE account_id = " + str(cuenta.id) + " and parent_state='posted' and date_part('month',date)=" + str(
                            self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"
                        self.env.cr.execute(request)
                        for record in self.env.cr.dictfetchall():
                            if record['credit_account']:
                                suma_grupo_usa += record['credit_account']
                # mando a log el total por grupo
                #_logger.info('TOTAL grupo:' + str(suma_grupo_usa))
                suma_resultado += suma_grupo_usa + suma_grupo_mex
            # calculos finales-----
            self.icdirecto_total = abs(suma_resultado)
            self.icdirecto_mex = abs(suma_grupo_mex)
            self.icdirecto_usa = abs(suma_grupo_usa)

        # *******************- fin IC DIRECTO***************
        #***********  PROCESO RECRUITING antes feb 2023 *******************
        #recruiting = self.env['type.results'].search([('resultado', '=', 'RECRUITING')], limit=1)
        #if recruiting:
            # Si encuentra la configuracion busco los grupos
        #    suma_resultado = 0
        #    for grupo in recruiting.grupo:
                # por cada grupo, busco las cuentas relacionadas
        #        suma_grupo = 0
        #        cuentas = self.env['account.account'].search([('grupo', '=', grupo.id)])
        #        for cuenta in cuentas:
        #            request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
        #                      " WHERE account_id = " + str(cuenta.id) + " and parent_state='posted' and date_part('month',date)=" + str(
        #                self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"
        #            self.env.cr.execute(request)
        #            for record in self.env.cr.dictfetchall():
        #                if record['balance_account']:
        #                    suma_grupo += record['balance_account']
        #        suma_resultado += suma_grupo
        #    self.recruiting_total = suma_resultado
        #    self.recruiting_mex = suma_resultado * self.revenue_interco_mex
        #    self.recruiting_usa = suma_resultado * self.revenue_interco_usa
        #    self.recruiting_arg = suma_resultado * self.revenue_interco_arg

        recruiting = self.env['type.results'].search([('resultado', '=', 'RECRUITING')], limit=1)
        if recruiting:
            suma_mkt, suma_b1, suma_nt, suma_s4, suma_tusa, suma_tlatam = 0, 0, 0, 0, 0, 0
            for grupo in recruiting.grupo:
                suma_b1 = suma_b1 + self.calc_subgrupos('B1', grupo.id)
                suma_nt = suma_nt +  self.calc_subgrupos('NT', grupo.id)
                suma_mkt = suma_mkt + self.calc_subgrupos('MKT', grupo.id)
                suma_s4 = suma_s4 + self.calc_subgrupos('S4', grupo.id)
                suma_tusa = suma_tusa + self.calc_subgrupos('TUSA', grupo.id)
                suma_tlatam = suma_tlatam + self.calc_subgrupos('TLATAM', grupo.id)
            _logger.info('ACA RECRUITING :')
            _logger.info('   suma b1:' + str(suma_b1))
            _logger.info('   suma nt:' + str(suma_nt))
            _logger.info('   suma mkt:' + str(suma_mkt) + ' total_mkt:' + str(self.revenue_interco_total_mkt))
            _logger.info('   suma s4:' + str(suma_s4))
            _logger.info('   suma tlatam:' + str(suma_tlatam))
            _logger.info('   suma talentusa:' + str(suma_tusa))
            # calculos finales-----

            if self.revenue_interco_total_b1 > 0:
                self.recruiting_b1_usa = suma_b1 * (self.revenue_b1_usa / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_usa:' + str(
                    self.revenue_b1_usa / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                porc_mkt_revenue = 0.00
                porc_mkt_revenue = self.revenue_mkt_usa / self.revenue_interco_total_mkt
                self.recruiting_mkt_usa = suma_mkt * porc_mkt_revenue
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_usa:' + str(
                    porc_mkt_revenue))
            if self.revenue_interco_total_nt > 0:
                self.recruiting_nt_usa = suma_nt * (self.revenue_nt_usa / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_usa:' + str(
                    self.revenue_nt_usa / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                self.recruiting_s4_usa = suma_s4 * (self.revenue_s4_usa / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_usa:' + str(
                    self.revenue_s4_usa / self.revenue_interco_total_s4))
            # usa no suma tlatam
            if self.revenue_interco_total_usa > 0:
                self.recruiting_talent_usa = suma_tusa * (self.revenue_tusa_usa / self.revenue_interco_total_usa)
                _logger.info('  suma_tusa:' + str(suma_tusa) + ' revenue_tusa_usa:' + str(
                    self.revenue_tusa_usa / self.revenue_interco_total_usa))

            _logger.info('   b1 usa:' + str(self.recruiting_b1_usa))
            _logger.info('   nt usa:' + str(self.recruiting_nt_usa))
            _logger.info('   mkt usa:' + str(self.recruiting_mkt_usa))
            _logger.info('   s4 usa:' + str(self.recruiting_s4_usa))
            _logger.info('   tusa:' + str(self.recruiting_talent_usa))
            # calculos mexico

            if self.revenue_interco_total_b1 > 0:
                self.recruiting_b1_mex = suma_b1 * (self.revenue_b1_mex / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_mex:' + str(
                    self.revenue_b1_mex / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                porc_mkt_revenue = 0.00
                porc_mkt_revenue = self.revenue_mkt_mex / self.revenue_interco_total_mkt
                self.recruiting_mkt_mex = suma_mkt * porc_mkt_revenue
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_mex:' + str(
                    porc_mkt_revenue))
            if self.revenue_interco_total_nt > 0:
                self.recruiting_nt_mex = suma_nt * (self.revenue_nt_mex / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_mex:' + str(
                    self.revenue_nt_mex / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                self.recruiting_s4_mex = suma_s4 * (self.revenue_s4_mex / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_mex:' + str(
                    self.revenue_s4_mex / self.revenue_interco_total_s4))
            # mex no suma tusa
            if self.revenue_interco_total_latam > 0:
                self.recruiting_talent_mex = suma_tlatam * (self.revenue_tlatam_mex / self.revenue_interco_total_latam)
                _logger.info('  suma_tlatam:' + str(suma_tlatam) + ' revenue_tmex_mex:' + str(
                    self.revenue_tlatam_mex / self.revenue_interco_total_latam))
            self.recruiting_mex = self.recruiting_b1_mex + self.recruiting_nt_mex + self.recruiting_mkt_mex + self.recruiting_s4_mex + self.recruiting_talent_mex
            _logger.info('---------MEX--------- :')

            _logger.info('   b1 mex:' + str(self.recruiting_b1_mex))
            _logger.info('   nt mex:' + str(self.recruiting_nt_mex))
            _logger.info('   mkt mex:' + str(self.recruiting_mkt_mex))
            _logger.info('   s4 mex:' + str(self.recruiting_s4_mex))
            _logger.info('   tlatam:' + str(self.recruiting_talent_mex))

            self.recruiting_total = self.recruiting_usa + self.recruiting_mex
        #*******************- fin recruiting***************
        #---------------- PROCESO MKT -----------------
        mkt = self.env['type.results'].search([('resultado', '=', 'MKT')], limit=1)
        if mkt:
            suma_mkt, suma_b1, suma_nt, suma_s4, suma_tusa, suma_tlatam = suma_tlatam + 0, 0, 0, 0, 0, 0
            for grupo in mkt.grupo:
                suma_b1= suma_b1 + self.calc_subgrupos('B1',grupo.id)
                suma_nt = suma_nt +  self.calc_subgrupos('NT', grupo.id)
                suma_mkt = suma_mkt + self.calc_subgrupos('MKT', grupo.id)
                suma_s4 = suma_s4 + self.calc_subgrupos('S4', grupo.id)
                suma_tusa = suma_tusa + self.calc_subgrupos('TUSA', grupo.id)
                suma_tlatam = suma_tlatam + self.calc_subgrupos('TLATAM', grupo.id)
            _logger.info('ACA GRUPO MKT :')
            _logger.info('   suma b1:' + str(suma_b1))
            _logger.info('   suma nt:' + str(suma_nt))
            _logger.info('   suma mkt:' + str(suma_mkt) + ' total_mkt:' + str(self.revenue_interco_total_mkt))
            _logger.info('   suma s4:' + str(suma_s4))
            _logger.info('   suma tlatam:' + str(suma_tlatam))
            _logger.info('   suma talentusa:' + str(suma_tusa))
            # calculos finales-----
            if self.revenue_interco_total_b1>0:
                self.mkt_b1_usa=suma_b1 * (self.revenue_b1_usa/self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_usa:' + str(
                    self.revenue_b1_usa / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt>0:
                porc_mkt_revenue=0.00
                porc_mkt_revenue=self.revenue_mkt_usa/self.revenue_interco_total_mkt
                self.mkt_mkt_usa=suma_mkt * porc_mkt_revenue
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_usa:' + str(
                porc_mkt_revenue))
            if self.revenue_interco_total_nt>0:
                self.mkt_nt_usa=suma_nt * (self.revenue_nt_usa/self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_usa:' + str(
                    self.revenue_nt_usa / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4>0:
                self.mkt_s4_usa= suma_s4 * (self.revenue_s4_usa / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_usa:' + str(
                    self.revenue_s4_usa / self.revenue_interco_total_s4))
            # usa no suma tlatam
            if self.revenue_interco_total_usa>0:
                self.mkt_talent_usa=suma_tusa * (self.revenue_tusa_usa / self.revenue_interco_total_usa)
                _logger.info('  suma_tusa:' + str(suma_tusa) + ' revenue_tusa_usa:' + str(
                    self.revenue_tusa_usa / self.revenue_interco_total_usa))
            self.mkt_usa = self.mkt_b1_usa + self.mkt_nt_usa + self.mkt_mkt_usa + self.mkt_s4_usa+ self.mkt_talent_usa
            _logger.info('   b1 usa:' + str(self.mkt_b1_usa))
            _logger.info('   nt usa:' + str(self.mkt_nt_usa))
            _logger.info('   mkt usa:' + str(self.mkt_mkt_usa))
            _logger.info('   s4 usa:' + str(self.mkt_s4_usa))
            _logger.info('   tusa:' + str(self.mkt_talent_usa))
              # calculos mexico
            if self.revenue_interco_total_b1 > 0:
                self.mkt_b1_mex = suma_b1 * (self.revenue_b1_mex / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_mex:' + str(
                    self.revenue_b1_mex / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                porc_mkt_revenue = 0.00
                porc_mkt_revenue = self.revenue_mkt_mex / self.revenue_interco_total_mkt
                self.mkt_mkt_mex = suma_mkt * porc_mkt_revenue
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_mex:' + str(
                    porc_mkt_revenue))
            if self.revenue_interco_total_nt > 0:
                self.mkt_nt_mex = suma_nt * (self.revenue_nt_mex / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_mex:' + str(
                    self.revenue_nt_mex / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                self.mkt_s4_mex = suma_s4 * (self.revenue_s4_mex / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_mex:' + str(
                    self.revenue_s4_mex / self.revenue_interco_total_s4))
            # mex no suma tusa
            if self.revenue_interco_total_latam > 0:
                self.mkt_talent_mex = suma_tlatam * (self.revenue_tlatam_mex / self.revenue_interco_total_latam)
                _logger.info('  suma_tlatam:' + str(suma_tlatam) + ' revenue_tmex_mex:' + str(
                    self.revenue_tlatam_mex / self.revenue_interco_total_latam))
            self.mkt_mex = self.mkt_b1_mex + self.mkt_nt_mex + self.mkt_mkt_mex + self.mkt_s4_mex + self.mkt_talent_mex
            _logger.info('---------MEX--------- :')

            _logger.info('   b1 mex:' + str(self.mkt_b1_mex))
            _logger.info('   nt mex:' + str(self.mkt_nt_mex))
            _logger.info('   mkt mex:' + str(self.mkt_mkt_mex))
            _logger.info('   s4 mex:' + str(self.mkt_s4_mex))
            _logger.info('   tlatam:' + str(self.mkt_talent_mex))

            self.mkt_total = self.mkt_usa + self.mkt_mex
        # ---------------- PROCESO OP -----------------
        op = self.env['type.results'].search([('resultado', '=', 'OP')], limit=1)
        if op:
            suma_mkt, suma_b1, suma_nt, suma_s4, suma_tusa, suma_tlatam = suma_tlatam + 0, 0, 0, 0, 0, 0
            for grupo in op.grupo:
                suma_b1= suma_b1 + self.calc_subgrupos('B1',grupo.id)
                suma_nt = suma_nt +  self.calc_subgrupos('NT', grupo.id)
                suma_mkt = suma_mkt + self.calc_subgrupos('MKT', grupo.id)
                suma_s4 = suma_s4 + self.calc_subgrupos('S4', grupo.id)
                suma_tusa = suma_tusa + self.calc_subgrupos('TUSA', grupo.id)
                suma_tlatam = suma_tlatam + self.calc_subgrupos('TLATAM', grupo.id)
            _logger.info('ACA GRUPO OP :')
            _logger.info('   suma b1:' + str(suma_b1))
            _logger.info('   suma nt:' + str(suma_nt))
            _logger.info('   suma mkt:' + str(suma_mkt) + ' total_mkt:' + str(self.revenue_interco_total_mkt))
            _logger.info('   suma s4:' + str(suma_s4))
            _logger.info('   suma tlatam:' + str(suma_tlatam))
            _logger.info('   suma talentusa:' + str(suma_tusa))
            # calculos finales-----

            if self.revenue_interco_total_b1>0:
                self.op_b1_usa=suma_b1 * (self.revenue_b1_usa/self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_usa:' + str(
                    self.revenue_b1_usa / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt>0:
                self.op_mkt_usa=suma_mkt * (self.revenue_mkt_usa/self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_usa:' + str(
                    self.revenue_mkt_usa / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt>0:
                self.op_nt_usa=suma_nt * (self.revenue_nt_usa/self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_usa:' + str(
                    self.revenue_nt_usa / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4>0:
                self.op_s4_usa= suma_s4 * (self.revenue_s4_usa / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_usa:' + str(
                    self.revenue_s4_usa / self.revenue_interco_total_s4))
            # usa no suma tlatam
            if self.revenue_interco_total_usa>0:
                self.op_talent_usa=suma_tusa * (self.revenue_tusa_usa / self.revenue_interco_total_usa)
                _logger.info('  suma_tusa:' + str(suma_tusa) + ' revenue_tusa_usa:' + str(
                    self.revenue_tusa_usa / self.revenue_interco_total_usa))
            self.op_usa = self.op_b1_usa + self.op_nt_usa + self.op_mkt_usa + self.op_s4_usa+ self.op_talent_usa
            _logger.info('ACA GRUPO OPERACIONES :')

            _logger.info('   b1 usa:' + str(self.op_b1_usa))
            _logger.info('   nt usa:' + str(self.op_nt_usa))
            _logger.info('   mkt usa:' + str(self.op_mkt_usa))
            _logger.info('   s4 usa:' + str(self.op_s4_usa))
            _logger.info('   tusa:' + str(self.op_talent_usa))
            # calculos mexico

            if self.revenue_interco_total_b1 > 0:
                self.op_b1_mex = suma_b1 * (self.revenue_b1_mex / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_mex:' + str(
                    self.revenue_b1_mex / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                self.op_mkt_mex = suma_mkt * self.revenue_mkt_mex / self.revenue_interco_total_mkt
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_mex:' + str(
                    self.revenue_mkt_mex / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                self.op_nt_mex = suma_nt * (self.revenue_nt_mex / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_mex:' + str(
                    self.revenue_nt_mex / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                self.op_s4_mex = suma_s4 * (self.revenue_s4_mex / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_mex:' + str(
                    self.revenue_s4_mex / self.revenue_interco_total_s4))
            # mex no suma tusa
            if self.revenue_interco_total_latam > 0:
                self.op_talent_mex = suma_tlatam * (self.revenue_tlatam_mex / self.revenue_interco_total_latam)
                _logger.info('  suma_tlatam:' + str(suma_tlatam) + ' revenue_tmex_mex:' + str(
                    self.revenue_tlatam_mex / self.revenue_interco_total_latam))
            self.op_mex = self.op_b1_mex + self.op_nt_mex + self.op_mkt_mex + self.op_s4_mex +  self.op_talent_mex
            _logger.info('---------MEX--------- :')

            _logger.info('   b1 mex:' + str(self.op_b1_mex))
            _logger.info('   nt mex:' + str(self.op_nt_mex))
            _logger.info('   mkt mex:' + str(self.op_mkt_mex))
            _logger.info('   s4 mex:' + str(self.op_s4_mex))
            _logger.info('   tlatam:' + str(self.op_talent_mex))

            # calculos Arg
            op_b1_arg, op_nt_arg, op_mkt_arg, op_s4_arg, op_arg_tlatam, op_mkt_arg = 0, 0, 0, 0, 0, 0
            if self.revenue_interco_total_b1 > 0:
                op_b1_arg = suma_b1 * (self.revenue_b1_arg / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_arg:' + str(
                    self.revenue_b1_arg / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                op_mkt_arg = suma_mkt * self.revenue_mkt_arg / self.revenue_interco_total_mkt
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_arg:' + str(
                    self.revenue_mkt_arg / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                op_nt_arg = suma_nt * (self.revenue_nt_arg / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_arg:' + str(
                    self.revenue_nt_arg / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                op_s4_arg = suma_s4 * (self.revenue_s4_arg / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_arg:' + str(
                    self.revenue_s4_arg / self.revenue_interco_total_s4))
            # arg no suma tusa
            if self.revenue_interco_total_latam > 0:
                op_arg_tlatam = suma_tlatam * (self.revenue_tlatam_arg / self.revenue_interco_total_latam)
                _logger.info('  suma_tlatam:' + str(suma_tlatam) + ' revenue_targ_arg:' + str(
                    self.revenue_tlatam_arg / self.revenue_interco_total_latam))
            self.op_arg = op_b1_arg + op_nt_arg + op_mkt_arg + op_s4_arg + op_arg_tlatam
            _logger.info('---------MEX--------- :')

            _logger.info('   b1 arg:' + str(op_b1_arg))
            _logger.info('   nt arg:' + str(op_nt_arg))
            _logger.info('   mkt arg:' + str(op_mkt_arg))
            _logger.info('   s4 arg:' + str(op_s4_arg))
            _logger.info('   tlatam:' + str(op_arg_tlatam))

            self.op_total = self.op_usa + self.op_mex + self.op_arg
        # ---------------- PROCESO SALES -----------------
        sales = self.env['type.results'].search([('resultado', '=', 'SALES')], limit=1)
        if sales:
            suma_mkt, suma_b1, suma_nt, suma_s4, suma_tusa, suma_tlatam = suma_tlatam + 0, 0, 0, 0, 0, 0
            for grupo in sales.grupo:
                suma_b1 = suma_b1 + self.calc_subgrupos('B1', grupo.id)
                suma_nt = suma_nt +  self.calc_subgrupos('NT', grupo.id)
                suma_mkt = suma_mkt + self.calc_subgrupos('MKT', grupo.id)
                suma_s4 = suma_s4 + self.calc_subgrupos('S4', grupo.id)
                suma_tusa = suma_tusa + self.calc_subgrupos('TUSA', grupo.id)
                suma_tlatam = suma_tlatam + self.calc_subgrupos('TLATAM', grupo.id)
            _logger.info('ACA GRUPO SALES :')
            _logger.info('   suma b1:' + str(suma_b1))
            _logger.info('   suma nt:' + str(suma_nt))
            _logger.info('   suma mkt:' + str(suma_mkt) )
            _logger.info('   suma s4:' + str(suma_s4))
            _logger.info('   suma tlatam:' + str(suma_tlatam))
            _logger.info('   suma talentusa:' + str(suma_tusa))
            # calculos finales-----

            if self.revenue_interco_total_b1 > 0:
                self.sales_b1_usa = suma_b1 * (self.revenue_b1_usa / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_usa:' + str(
                    self.revenue_b1_usa / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                self.sales_mkt_usa = suma_mkt * (self.revenue_mkt_usa / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_usa:' + str(
                    self.revenue_mkt_usa / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                self.sales_nt_usa = suma_nt * (self.revenue_nt_usa / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_usa:' + str(
                    self.revenue_nt_usa / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                self.sales_s4_usa = suma_s4 * (self.revenue_s4_usa / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_usa:' + str(
                    self.revenue_s4_usa / self.revenue_interco_total_s4))
            # usa no suma tlatam
            if self.revenue_interco_total_usa > 0:
                self.sales_talent_usa = suma_tusa * (self.revenue_tusa_usa / self.revenue_interco_total_usa)
                _logger.info('  suma_tusa:' + str(suma_tusa) + ' revenue_tusa_usa:' + str(
                    self.revenue_tusa_usa / self.revenue_interco_total_usa))
            self.sales_usa = self.sales_b1_usa + self.sales_nt_usa + self.sales_mkt_usa + self.sales_s4_usa + self.sales_talent_usa
            _logger.info('   b1 usa:' + str(self.sales_b1_usa))
            _logger.info('   nt usa:' + str(self.sales_nt_usa))
            _logger.info('   mkt usa:' + str(self.sales_mkt_usa))
            _logger.info('   s4 usa:' + str(self.sales_s4_usa))
            _logger.info('   tusa:' + str(self.sales_talent_usa))

            # calculos mexico

            if self.revenue_interco_total_b1 > 0:
                self.sales_b1_mex = suma_b1 * (self.revenue_b1_mex / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_mex:' + str(
                    self.revenue_b1_mex / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                self.sales_mkt_mex = suma_mkt * ( self.revenue_mkt_mex / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_sales_mex:' + str(
                    self.revenue_mkt_mex / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                self.sales_nt_mex = suma_nt * (self.revenue_nt_mex / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_mex:' + str(
                    self.revenue_nt_mex / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                self.sales_s4_mex = suma_s4 * (self.revenue_s4_mex / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_mex:' + str(
                    self.revenue_s4_mex / self.revenue_interco_total_s4))
            # mex no suma tusa
            if self.revenue_interco_total_latam > 0:
                sales_mex_tlatam = suma_tlatam * (self.revenue_tlatam_mex / self.revenue_interco_total_latam)
                _logger.info('  suma_tlatam:' + str(suma_tlatam) + ' revenue_tmex_mex:' + str(
                    self.revenue_tlatam_mex / self.revenue_interco_total_latam))
            self.sales_mex = self.sales_b1_mex + self.sales_nt_mex + self.sales_mkt_mex + self.sales_s4_mex + self.sales_talent_mex
            _logger.info('---------MEX--------- :')

            _logger.info('   b1 mex:' + str(self.sales_b1_mex))
            _logger.info('   nt mex:' + str(self.sales_nt_mex))
            _logger.info('   mkt mex:' + str(self.sales_mkt_mex))
            _logger.info('   s4 mex:' + str(self.sales_s4_mex))
            _logger.info('   tlatam:' + str(self.sales_talent_mex))

            self.sales_total = self.sales_usa + self.sales_mex
        # ---------------- PROCESO PRESALES -----------------
        presales = self.env['type.results'].search([('resultado', '=', 'PRESALES')], limit=1)
        if presales:
            suma_mkt, suma_b1, suma_nt, suma_s4, suma_tusa, suma_tlatam = suma_tlatam + 0, 0, 0, 0, 0, 0
            for grupo in presales.grupo:
                suma_b1 = suma_b1 + self.calc_subgrupos('B1', grupo.id)
                suma_nt = suma_nt +  self.calc_subgrupos('NT', grupo.id)
                suma_mkt = suma_mkt + self.calc_subgrupos('MKT', grupo.id)
                suma_s4 = suma_s4 + self.calc_subgrupos('S4', grupo.id)
                suma_tusa = suma_tusa + self.calc_subgrupos('TUSA', grupo.id)
                suma_tlatam = suma_tlatam + self.calc_subgrupos('TLATAM', grupo.id)
            _logger.info('ACA GRUPO PRESALES :')
            _logger.info('   suma b1:' + str(suma_b1))
            _logger.info('   suma nt:' + str(suma_nt))
            _logger.info('   suma mkt:' + str(suma_mkt))
            _logger.info('   suma s4:' + str(suma_s4))
            _logger.info('   suma tlatam:' + str(suma_tlatam))
            _logger.info('   suma talentusa:' + str(suma_tusa))
            # calculos finales-----

            if self.revenue_interco_total_b1 > 0:
                self.presales_b1_usa = suma_b1 * (self.revenue_b1_usa / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_usa:' + str(
                    self.revenue_b1_usa / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                self.presales_mkt_usa = suma_mkt * (self.revenue_mkt_usa / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_usa:' + str(
                    self.revenue_mkt_usa / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                self.presales_nt_usa = suma_nt * (self.revenue_nt_usa / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_usa:' + str(
                    self.revenue_nt_usa / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                self.presales_s4_usa = suma_s4 * (self.revenue_s4_usa / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_usa:' + str(
                    self.revenue_s4_usa / self.revenue_interco_total_s4))
            # usa no suma tlatam
            if self.revenue_interco_total_usa > 0:
                self.presales_talent_usa = suma_tusa * (self.revenue_tusa_usa / self.revenue_interco_total_usa)
                _logger.info('  suma_tusa:' + str(suma_tusa) + ' revenue_tusa_usa:' + str(
                    self.revenue_tusa_usa / self.revenue_interco_total_usa))
            # busco en ctas comunes

            self.presales_usa = self.presales_b1_usa + self.presales_nt_usa + self.presales_mkt_usa + self.presales_s4_usa + self.presales_talent_usa
            _logger.info('   b1 usa:' + str(self.presales_b1_usa))
            _logger.info('   nt usa:' + str(self.presales_nt_usa))
            _logger.info('   mkt usa:' + str(self.presales_mkt_usa))
            _logger.info('   s4 usa:' + str(self.presales_s4_usa))
            _logger.info('   tlatam:' + str(self.presales_talent_usa))
            # calculos mexico

            if self.revenue_interco_total_b1 > 0:
                self.presales_b1_mex = suma_b1 * (self.revenue_b1_mex / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_mex:' + str(
                    self.revenue_b1_mex / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                self.presales_mkt_mex = suma_mkt * (self.revenue_mkt_mex / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_presales_mex:' + str(
                    self.revenue_mkt_mex / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                self.presales_nt_mex = suma_nt * (self.revenue_nt_mex / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_mex:' + str(
                    self.revenue_nt_mex / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                self.presales_s4_mex = suma_s4 * (self.revenue_s4_mex / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_mex:' + str(
                    self.revenue_s4_mex / self.revenue_interco_total_s4))
            # mex no suma tusa
            if self.revenue_interco_total_latam > 0:
                self.presales_talent_mex= suma_tlatam * (self.revenue_tlatam_mex / self.revenue_interco_total_latam)
                _logger.info('  suma_tlatam:' + str(suma_tlatam) + ' revenue_tmex_mex:' + str(
                    self.revenue_tlatam_mex / self.revenue_interco_total_latam))
            self.presales_mex = self.presales_b1_mex + self.presales_nt_mex + self.presales_mkt_mex + self.presales_s4_mex + self.presales_talent_mex
            _logger.info('---------MEX--------- :')

            _logger.info('   b1 mex:' + str(self.presales_b1_mex))
            _logger.info('   nt mex:' + str(self.presales_nt_mex))
            _logger.info('   mkt mex:' + str(self.presales_mkt_mex))
            _logger.info('   s4 mex:' + str(self.presales_s4_mex))
            _logger.info('   tlatam:' + str(self.presales_talent_mex))

            self.presales_total = self.presales_usa + self.presales_mex
        # ---------------- PROCESO CI -----------------
        ciun = self.env['type.results'].search([('resultado', '=', 'CI-UN')], limit=1)
        if ciun:
            suma_mkt, suma_b1, suma_nt, suma_s4, suma_tusa, suma_tlatam = suma_tlatam + 0, 0, 0, 0, 0, 0
            for grupo in ciun.grupo:
                suma_b1 = suma_b1 + self.calc_subgrupos('B1', grupo.id)
                suma_nt = suma_nt +  self.calc_subgrupos('NT', grupo.id)
                suma_mkt = suma_mkt + self.calc_subgrupos('MKT', grupo.id)
                suma_s4 = suma_s4 + self.calc_subgrupos('S4', grupo.id)
                suma_tusa = suma_tusa + self.calc_subgrupos('TUSA', grupo.id)
                suma_tlatam = suma_tlatam + self.calc_subgrupos('TLATAM', grupo.id)
            _logger.info('ACA GRUPO CI-UN :')
            _logger.info('   suma b1:' + str(suma_b1))
            _logger.info('   suma nt:' + str(suma_nt))
            _logger.info('   suma mkt:' + str(suma_mkt))
            _logger.info('   suma s4:' + str(suma_s4))
            _logger.info('   suma tlatam:' + str(suma_tlatam))
            _logger.info('   suma talentusa:' + str(suma_tusa))
            # calculos finales-----
            if self.revenue_interco_total_b1 > 0:
                self.ciun_b1_usa = suma_b1 * (self.revenue_b1_usa / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_usa:' + str(
                    self.revenue_b1_usa / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                self.ciun_mkt_usa = suma_mkt * (self.revenue_mkt_usa / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_usa:' + str(
                    self.revenue_mkt_usa / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                self.ciun_nt_usa = suma_nt * (self.revenue_nt_usa / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_usa:' + str(
                    self.revenue_nt_usa / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                self.ciun_s4_usa = suma_s4 * (self.revenue_s4_usa / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_usa:' + str(
                    self.revenue_s4_usa / self.revenue_interco_total_s4))
            # usa no suma tlatam
            if self.revenue_interco_total_usa > 0:
                self.ciun_talent_usa = suma_tusa * (self.revenue_tusa_usa / self.revenue_interco_total_usa)
                _logger.info('  suma_tusa:' + str(suma_tusa) + ' revenue_tusa_usa:' + str(
                    self.revenue_tusa_usa / self.revenue_interco_total_usa))
            # busco en ctas comunes

            self.ciun_usa = self.ciun_b1_usa + self.ciun_nt_usa + self.ciun_mkt_usa + self.ciun_s4_usa + self.ciun_talent_usa
            _logger.info('   b1 usa:' + str(self.ciun_b1_usa))
            _logger.info('   nt usa:' + str(self.ciun_nt_usa))
            _logger.info('   mkt usa:' + str(self.ciun_mkt_usa))
            _logger.info('   s4 usa:' + str(self.ciun_s4_usa))
            _logger.info('   tlatam:' + str(self.ciun_talent_usa))
            # calculos mexico
            if self.revenue_interco_total_b1 > 0:
                self.ciun_b1_mex = suma_b1 * (self.revenue_b1_mex / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_mex:' + str(
                    self.revenue_b1_mex / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                self.ciun_mkt_mex = suma_mkt * (self.revenue_mkt_mex / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_ciun_mex:' + str(
                    self.revenue_mkt_mex / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                self.ciun_nt_mex = suma_nt * (self.revenue_nt_mex / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_mex:' + str(
                    self.revenue_nt_mex / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                self.ciun_s4_mex = suma_s4 * (self.revenue_s4_mex / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_mex:' + str(
                    self.revenue_s4_mex / self.revenue_interco_total_s4))
            # mex no suma tusa
            if self.revenue_interco_total_latam > 0:
                self.ciun_talent_mex = suma_tlatam * (self.revenue_tlatam_mex / self.revenue_interco_total_latam)
                _logger.info('  suma_tlatam:' + str(suma_tlatam) + ' revenue_tmex_mex:' + str(
                    self.revenue_tlatam_mex / self.revenue_interco_total_latam))
            self.ciun_mex = self.ciun_b1_mex + self.ciun_nt_mex + self.ciun_mkt_mex + self.ciun_s4_mex + self.ciun_talent_mex
            _logger.info('---------MEX--------- :')

            _logger.info('   b1 mex:' + str(self.ciun_b1_mex))
            _logger.info('   nt mex:' + str(self.ciun_nt_mex))
            _logger.info('   mkt mex:' + str(self.ciun_mkt_mex))
            _logger.info('   s4 mex:' + str(self.ciun_s4_mex))
            _logger.info('   tlatam:' + str(self.ciun_talent_mex))

        self.ciun_total = self.ciun_usa + self.ciun_mex
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
                    request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + " and parent_state='posted' and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio) +  " and company_id=1"
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['balance_account']:
                            suma_grupo_usa += record['balance_account']
                # -------------MEX
                cuentas_mex = self.env['account.account'].search([('grupo', '=', grupo.id), ('pais', '=', 'MEX')])
         #       _logger.info('GRUPO:' + grupo.name + 'CUENTAS MEX:' + str(cuentas_usa))
                for cuenta in cuentas_mex:
                    request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + " and parent_state='posted' and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio) +  " and company_id=1"
                    _logger.info('QUERY:' + request)
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['balance_account']:
                            suma_grupo_mex += record['balance_account']

            # calculos finales-----
            # _logger.info('GRUPO COMISIONES UN')
            # _logger.info(' total:' + str(suma_grupo_usa))
            self.comi_usa = suma_grupo_usa
            self.comi_mex =  suma_grupo_mex
            self.comi_total = suma_grupo_usa + suma_grupo_mex
        # ---------------fin proceso Comisiones-Talent--------------------
        # ---------------- PROCESO comisiones mkt  sin uso feb 2023 -----------------
        # commkt = self.env['type.results'].search([('resultado', '=', 'COMISIONES MKT')], limit=1)
        # if commkt:
        #     # en excel solo toma a un grupo para cda cuenta contable, igual hago la suma por si hubieran mas
        #     # -------------USA
        #     suma_grupo_usa = 0
        #     suma_grupo_mex = 0
        #     for grupo in commkt.grupo:
        #         cuentas_usa = self.env['account.account'].search([('grupo', '=', grupo.id), ('pais', '=', 'USA')])
        #         _logger.info('GRUPO:' + grupo.name + 'CUENTAS USA:' + str(cuentas_usa))
        #             request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
        #         for cuenta in cuentas_usa:
        #                       " WHERE account_id = " + str(cuenta.id) + "  and parent_state='posted' and date_part('month',date)=" + str(
        #                 self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"
        #             self.env.cr.execute(request)
        #             for record in self.env.cr.dictfetchall():
        #                 if record['balance_account']:
        #                     suma_grupo_usa += record['balance_account']
        #         # -------------MEX
        #         cuentas_mex = self.env['account.account'].search([('grupo', '=', grupo.id), ('pais', '=', 'MEX')])
        #    #     _logger.info('GRUPO:' + grupo.name + 'CUENTAS MEX:' + str(cuentas_usa))
        #         for cuenta in cuentas_mex:
        #             request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
        #                       " WHERE account_id = " + str(cuenta.id) + " and parent_state='posted' and date_part('month',date)=" + str(
        #                 self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"
        #      #       _logger.info('QUERY:' + request)
        #             self.env.cr.execute(request)
        #             for record in self.env.cr.dictfetchall():
        #                 if record['balance_account']:
        #                     suma_grupo_mex += record['balance_account']
        #
        #     # calculos finales-----
        #     # _logger.info('GRUPO COMISIONES MKT')
        #     # _logger.info(' total:' + str(suma_grupo_usa))
        #     self.comimkt_usa = suma_grupo_usa
        #     self.comimkt_mex = suma_grupo_mex
        #     self.comimkt_total = suma_grupo_usa + suma_grupo_mex
        #***************  FIN comisiones kmt **************
        # ---------------- PROCESO leads mkt  UN directo - PASA  a indirecto-----------------
        leads = self.env['type.results'].search([('resultado', '=', 'LEADS MKT')], limit=1)
        if leads:
            suma_mkt, suma_b1, suma_nt, suma_s4, suma_tusa, suma_tlatam = suma_tlatam + 0, 0, 0, 0, 0, 0
            for grupo in ciun.grupo:
                suma_b1 = suma_b1 + self.calc_subgrupos('B1', grupo.id)
                suma_nt = suma_nt +  self.calc_subgrupos('NT', grupo.id)
                suma_mkt = suma_mkt + self.calc_subgrupos('MKT', grupo.id)
                suma_s4 = suma_s4 + self.calc_subgrupos('S4', grupo.id)
                suma_tusa = suma_tusa + self.calc_subgrupos('TUSA', grupo.id)
                suma_tlatam = suma_tlatam + self.calc_subgrupos('TLATAM', grupo.id)
            # calculos finales-----
            if self.revenue_interco_total_b1 > 0:
                self.leadsmkt_b1_usa = suma_b1 * (self.revenue_b1_usa / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_usa:' + str(
                    self.revenue_b1_usa / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                self.leadsmkt_mkt_usa = suma_mkt * (self.revenue_mkt_usa / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_usa:' + str(
                    self.revenue_mkt_usa / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                self.leadsmkt_nt_usa = suma_nt * (self.revenue_nt_usa / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_usa:' + str(
                    self.revenue_nt_usa / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                self.leadsmkt_s4_usa = suma_s4 * (self.revenue_s4_usa / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_usa:' + str(
                    self.revenue_s4_usa / self.revenue_interco_total_s4))
            if self.revenue_interco_total_usa > 0:
                self.leadsmkt_talent_usa = suma_tusa * (self.revenue_tusa_usa / self.revenue_interco_total_usa)
                _logger.info('  suma_tusa:' + str(suma_tusa) + ' revenue_tusa_usa:' + str(
                    self.revenue_tusa_usa / self.revenue_interco_total_usa))

            self.leadsmkt_usa = self.leadsmkt_b1_usa + self.leadsmkt_nt_usa + self.leadsmkt_mkt_usa + self.leadsmkt_s4_usa + self.leadsmkt_talent_usa
            _logger.info('   b1 usa:' + str(self.leadsmkt_b1_usa))
            _logger.info('   nt usa:' + str(self.leadsmkt_nt_usa))
            _logger.info('   mkt usa:' + str(self.leadsmkt_mkt_usa))
            _logger.info('   s4 usa:' + str(self.leadsmkt_s4_usa))
            _logger.info('   tlatam:' + str(self.leadsmkt_talent_usa))
            # calculos mexico
            if self.revenue_interco_total_b1 > 0:
                self.leadsmkt_b1_mex = suma_b1 * (self.revenue_b1_mex / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_mex:' + str(
                    self.revenue_b1_mex / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                self.leadsmkt_mkt_mex = suma_mkt * (self.revenue_mkt_mex / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_leadsmkt_mex:' + str(
                    self.revenue_mkt_mex / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                self.leadsmkt_nt_mex = suma_nt * (self.revenue_nt_mex / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_mex:' + str(
                    self.revenue_nt_mex / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                self.leadsmkt_s4_mex = suma_s4 * (self.revenue_s4_mex / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_mex:' + str(
                    self.revenue_s4_mex / self.revenue_interco_total_s4))
            # mex no suma tusa
            if self.revenue_interco_total_latam > 0:
                self.leadsmkt_talent_mex = suma_tlatam * (self.revenue_tlatam_mex / self.revenue_interco_total_latam)
                _logger.info('  suma_tlatam:' + str(suma_tlatam) + ' revenue_tmex_mex:' + str(
                    self.revenue_tlatam_mex / self.revenue_interco_total_latam))
            self.leadsmkt_mex = self.leadsmkt_b1_mex + self.leadsmkt_nt_mex + self.leadsmkt_mkt_mex + self.leadsmkt_s4_mex + self.leadsmkt_talent_mex
            _logger.info('---------MEX--------- :')

            _logger.info('   b1 mex:' + str(self.leadsmkt_b1_mex))
            _logger.info('   nt mex:' + str(self.leadsmkt_nt_mex))
            _logger.info('   mkt mex:' + str(self.leadsmkt_mkt_mex))
            _logger.info('   s4 mex:' + str(self.leadsmkt_s4_mex))
            _logger.info('   tlatam:' + str(self.leadsmkt_talent_mex))

        self.leadsmkt_total = self.leadsmkt_usa + self.leadsmkt_mex

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
                for cuenta in cuentas_usa:
                    request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + " and parent_state='posted'  and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['balance_account']:
                            suma_grupo_usa += record['balance_account']
                # -------------MEX
                cuentas_mex = self.env['account.account'].search(
                    [('grupo', '=', grupo.id), ('pais', '=', 'MEX')])
       #         _logger.info('GRUPO:' + grupo.name + 'CUENTAS MEX:' + str(cuentas_usa))
                for cuenta in cuentas_mex:
                    request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + " and parent_state='posted' and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"

                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['balance_account']:
                            suma_grupo_mex += record['balance_account']

                # calculos finales-----
                # _logger.info('GRUPO COMISIONES UN')
                # _logger.info(' total:' + str(suma_grupo_usa))
                self.comun_usa = suma_grupo_usa
                self.comun_mex = suma_grupo_mex
                self.comun_total = suma_grupo_usa + suma_grupo_mex

        #*************** CALCULO CI*************************
        # # CALCULA SOBRE SUMA DE GRUPOS DIRECTO
        # comisiones = self.env['type.results'].search([('resultado', '=', 'CI')], limit=1)
        # if comisiones:
        #     # Si encuentra la configuracion busco los grupos
        #     suma_resultado = 0
        #     for grupo in comisiones.grupo:
        #         cuentas_comunes= self.env['intercompany.cost.ctascomunes'].search([('grupo_id','=',grupo.id)])
        #         _logger.info('grupo ci:' + str(grupo.id))
        #         _logger.info('cuentas_comunes:' + str(cuentas_comunes))
        #         suma_grupo=0
        #         if cuentas_comunes:
        #             for record_cta in cuentas_comunes:
        #                 _logger.info('GRUPO CI :' + grupo.name + 'CUENTAS comunes:' + str(record_cta))
        #                 request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
        #                           " WHERE account_id = " + str(record_cta.account_id.id) + " and parent_state='posted'  " \
        #                                                                            " and analytic_account_id=" + str(
        #                     record_cta.centro_costos.id) + " and date_part('month',date)=" + str(
        #                     self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"
        #                 _logger.info('QUERY:' + request)
        #                 self.env.cr.execute(request)
        #                 for record in self.env.cr.dictfetchall():
        #                     if record['balance_account']:
        #                         _logger.info(
        #                             '  parcial cta comun :' + str(record_cta['id']) + '- centro costo :' + str(record_cta['centro_costos']) + ' $' + str(
        #                                 record['balance_account']))
        #                         suma_grupo += record['balance_account']
        #             _logger.info('TOTAL grupo:' + str(suma_grupo))
        #             suma_resultado += suma_grupo
        #         else:
        #             #sino tenia datos en ctas comunes busco las cuentas relacionadas al grupo en su totalidad
        #             suma_grupo = 0
        #             cuentas = self.env['account.account'].search([('grupo', '=', grupo.id)])
        #             _logger.info('GRUPO CI :' + grupo.name + 'CUENTAS:' + str(cuentas))
        #             for cuenta in cuentas:
        #                 request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
        #                           " WHERE account_id = " + str(cuenta.id) + " and parent_state='posted' and date_part('month',date)=" + str(
        #                     self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"
        #                 _logger.info(request)
        #                 self.env.cr.execute(request)
        #                 for record in self.env.cr.dictfetchall():
        #                     if record['balance_account']:
        #                         suma_grupo += record['balance_account']
        #
        #             # mando a log el total por grupo
        #             _logger.info('TOTAL grupo:' + str(suma_grupo))
        #             suma_resultado += suma_grupo
        #     # calculos finales-----
        #     _logger.info('suma total CI:' + str(suma_resultado))
        #     _logger.info('revenue mex:' + str(self.revenue_interco_mex))
        #     _logger.info('revenue usa:' + str(self.revenue_interco_usa))
        #     self.ci_mex = (suma_resultado * self.revenue_interco_mex)
        #     self.ci_usa = (suma_resultado * self.revenue_interco_usa)
        #     #self.ci_arg = (suma_resultado * self.revenue_interco_arg)
        #     self.ci_total = self.ci_mex + self.ci_usa
        # *************** CALCULO CI*************************
        # CALCULA SOBRE SUMA DE GRUPOS INDIRECTO
        comisiones = self.env['type.results'].search([('resultado', '=', 'CI')], limit=1)
        if comisiones:
            suma_mkt, suma_b1, suma_nt, suma_s4, suma_tusa, suma_tlatam = suma_tlatam + 0, 0, 0, 0, 0, 0
            for grupo in ciun.grupo:
                suma_b1 = suma_b1 + self.calc_subgrupos('B1', grupo.id)
                suma_nt = suma_nt +  self.calc_subgrupos('NT', grupo.id)
                suma_mkt = suma_mkt + self.calc_subgrupos('MKT', grupo.id)
                suma_s4 = suma_s4 + self.calc_subgrupos('S4', grupo.id)
                suma_tusa = suma_tusa + self.calc_subgrupos('TUSA', grupo.id)
                suma_tlatam = suma_tlatam + self.calc_subgrupos('TLATAM', grupo.id)
            _logger.info('ACA GRUPO CI :')
            _logger.info('   suma b1:' + str(suma_b1))
            _logger.info('   suma nt:' + str(suma_nt))
            _logger.info('   suma mkt:' + str(suma_mkt))
            _logger.info('   suma s4:' + str(suma_s4))
            _logger.info('   suma tlatam:' + str(suma_tlatam))
            _logger.info('   suma talentusa:' + str(suma_tusa))
            # calculos finales-----
            if self.revenue_interco_total_b1 > 0:
                self.ci_b1_usa = suma_b1 * (self.revenue_b1_usa / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_usa:' + str(
                    self.revenue_b1_usa / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                self.ci_mkt_usa = suma_mkt * (self.revenue_mkt_usa / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_usa:' + str(
                    self.revenue_mkt_usa / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                self.ci_nt_usa = suma_nt * (self.revenue_nt_usa / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_usa:' + str(
                    self.revenue_nt_usa / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                self.ci_s4_usa = suma_s4 * (self.revenue_s4_usa / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_usa:' + str(
                    self.revenue_s4_usa / self.revenue_interco_total_s4))
                # usa no suma tlatam
            if self.revenue_interco_total_usa > 0:
                self.ci_talent_usa = suma_tusa * (self.revenue_tusa_usa / self.revenue_interco_total_usa)
                _logger.info('  suma_tusa:' + str(suma_tusa) + ' revenue_tusa_usa:' + str(
                    self.revenue_tusa_usa / self.revenue_interco_total_usa))
                # busco en ctas comunes

            self.ci_usa = self.ci_b1_usa + self.ci_nt_usa + self.ci_mkt_usa + self.ci_s4_usa + self.ci_talent_usa
            _logger.info('   b1 usa:' + str(self.ci_b1_usa))
            _logger.info('   nt usa:' + str(self.ci_nt_usa))
            _logger.info('   mkt usa:' + str(self.ci_mkt_usa))
            _logger.info('   s4 usa:' + str(self.ci_s4_usa))
            _logger.info('   tlatam:' + str(self.ci_talent_usa))
            # calculos mexico
            if self.revenue_interco_total_b1 > 0:
                self.ci_b1_mex = suma_b1 * (self.revenue_b1_mex / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_mex:' + str(
                    self.revenue_b1_mex / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                self.ci_mkt_mex = suma_mkt * (self.revenue_mkt_mex / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_ci_mex:' + str(
                    self.revenue_mkt_mex / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                self.ci_nt_mex = suma_nt * (self.revenue_nt_mex / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_mex:' + str(
                    self.revenue_nt_mex / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                self.ci_s4_mex = suma_s4 * (self.revenue_s4_mex / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_mex:' + str(
                    self.revenue_s4_mex / self.revenue_interco_total_s4))
            # mex no suma tusa
            if self.revenue_interco_total_latam > 0:
                self.ci_talent_mex = suma_tlatam * (self.revenue_tlatam_mex / self.revenue_interco_total_latam)
                _logger.info('  suma_tlatam:' + str(suma_tlatam) + ' revenue_tmex_mex:' + str(
                    self.revenue_tlatam_mex / self.revenue_interco_total_latam))
            self.ci_mex = self.ci_b1_mex + self.ci_nt_mex + self.ci_mkt_mex + self.ci_s4_mex + self.ci_talent_mex
            _logger.info('---------MEX--------- :')

            _logger.info('   b1 mex:' + str(self.ci_b1_mex))
            _logger.info('   nt mex:' + str(self.ci_nt_mex))
            _logger.info('   mkt mex:' + str(self.ci_mkt_mex))
            _logger.info('   s4 mex:' + str(self.ci_s4_mex))
            _logger.info('   tlatam:' + str(self.ci_talent_mex))

        self.ci_total = self.ci_usa + self.ci_mex

        #--------------- FIN CALCULOS -----------------
        self.state = 'checkpoint'

    #**********************  FIN PROCESO******************
    def calc_subgrupos(self,subgrupo, grupo_id):
        suma_subgrupo = 0
        request_cta="SELECT cta.id as id FROM account_account as cta INNER JOIN intercompany_cost_subgroups as subgrup ON subgrup.grupo_id= cta.grupo " \
                    "WHERE grupo=" + str(grupo_id) + " and subgrup.distribucion_costo='"+ subgrupo +"'  and subgrup.id=cta.subgrupo"

        #_logger.info('QUERY:' + request_cta)
        self.env.cr.execute(request_cta)
        for record_cta in self.env.cr.dictfetchall():
            request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
                      " WHERE account_id = " + str(record_cta['id']) +  " and parent_state='posted'  " \
                        "and date_part('month',date)=" + str(self.mes) +" and date_part('year',date)=" + str(self.anio) + " and company_id=1"
            _logger.info('QUERY:' + request)
            self.env.cr.execute(request)
            for record in self.env.cr.dictfetchall():
                if record['balance_account']:
                    _logger.info('  parcial cta:'+str(record_cta['id']) +'- subgrupo:' + subgrupo + ' $'+ str(record['balance_account']))
                    suma_subgrupo += record['balance_account']
        # mando a log el total por subgrupo
        _logger.info('-------TOTAL grupo:' + str(grupo_id) + ' subgrupo:' + subgrupo + ':$' + str(suma_subgrupo))

        #----------- busca en ctas contables COMUNES
        request_cta = "SELECT account_id as id, centro_costos FROM intercompany_cost_ctascomunes as cta where cta.grupo_id= " \
        + str(grupo_id)  + " and cta.distribucion_costo='" + subgrupo +"'"

        self.env.cr.execute(request_cta)
        for record_cta in self.env.cr.dictfetchall():
                request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
                          " WHERE account_id = " + str(record_cta['id']) + " and parent_state='posted'  " \
                          " and analytic_account_id="+ str(record_cta['centro_costos']) +" and date_part('month',date)=" + str(
                    self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"
                _logger.info('QUERY:' + request)
                self.env.cr.execute(request)
                for record in self.env.cr.dictfetchall():
                    if record['balance_account']:
                        _logger.info('  parcial cta comun :' + str(record_cta['id']) + '- subgrupo:' + subgrupo + ' $' + str(
                            record['balance_account']))
                        suma_subgrupo += record['balance_account']

        # mando a log el total por subgrupo
        _logger.info('-------TOTAL grupo:' + str(grupo_id) + ' subgrupo:' + subgrupo + ':$' + str(suma_subgrupo))

        return suma_subgrupo

    #def busca

    def post(self):
        #PARAMETROS
        CODCTA_IC_USA = self.env['ir.config_parameter'].get_param('codcta_ic_usa', '')
        CODCTA_IC_MEX = self.env['ir.config_parameter'].get_param('codcta_ic_mex', '')
        pdiario = (self.env['ir.config_parameter'].get_param('diario'))
        _logger.info('----Diario de asiento final:' + CODCTA_IC_MEX)
      #  _logger.info('----Diario de asiento final:' + pdiario)
        DIARIO = int(pdiario)

        # busco cuentas, luego genero asientos
        cta_recruiting_B1_mex,cta_recruiting_MKT_mex, cta_recruiting_S4_mex,  cta_recruiting_NT_mex,  cta_recruiting_talent_mex=None,None,None,None,None
        cta_recruiting_B1_usa, cta_recruiting_MKT_usa, cta_recruiting_S4_usa, cta_recruiting_NT_usa, cta_recruiting_talent_usa = None,None,None,None,None
        cta_mkt_B1_mex, cta_mkt_MKT_mex , cta_mkt_S4_mex, cta_mkt_NT_mex , cta_mkt_talent_mex= None,None,None,None,None
        cta_mkt_B1_usa, cta_mkt_MKT_usa, cta_mkt_S4_usa, cta_mkt_NT_usa, cta_mkt_talent_usa = None, None, None, None, None
        cta_op_B1_mex, cta_op_MKT_mex, cta_op_S4_mex, cta_op_NT_mex, cta_op_talent_mex = None, None, None, None, None
        cta_op_B1_usa, cta_op_MKT_usa, cta_op_S4_usa, cta_op_NT_usa, cta_op_talent_usa = None, None, None, None, None
        cta_sales_B1_mex, cta_sales_MKT_mex, cta_sales_S4_mex, cta_sales_NT_mex, cta_sales_talent_mex = None, None, None, None, None
        cta_sales_B1_usa, cta_sales_MKT_usa, cta_sales_S4_usa, cta_sales_NT_usa, cta_sales_talent_usa = None, None, None, None, None
        cta_presales_B1_mex, cta_presales_MKT_mex, cta_presales_S4_mex, cta_presales_NT_mex, cta_presales_talent_mex = None, None, None, None, None
        cta_presales_B1_usa, cta_presales_MKT_usa, cta_presales_S4_usa, cta_presales_NT_usa, cta_presales_talent_usa = None, None, None, None, None
        cta_ci_B1_mex, cta_ci_MKT_mex, cta_ci_S4_mex, cta_ci_NT_mex, cta_ci_talent_mex = None, None, None, None, None
        cta_ci_B1_usa, cta_ci_MKT_usa, cta_ci_S4_usa, cta_ci_NT_usa, cta_ci_talent_usa = None, None, None, None, None
        cta_ciun_B1_mex, cta_ciun_MKT_mex, cta_ciun_S4_mex, cta_ciun_NT_mex, cta_ciun_talent_mex = None, None, None, None, None
        cta_ciun_B1_usa, cta_ciun_MKT_usa, cta_ciun_S4_usa, cta_ciun_NT_usa, cta_ciun_talent_usa = None, None, None, None, None
        cta_leads_B1_mex, cta_leads_MKT_mex, cta_leads_S4_mex, cta_leads_NT_mex, cta_leads_talent_mex = None, None, None, None, None
        cta_leads_B1_usa, cta_leads_MKT_usa, cta_leads_S4_usa, cta_leads_NT_usa, cta_leads_talent_usa = None, None, None, None, None
        

        cuentas = self.env['type.results'].search([('resultado', '=', 'RECRUITING')])
        for ctas in cuentas:
            cta_recruiting_B1_mex = ctas.ctacontable_B1_mex
            cta_recruiting_MKT_mex = ctas.ctacontable_MKT_mex
            cta_recruiting_S4_mex = ctas.ctacontable_S4_mex
            cta_recruiting_NT_mex = ctas.ctacontable_NT_mex
            cta_recruiting_talent_mex = ctas.ctacontable_talent_mex
            cta_recruiting_B1_usa = ctas.ctacontable_B1_usa
            cta_recruiting_MKT_usa = ctas.ctacontable_MKT_usa
            cta_recruiting_S4_usa = ctas.ctacontable_S4_usa
            cta_recruiting_NT_usa = ctas.ctacontable_NT_usa
            cta_recruiting_talent_usa = ctas.ctacontable_talent_usa
        if  not(cta_recruiting_B1_mex) and (self.recruiting_b1_mex>0):
            raise UserError(('Falta definir las cuentas contables de recupero para RECRUITING B1 MEX'))
        if  not(cta_recruiting_MKT_mex) and (self.recruiting_mkt_mex>0):
            raise UserError(('Falta definir las cuentas contables de recupero para RECRUITING MKT MEX'))
        if  not(cta_recruiting_S4_mex) and (self.recruiting_s4_mex>0):
            raise UserError(('Falta definir las cuentas contables de recupero para RECRUITING S4 MEX'))
        if not (cta_recruiting_NT_mex) and (self.recruiting_nt_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para RECRUITING NT MEX'))
        if not (cta_recruiting_talent_mex) and (self.recruiting_talent_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para RECRUITING talent latam MEX'))
        if not (cta_recruiting_B1_usa) and (self.recruiting_b1_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para RECRUITING B1 USA'))
        if not (cta_recruiting_MKT_usa) and (self.recruiting_mkt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para RECRUITING MKT USA'))
        if not (cta_recruiting_S4_usa) and (self.recruiting_s4_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para RECRUITING S4 USA'))
        if not (cta_recruiting_NT_usa) and (self.recruiting_nt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para RECRUITING NT USA'))
        if not (cta_recruiting_talent_usa) and (self.recruiting_talent_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para RECRUITING talent USA'))

        #--------------------------------------------------#
        cuentas = self.env['type.results'].search([('resultado', '=', 'MKT')])
        for ctas in cuentas:
            cta_mkt_B1_mex = ctas.ctacontable_B1_mex
            cta_mkt_MKT_mex = ctas.ctacontable_MKT_mex
            cta_mkt_S4_mex = ctas.ctacontable_S4_mex
            cta_mkt_NT_mex = ctas.ctacontable_NT_mex
            cta_mkt_talent_mex = ctas.ctacontable_talent_mex
            cta_mkt_B1_usa = ctas.ctacontable_B1_usa
            cta_mkt_MKT_usa = ctas.ctacontable_MKT_usa
            cta_mkt_S4_usa = ctas.ctacontable_S4_usa
            cta_mkt_NT_usa = ctas.ctacontable_NT_usa
            cta_mkt_talent_usa = ctas.ctacontable_talent_usa
        if not (cta_mkt_B1_mex) and (self.mkt_b1_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para MKT B1 MEX'))
        if not (cta_mkt_MKT_mex) and (self.mkt_mkt_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para MKT MKT MEX'))
        if not (cta_mkt_S4_mex) and (self.mkt_s4_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para MKT S4 MEX'))
        if not (cta_mkt_NT_mex) and (self.mkt_nt_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para MKT NT MEX'))
        if not (cta_mkt_talent_mex) and (self.mkt_talent_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para MKT talent latam MEX'))
        if not (cta_mkt_B1_usa) and (self.mkt_b1_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para MKT B1 USA'))
        if not (cta_mkt_MKT_usa) and (self.mkt_mkt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para MKT MKT USA'))
        if not (cta_mkt_S4_usa) and (self.mkt_s4_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para MKT S4 USA'))
        if not (cta_mkt_NT_usa) and (self.mkt_nt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para MKT NT USA'))
        if not (cta_mkt_talent_usa) and (self.mkt_talent_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para MKT talent USA'))

        # --------------------------------------------------#
        cuentas = self.env['type.results'].search([('resultado', '=', 'OP')])
        for ctas in cuentas:
            cta_op_B1_mex = ctas.ctacontable_B1_mex
            cta_op_MKT_mex = ctas.ctacontable_MKT_mex
            cta_op_S4_mex = ctas.ctacontable_S4_mex
            cta_op_NT_mex = ctas.ctacontable_NT_mex
            cta_op_talent_mex = ctas.ctacontable_talent_mex
            cta_op_B1_usa = ctas.ctacontable_B1_usa
            cta_op_MKT_usa = ctas.ctacontable_MKT_usa
            cta_op_S4_usa = ctas.ctacontable_S4_usa
            cta_op_NT_usa = ctas.ctacontable_NT_usa
            cta_op_talent_usa = ctas.ctacontable_talent_usa
        if  not(cta_op_B1_mex) and (self.op_b1_mex>0):
            raise UserError(('Falta definir las cuentas contables de recupero para OP B1 MEX'))
        if  not(cta_op_MKT_mex) and (self.op_mkt_mex>0):
            raise UserError(('Falta definir las cuentas contables de recupero para OP MKT MEX'))
        if  not(cta_op_S4_mex) and (self.op_s4_mex>0):
            raise UserError(('Falta definir las cuentas contables de recupero para OP S4 MEX'))
        if not (cta_op_NT_mex) and (self.op_nt_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para OP NT MEX'))
        if not (cta_op_talent_mex) and (self.op_talent_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para OP talent latam MEX'))
        if not (cta_op_B1_usa) and (self.op_b1_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para OP B1 USA'))
        if not (cta_op_MKT_usa) and (self.op_mkt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para OP MKT USA'))
        if not (cta_op_S4_usa) and (self.op_s4_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para OP S4 USA'))
        if not (cta_op_NT_usa) and (self.op_nt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para OP NT USA'))
        if not (cta_op_talent_usa) and (self.op_talent_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para OP talent USA'))
        # --------------------------------------------------#
        cuentas = self.env['type.results'].search([('resultado', '=', 'CI')])
        for ctas in cuentas:
            cta_ci_B1_mex = ctas.ctacontable_B1_mex
            cta_ci_MKT_mex = ctas.ctacontable_MKT_mex
            cta_ci_S4_mex = ctas.ctacontable_S4_mex
            cta_ci_NT_mex = ctas.ctacontable_NT_mex
            cta_ci_talent_mex = ctas.ctacontable_talent_mex
            cta_ci_B1_usa = ctas.ctacontable_B1_usa
            cta_ci_MKT_usa = ctas.ctacontable_MKT_usa
            cta_ci_S4_usa = ctas.ctacontable_S4_usa
            cta_ci_NT_usa = ctas.ctacontable_NT_usa
            cta_ci_talent_usa = ctas.ctacontable_talent_usa
        if  not(cta_ci_B1_mex) and (self.ci_b1_mex>0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI B1 MEX'))
        if  not(cta_ci_MKT_mex) and (self.ci_mkt_mex>0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI MKT MEX'))
        if  not(cta_ci_S4_mex) and (self.ci_s4_mex>0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI S4 MEX'))
        if not (cta_ci_NT_mex) and (self.ci_nt_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI NT MEX'))
        if not (cta_ci_talent_mex) and (self.ci_talent_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI talent latam MEX'))
        if not (cta_ci_B1_usa) and (self.ci_b1_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI B1 USA'))
        if not (cta_ci_MKT_usa) and (self.ci_mkt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI MKT USA'))
        if not (cta_ci_S4_usa) and (self.ci_s4_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI S4 USA'))
        if not (cta_ci_NT_usa) and (self.ci_nt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI NT USA'))
        if not (cta_ci_talent_usa) and (self.ci_talent_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI talent USA'))

        # --------------------------------------------------#
        cuentas = self.env['type.results'].search([('resultado', '=', 'SALES')])
        for ctas in cuentas:
            cta_sales_B1_mex = ctas.ctacontable_B1_mex
            cta_sales_MKT_mex = ctas.ctacontable_MKT_mex
            cta_sales_S4_mex = ctas.ctacontable_S4_mex
            cta_sales_NT_mex = ctas.ctacontable_NT_mex
            cta_sales_talent_mex = ctas.ctacontable_talent_mex
            cta_sales_B1_usa = ctas.ctacontable_B1_usa
            cta_sales_MKT_usa = ctas.ctacontable_MKT_usa
            cta_sales_S4_usa = ctas.ctacontable_S4_usa
            cta_sales_NT_usa = ctas.ctacontable_NT_usa
            cta_sales_talent_usa = ctas.ctacontable_talent_usa
        if  not(cta_sales_B1_mex) and (self.sales_b1_mex>0):
            raise UserError(('Falta definir las cuentas contables de recupero para SALES B1 MEX'))
        if  not(cta_sales_MKT_mex) and (self.sales_mkt_mex>0):
            raise UserError(('Falta definir las cuentas contables de recupero para SALES MKT MEX'))
        if  not(cta_sales_S4_mex) and (self.sales_s4_mex>0):
            raise UserError(('Falta definir las cuentas contables de recupero para SALES S4 MEX'))
        if not (cta_sales_NT_mex) and (self.sales_nt_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para SALES NT MEX'))
        if not (cta_sales_talent_mex) and (self.sales_talent_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para SALES talent latam MEX'))
        if not (cta_sales_B1_usa) and (self.sales_b1_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para SALES B1 USA'))
        if not (cta_sales_MKT_usa) and (self.sales_mkt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para SALES MKT USA'))
        if not (cta_sales_S4_usa) and (self.sales_s4_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para SALES S4 USA'))
        if not (cta_sales_NT_usa) and (self.sales_nt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para SALES NT USA'))
        if not (cta_sales_talent_usa) and (self.sales_talent_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para SALES talent USA'))

        # --------------------------------------------------#
        cuentas = self.env['type.results'].search([('resultado', '=', 'PRESALES')])
        for ctas in cuentas:
            cta_presales_B1_mex = ctas.ctacontable_B1_mex
            cta_presales_MKT_mex = ctas.ctacontable_MKT_mex
            cta_presales_S4_mex = ctas.ctacontable_S4_mex
            cta_presales_NT_mex = ctas.ctacontable_NT_mex
            cta_presales_talent_mex = ctas.ctacontable_talent_mex
            cta_presales_B1_usa = ctas.ctacontable_B1_usa
            cta_presales_MKT_usa = ctas.ctacontable_MKT_usa
            cta_presales_S4_usa = ctas.ctacontable_S4_usa
            cta_presales_NT_usa = ctas.ctacontable_NT_usa
            cta_presales_talent_usa = ctas.ctacontable_talent_usa
        if  not(cta_presales_B1_mex) and (self.presales_b1_mex>0):
            raise UserError(('Falta definir las cuentas contables de recupero para PRESALES B1 MEX'))
        if  not(cta_presales_MKT_mex) and (self.presales_mkt_mex>0):
            raise UserError(('Falta definir las cuentas contables de recupero para PRESALES MKT MEX'))
        if  not(cta_presales_S4_mex) and (self.presales_s4_mex>0):
            raise UserError(('Falta definir las cuentas contables de recupero para PRESALES S4 MEX'))
        if not (cta_presales_NT_mex) and (self.presales_nt_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para PRESALES NT MEX'))
        if not (cta_presales_talent_mex) and (self.presales_talent_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para PRESALES talent latam MEX'))
        if not (cta_presales_B1_usa) and (self.presales_b1_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para PRESALES B1 USA'))
        if not (cta_presales_MKT_usa) and (self.presales_mkt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para PRESALES MKT USA'))
        if not (cta_presales_S4_usa) and (self.presales_s4_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para PRESALES S4 USA'))
        if not (cta_presales_NT_usa) and (self.presales_nt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para PRESALES NT USA'))
        if not (cta_presales_talent_usa) and (self.presales_talent_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para PRESALES talent USA'))

        # --------------------------------------------------#
        cuentas = self.env['type.results'].search([('resultado', '=', 'CI-UN')])
        for ctas in cuentas:
            cta_ciun_B1_mex = ctas.ctacontable_B1_mex
            cta_ciun_MKT_mex = ctas.ctacontable_MKT_mex
            cta_ciun_S4_mex = ctas.ctacontable_S4_mex
            cta_ciun_NT_mex = ctas.ctacontable_NT_mex
            cta_ciun_talent_mex = ctas.ctacontable_talent_mex
            cta_ciun_B1_usa = ctas.ctacontable_B1_usa
            cta_ciun_MKT_usa = ctas.ctacontable_MKT_usa
            cta_ciun_S4_usa = ctas.ctacontable_S4_usa
            cta_ciun_NT_usa = ctas.ctacontable_NT_usa
            cta_ciun_talent_usa = ctas.ctacontable_talent_usa
        if not (cta_ciun_B1_mex) and (self.ciun_b1_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI-UN B1 MEX'))
        if not (cta_ciun_MKT_mex) and (self.ciun_mkt_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI-UN MKT MEX'))
        if not (cta_ciun_S4_mex) and (self.ciun_s4_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI-UN S4 MEX'))
        if not (cta_ciun_NT_mex) and (self.ciun_nt_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI-UN NT MEX'))
        if not (cta_ciun_talent_mex) and (self.ciun_talent_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI-UN talent latam MEX'))
        if not (cta_ciun_B1_usa) and (self.ciun_b1_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI-UN B1 USA'))
        if not (cta_ciun_MKT_usa) and (self.ciun_mkt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI-UN MKT USA'))
        if not (cta_ciun_S4_usa) and (self.ciun_s4_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI-UN S4 USA'))
        if not (cta_ciun_NT_usa) and (self.ciun_nt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI-UN NT USA'))
        if not (cta_ciun_talent_usa) and (self.ciun_talent_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para CI-UN talent USA'))

        #--------------------------------------------------------
        # se deja de hacer feb 2023
        # cuentas = self.env['type.results'].search([('resultado', '=', 'COMISIONES UN')])
        # for ctas in cuentas:
        #     cta_comisionesun_mex = ctas.ctacontable_mex
        #     cta_comisionesun_usa = ctas.ctacontable_usa
        # if not (cta_comisionesun_mex) or not (cta_comisionesun_usa):
        #     raise UserError(('Falta definir las cuentas contables de recupero para COMISIONES UN'))
        #--------------------------------------------------------
        # se deja de hacer feb 2023
        # cuentas = self.env['type.results'].search([('resultado', '=', 'COMISIONES MKT')])
        # for ctas in cuentas:
        #     cta_comisionesmkt_mex = ctas.ctacontable_mex
        #     cta_comisionesmkt_usa = ctas.ctacontable_usa
        # if not (cta_comisionesmkt_mex) or not (cta_comisionesmkt_usa):
        #     raise UserError(('Falta definir las cuentas contables de recupero para COMISIONES MKT'))
        #--------------------------------------------------------
        # cuentas = self.env['type.results'].search([('resultado', '=', 'COMISIONES TALENT')])
        # for ctas in cuentas:
        #     cta_comisionestalent_mex = ctas.ctacontable_mex
        #     cta_comisionestalent_usa = ctas.ctacontable_usa
        # if not (cta_comisionestalent_mex) or not (cta_comisionestalent_usa):
        #     raise UserError(('Falta definir las cuentas contables de recupero para COMISIONES TALENT'))
        #--------------------------------------------------------
        cuentas = self.env['type.results'].search([('resultado', '=', 'LEADS MKT')])
        for ctas in cuentas:
            cta_leads_B1_mex = ctas.ctacontable_B1_mex
            cta_leads_MKT_mex = ctas.ctacontable_MKT_mex
            cta_leads_S4_mex = ctas.ctacontable_S4_mex
            cta_leads_NT_mex = ctas.ctacontable_NT_mex
            cta_leads_talent_mex = ctas.ctacontable_talent_mex
            cta_leads_B1_usa = ctas.ctacontable_B1_usa
            cta_leads_MKT_usa = ctas.ctacontable_MKT_usa
            cta_leads_S4_usa = ctas.ctacontable_S4_usa
            cta_leads_NT_usa = ctas.ctacontable_NT_usa
            cta_leads_talent_usa = ctas.ctacontable_talent_usa
        if not (cta_leads_B1_mex) and (self.leadsmkt_b1_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para LEADS B1 MEX'))
        if not (cta_leads_MKT_mex) and (self.leadsmkt_mkt_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para LEADS MKT MEX'))
        if not (cta_leads_S4_mex) and (self.leadsmkt_s4_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para LEADS S4 MEX'))
        if not (cta_leads_NT_mex) and (self.leadsmkt_nt_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para LEADS NT MEX'))
        if not (cta_leads_talent_mex) and (self.leadsmkt_talent_mex > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para LEADS talent latam MEX'))
        if not (cta_leads_B1_usa) and (self.leadsmkt_b1_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para LEADS B1 USA'))
        if not (cta_leads_MKT_usa) and (self.leadsmkt_mkt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para LEADS MKT USA'))
        if not (cta_leads_S4_usa) and (self.leadsmkt_s4_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para LEADS S4 USA'))
        if not (cta_leads_NT_usa) and (self.leadsmkt_nt_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para LEADS NT USA'))
        if not (cta_leads_talent_usa) and (self.leadsmkt_talent_usa > 0):
            raise UserError(('Falta definir las cuentas contables de recupero para LEADS talent USA'))

        #**************** genero asientos  ***********************
        cta_acobrar_ic_mex = self.env['account.account'].search([('code', '=', CODCTA_IC_MEX)])
        cta_acobrar_ic_usa = self.env['account.account'].search([('code', '=', CODCTA_IC_USA)])
        _logger.info('---CUENTA IC MEX:' + str(cta_acobrar_ic_mex))
        _logger.info('---CUENTA IC USA:' + str(cta_acobrar_ic_usa))
        # ------ ASIENTO RECRUITING-----------
        # recruitng mex
        totrecruiting_mex=0
        lines = [(5, 0, 0)]
        if (self.recruiting_b1_mex>0):
            val = {'account_id': cta_recruiting_B1_mex.id,
                'currency_id': 19,
                'debit': self.recruiting_b1_mex,
                'amount_currency': self.recruiting_b1_mex}
            lines.append((0, 0, val))
            totrecruiting_mex= totrecruiting_mex+self.recruiting_b1_mex
        if (self.recruiting_mkt_mex>0):
            val = {'account_id': cta_recruiting_MKT_mex.id,
               'currency_id': 19,
               'debit': self.recruiting_mkt_mex,
               'amount_currency': self.recruiting_mkt_mex}
            lines.append((0, 0, val))
            totrecruiting_mex = totrecruiting_mex + self.recruiting_mkt_mex
        if (self.recruiting_s4_mex>0):
            val = {'account_id': cta_recruiting_S4_mex.id,
               'currency_id': 19,
               'debit': self.recruiting_s4_mex,
               'amount_currency': self.recruiting_s4_mex}
            lines.append((0, 0, val))
            totrecruiting_mex = totrecruiting_mex + self.recruiting_s4_mex
        if (self.recruiting_nt_mex > 0):
            val = {'account_id': cta_recruiting_NT_mex.id,
                   'currency_id': 19,
                   'debit': self.recruiting_nt_mex,
                   'amount_currency': self.recruiting_nt_mex}
            lines.append(0, 0, val)
            totrecruiting_mex = totrecruiting_mex + self.recruiting_nt_mex
        if (self.recruiting_talent_mex > 0):
            val = {'account_id': cta_recruiting_talent_mex.id,
                   'currency_id': 19,
                   'debit': self.recruiting_talent_mex,
                   'amount_currency': self.recruiting_talent_mex}
            lines.append((0, 0, val))
            totrecruiting_mex = totrecruiting_mex + self.recruiting_talent_mex
        if (totrecruiting_mex>0):
            val = {'account_id': cta_acobrar_ic_mex.id,
               'currency_id': 19,
               'credit': totrecruiting_mex,
               'amount_currency': totrecruiting_mex * -1,
               }
            lines.append((0, 0, val))
            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
            move.action_post()
        #recruitng usa
        totrecruiting_usa = 0
        lines = [(5, 0, 0)]
        if (self.recruiting_b1_usa > 0):
            val = {'account_id': cta_recruiting_B1_usa.id,
                   'currency_id': 19,
                   'debit': self.recruiting_b1_usa,
                   'amount_currency': self.recruiting_b1_usa}
            lines.append((0, 0, val))
            totrecruiting_usa = totrecruiting_usa + self.recruiting_b1_usa
        if (self.recruiting_mkt_usa > 0):
            val = {'account_id': cta_recruiting_MKT_usa.id,
                   'currency_id': 19,
                   'debit': self.recruiting_mkt_usa,
                   'amount_currency': self.recruiting_mkt_usa}
            lines.append((0, 0, val))
            totrecruiting_usa = totrecruiting_usa + self.recruiting_mkt_usa
        if (self.recruiting_s4_usa > 0):
            val = {'account_id': cta_recruiting_S4_usa.id,
                   'currency_id': 19,
                   'debit': self.recruiting_s4_usa,
                   'amount_currency': self.recruiting_s4_usa}
            lines.append((0, 0, val))
            totrecruiting_usa = totrecruiting_usa + self.recruiting_s4_usa
        if (self.recruiting_nt_usa > 0):
            val = {'account_id': cta_recruiting_NT_usa.id,
                   'currency_id': 19,
                   'debit': self.recruiting_nt_usa,
                   'amount_currency': self.recruiting_nt_usa}
            lines.append((0, 0, val))
            totrecruiting_usa = totrecruiting_usa + self.recruiting_nt_usa
        if (self.recruiting_talent_usa > 0):
            val = {'account_id': cta_recruiting_talent_usa.id,
                   'currency_id': 19,
                   'debit': self.recruiting_talent_usa,
                   'amount_currency': self.recruiting_talent_usa}
            lines.append((0, 0, val))
            totrecruiting_usa = totrecruiting_usa + self.recruiting_talent_usa
        if (totrecruiting_usa > 0):
            val = {'account_id': cta_acobrar_ic_usa.id,
                   'currency_id': 19,
                   'credit': totrecruiting_usa,
                   'amount_currency': totrecruiting_usa * -1,
                   }
            lines.append((0, 0, val))
            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
            move.action_post()
        # ------ ASIENTO MKT-----------
        # recruitng mex
        totmkt_mex = 0
        lines = [(5, 0, 0)]
        if (self.mkt_b1_mex > 0):
            val = {'account_id': cta_mkt_B1_mex.id,
                   'currency_id': 19,
                   'debit': self.mkt_b1_mex,
                   'amount_currency': self.mkt_b1_mex}
            lines.append((0, 0, val))
            totmkt_mex = totmkt_mex + self.mkt_b1_mex
        if (self.mkt_mkt_mex > 0):
            val = {'account_id': cta_mkt_MKT_mex.id,
                   'currency_id': 19,
                   'debit': self.mkt_mkt_mex,
                   'amount_currency': self.mkt_mkt_mex}
            lines.append((0, 0, val))
            totmkt_mex = totmkt_mex + self.mkt_mkt_mex
        if (self.mkt_s4_mex > 0):
            val = {'account_id': cta_mkt_S4_mex.id,
                   'currency_id': 19,
                   'debit': self.mkt_s4_mex,
                   'amount_currency': self.mkt_s4_mex}
            lines.append((0, 0, val))
            totmkt_mex = totmkt_mex + self.mkt_s4_mex
        if (self.mkt_nt_mex > 0):
            val = {'account_id': cta_mkt_NT_mex.id,
                   'currency_id': 19,
                   'debit': self.mkt_nt_mex,
                   'amount_currency': self.mkt_nt_mex}
            lines.append((0, 0, val))
            totmkt_mex = totmkt_mex + self.mkt_nt_mex
        if (self.mkt_talent_mex > 0):
            val = {'account_id': cta_mkt_talent_mex.id,
                   'currency_id': 19,
                   'debit': self.mkt_talent_mex,
                   'amount_currency': self.mkt_talent_mex}
            lines.append((0, 0, val))
            totmkt_mex = totmkt_mex + self.mkt_talent_mex
        if (totmkt_mex > 0):
            val = {'account_id': cta_acobrar_ic_mex.id,
                   'currency_id': 19,
                   'credit': totmkt_mex,
                   'amount_currency': totmkt_mex * -1,
                   }
            lines.append((0, 0, val))
            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
            move.action_post()
        # recruitng usa
        totmkt_usa = 0
        lines = [(5, 0, 0)]
        if (self.mkt_b1_usa > 0):
            val = {'account_id': cta_mkt_B1_usa.id,
                   'currency_id': 19,
                   'debit': self.mkt_b1_usa,
                   'amount_currency': self.mkt_b1_usa}
            lines.append((0, 0, val))
            totmkt_usa = totmkt_usa + self.mkt_b1_usa
        if (self.mkt_mkt_usa > 0):
            val = {'account_id': cta_mkt_MKT_usa.id,
                   'currency_id': 19,
                   'debit': self.mkt_mkt_usa,
                   'amount_currency': self.mkt_mkt_usa}
            lines.append((0, 0, val))
            totmkt_usa = totmkt_usa + self.mkt_mkt_usa
        if (self.mkt_s4_usa > 0):
            val = {'account_id': cta_mkt_S4_usa.id,
                   'currency_id': 19,
                   'debit': self.mkt_s4_usa,
                   'amount_currency': self.mkt_s4_usa}
            lines.append((0, 0, val))
            totmkt_usa = totmkt_usa + self.mkt_s4_usa
        if (self.mkt_nt_usa > 0):
            val = {'account_id': cta_mkt_NT_usa.id,
                   'currency_id': 19,
                   'debit': self.mkt_nt_usa,
                   'amount_currency': self.mkt_nt_usa}
            lines.append((0, 0, val))
            totmkt_usa = totmkt_usa + self.mkt_nt_usa
        if (self.mkt_talent_usa > 0):
            val = {'account_id': cta_mkt_talent_usa.id,
                   'currency_id': 19,
                   'debit': self.mkt_talent_usa,
                   'amount_currency': self.mkt_talent_usa}
            lines.append((0, 0, val))
            totmkt_usa = totmkt_usa + self.mkt_talent_usa
        if (totmkt_usa > 0):
            val = {'account_id': cta_acobrar_ic_usa.id,
                   'currency_id': 19,
                   'credit': totmkt_usa,
                   'amount_currency': totmkt_usa * -1,
                   }
            lines.append((0, 0, val))
            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
            move.action_post()
        
        # ------ ASIENTO SALES-----------
        # recruitng mex
        totsales_mex = 0
        lines = [(5, 0, 0)]
        if (self.sales_b1_mex > 0):
            val = {'account_id': cta_sales_B1_mex.id,
                   'currency_id': 19,
                   'debit': self.sales_b1_mex,
                   'amount_currency': self.sales_b1_mex}
            lines.append((0, 0, val))
            totsales_mex = totsales_mex + self.sales_b1_mex
        if (self.sales_mkt_mex > 0):
            val = {'account_id': cta_sales_MKT_mex.id,
                   'currency_id': 19,
                   'debit': self.sales_mkt_mex,
                   'amount_currency': self.sales_mkt_mex}
            lines.append((0, 0, val))
            totsales_mex = totsales_mex + self.sales_mkt_mex
        if (self.sales_s4_mex > 0):
            val = {'account_id': cta_sales_S4_mex.id,
                   'currency_id': 19,
                   'debit': self.sales_s4_mex,
                   'amount_currency': self.sales_s4_mex}
            lines.append((0, 0, val))
            totsales_mex = totsales_mex + self.sales_s4_mex
        if (self.sales_nt_mex > 0):
            val = {'account_id': cta_sales_NT_mex.id,
                   'currency_id': 19,
                   'debit': self.sales_nt_mex,
                   'amount_currency': self.sales_nt_mex}
            lines.append((0, 0, val))
            totsales_mex = totsales_mex + self.sales_nt_mex
        if (self.sales_talent_mex > 0):
            val = {'account_id': cta_sales_talent_mex.id,
                   'currency_id': 19,
                   'debit': self.sales_talent_mex,
                   'amount_currency': self.sales_talent_mex}
            lines.append((0, 0, val))
            totsales_mex = totsales_mex + self.sales_talent_mex
        if (totsales_mex > 0):
            val = {'account_id': cta_acobrar_ic_mex.id,
                   'currency_id': 19,
                   'credit': totsales_mex,
                   'amount_currency': totsales_mex * -1,
                   }
            lines.append((0, 0, val))
            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
            move.action_post()
        # recruitng usa
        totsales_usa = 0
        lines = [(5, 0, 0)]
        if (self.sales_b1_usa > 0):
            val = {'account_id': cta_sales_B1_usa.id,
                   'currency_id': 19,
                   'debit': self.sales_b1_usa,
                   'amount_currency': self.sales_b1_usa}
            lines.append((0, 0, val))
            totsales_usa = totsales_usa + self.sales_b1_usa
        if (self.sales_mkt_usa > 0):
            val = {'account_id': cta_sales_MKT_usa.id,
                   'currency_id': 19,
                   'debit': self.sales_mkt_usa,
                   'amount_currency': self.sales_mkt_usa}
            lines.append((0, 0, val))
            totsales_usa = totsales_usa + self.sales_mkt_usa
        if (self.sales_s4_usa > 0):
            val = {'account_id': cta_sales_S4_usa.id,
                   'currency_id': 19,
                   'debit': self.sales_s4_usa,
                   'amount_currency': self.sales_s4_usa}
            lines.append((0, 0, val))
            totsales_usa = totsales_usa + self.sales_s4_usa
        if (self.sales_nt_usa > 0):
            val = {'account_id': cta_sales_NT_usa.id,
                   'currency_id': 19,
                   'debit': self.sales_nt_usa,
                   'amount_currency': self.sales_nt_usa}
            lines.append((0, 0, val))
            totsales_usa = totsales_usa + self.sales_nt_usa
        if (self.sales_talent_usa > 0):
            val = {'account_id': cta_sales_talent_usa.id,
                   'currency_id': 19,
                   'debit': self.sales_talent_usa,
                   'amount_currency': self.sales_talent_usa}
            lines.append((0, 0, val))
            totsales_usa = totsales_usa + self.sales_talent_usa
        if (totsales_usa > 0):
            val = {'account_id': cta_acobrar_ic_usa.id,
                   'currency_id': 19,
                   'credit': totsales_usa,
                   'amount_currency': totsales_usa * -1,
                   }
            lines.append((0, 0, val))

            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
            move.action_post()
        # ------ ASIENTO PRESALES-----------
        # recruitng mex
        totpresales_mex = 0
        lines = [(5, 0, 0)]
        if (self.presales_b1_mex > 0):
            val = {'account_id': cta_presales_B1_mex.id,
                   'currency_id': 19,
                   'debit': self.presales_b1_mex,
                   'amount_currency': self.presales_b1_mex}
            lines.append((0, 0, val))
            totpresales_mex = totpresales_mex + self.presales_b1_mex
        if (self.presales_mkt_mex > 0):
            val = {'account_id': cta_presales_MKT_mex.id,
                   'currency_id': 19,
                   'debit': self.presales_mkt_mex,
                   'amount_currency': self.presales_mkt_mex}
            lines.append((0, 0, val))
            totpresales_mex = totpresales_mex + self.presales_mkt_mex
        if (self.presales_s4_mex > 0):
            val = {'account_id': cta_presales_S4_mex.id,
                   'currency_id': 19,
                   'debit': self.presales_s4_mex,
                   'amount_currency': self.presales_s4_mex}
            lines.append((0, 0, val))
            totpresales_mex = totpresales_mex + self.presales_s4_mex
        if (self.presales_nt_mex > 0):
            val = {'account_id': cta_presales_NT_mex.id,
                   'currency_id': 19,
                   'debit': self.presales_nt_mex,
                   'amount_currency': self.presales_nt_mex}
            lines.append((0, 0, val))
            totpresales_mex = totpresales_mex + self.presales_nt_mex
        if (self.presales_talent_mex > 0):
            val = {'account_id': cta_presales_talent_mex.id,
                   'currency_id': 19,
                   'debit': self.presales_talent_mex,
                   'amount_currency': self.presales_talent_mex}
            lines.append((0, 0, val))
            totpresales_mex = totpresales_mex + self.presales_talent_mex
        if (totpresales_mex > 0):
            val = {'account_id': cta_acobrar_ic_mex.id,
                   'currency_id': 19,
                   'credit': totpresales_mex,
                   'amount_currency': totpresales_mex * -1,
                   }
            lines.append((0, 0, val))
            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
            move.action_post()
        # recruitng usa
        totpresales_usa = 0
        lines = [(5, 0, 0)]
        if (self.presales_b1_usa > 0):
            val = {'account_id': cta_presales_B1_usa.id,
                   'currency_id': 19,
                   'debit': self.presales_b1_usa,
                   'amount_currency': self.presales_b1_usa}
            lines.append((0, 0, val))
            totpresales_usa = totpresales_usa + self.presales_b1_usa
        if (self.presales_mkt_usa > 0):
            val = {'account_id': cta_presales_MKT_usa.id,
                   'currency_id': 19,
                   'debit': self.presales_mkt_usa,
                   'amount_currency': self.presales_mkt_usa}
            lines.append((0, 0, val))
            totpresales_usa = totpresales_usa + self.presales_mkt_usa
        if (self.presales_s4_usa > 0):
            val = {'account_id': cta_presales_S4_usa.id,
                   'currency_id': 19,
                   'debit': self.presales_s4_usa,
                   'amount_currency': self.presales_s4_usa}
            lines.append((0, 0, val))
            totpresales_usa = totpresales_usa + self.presales_s4_usa
        if (self.presales_nt_usa > 0):
            val = {'account_id': cta_presales_NT_usa.id,
                   'currency_id': 19,
                   'debit': self.presales_nt_usa,
                   'amount_currency': self.presales_nt_usa}
            lines.append((0, 0, val))
            totpresales_usa = totpresales_usa + self.presales_nt_usa
        if (self.presales_talent_usa > 0):
            val = {'account_id': cta_presales_talent_usa.id,
                   'currency_id': 19,
                   'debit': self.presales_talent_usa,
                   'amount_currency': self.presales_talent_usa}
            lines.append((0, 0, val))
            totpresales_usa = totpresales_usa + self.presales_talent_usa
        if (totpresales_usa > 0):
            val = {'account_id': cta_acobrar_ic_usa.id,
                   'currency_id': 19,
                   'credit': totpresales_usa,
                   'amount_currency': totpresales_usa * -1,
                   }
            lines.append((0, 0, val))

            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
            move.action_post()
        # ------ ASIENTO CI-----------
        # recruitng mex
        totci_mex = 0
        lines = [(5, 0, 0)]
        if (self.ci_b1_mex > 0):
            val = {'account_id': cta_ci_B1_mex.id,
                   'currency_id': 19,
                   'debit': self.ci_b1_mex,
                   'amount_currency': self.ci_b1_mex}
            lines.append((0, 0, val))
            totci_mex = totci_mex + self.ci_b1_mex
        if (self.ci_mkt_mex > 0):
            val = {'account_id': cta_ci_MKT_mex.id,
                   'currency_id': 19,
                   'debit': self.ci_mkt_mex,
                   'amount_currency': self.ci_mkt_mex}
            lines.append((0, 0, val))
            totci_mex = totci_mex + self.ci_mkt_mex
        if (self.ci_s4_mex > 0):
            val = {'account_id': cta_ci_S4_mex.id,
                   'currency_id': 19,
                   'debit': self.ci_s4_mex,
                   'amount_currency': self.ci_s4_mex}
            lines.append((0, 0, val))
            totci_mex = totci_mex + self.ci_s4_mex
        if (self.ci_nt_mex > 0):
            val = {'account_id': cta_ci_NT_mex.id,
                   'currency_id': 19,
                   'debit': self.ci_nt_mex,
                   'amount_currency': self.ci_nt_mex}
            lines.append((0, 0, val))
            totci_mex = totci_mex + self.ci_nt_mex
        if (self.ci_talent_mex > 0):
            val = {'account_id': cta_ci_talent_mex.id,
                   'currency_id': 19,
                   'debit': self.ci_talent_mex,
                   'amount_currency': self.ci_talent_mex}
            lines.append((0, 0, val))
            totci_mex = totci_mex + self.ci_talent_mex
        if (totci_mex > 0):
            val = {'account_id': cta_acobrar_ic_mex.id,
                   'currency_id': 19,
                   'credit': totci_mex,
                   'amount_currency': totci_mex * -1,
                   }
            lines.append(0, 0, val)
            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
            move.action_post()
        # recruitng usa
        totci_usa = 0
        lines = [(5, 0, 0)]
        if (self.ci_b1_usa > 0):
            val = {'account_id': cta_ci_B1_usa.id,
                   'currency_id': 19,
                   'debit': self.ci_b1_usa,
                   'amount_currency': self.ci_b1_usa}
            lines.append((0, 0, val))
            totci_usa = totci_usa + self.ci_b1_usa
        if (self.ci_mkt_usa > 0):
            val = {'account_id': cta_ci_MKT_usa.id,
                   'currency_id': 19,
                   'debit': self.ci_mkt_usa,
                   'amount_currency': self.ci_mkt_usa}
            lines.append((0, 0, val))
            totci_usa = totci_usa + self.ci_mkt_usa
        if (self.ci_s4_usa > 0):
            val = {'account_id': cta_ci_S4_usa.id,
                   'currency_id': 19,
                   'debit': self.ci_s4_usa,
                   'amount_currency': self.ci_s4_usa}
            lines.append((0, 0, val))
            totci_usa = totci_usa + self.ci_s4_usa
        if (self.ci_nt_usa > 0):
            val = {'account_id': cta_ci_NT_usa.id,
                   'currency_id': 19,
                   'debit': self.ci_nt_usa,
                   'amount_currency': self.ci_nt_usa}
            lines.append((0, 0, val))
            totci_usa = totci_usa + self.ci_nt_usa
        if (self.ci_talent_usa > 0):
            val = {'account_id': cta_ci_talent_usa.id,
                   'currency_id': 19,
                   'debit': self.ci_talent_usa,
                   'amount_currency': self.ci_talent_usa}
            lines.append((0, 0, val))
            totci_usa = totci_usa + self.ci_talent_usa
        if (totci_usa > 0):
            val = {'account_id': cta_acobrar_ic_usa.id,
                   'currency_id': 19,
                   'credit': totci_usa,
                   'amount_currency': totci_usa * -1,
                   }
            lines.append(0, 0, val)

            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
            move.action_post()
        # ------ ASIENTO CI-UN -----------
        # recruitng mex
        totciun_mex = 0
        lines = [(5, 0, 0)]
        if (self.ciun_b1_mex > 0):
            val = {'account_id': cta_ciun_B1_mex.id,
                   'currency_id': 19,
                   'debit': self.ciun_b1_mex,
                   'amount_currency': self.ciun_b1_mex}
            lines.append((0, 0, val))
            totciun_mex = totciun_mex + self.ciun_b1_mex
        if (self.ciun_mkt_mex > 0):
            val = {'account_id': cta_ciun_MKT_mex.id,
                   'currency_id': 19,
                   'debit': self.ciun_mkt_mex,
                   'amount_currency': self.ciun_mkt_mex}
            lines.append((0, 0, val))
            totciun_mex = totciun_mex + self.ciun_mkt_mex
        if (self.ciun_s4_mex > 0):
            val = {'account_id': cta_ciun_S4_mex.id,
                   'currency_id': 19,
                   'debit': self.ciun_s4_mex,
                   'amount_currency': self.ciun_s4_mex}
            lines.append((0, 0, val))
            totciun_mex = totciun_mex + self.ciun_s4_mex
        if (self.ciun_nt_mex > 0):
            val = {'account_id': cta_ciun_NT_mex.id,
                   'currency_id': 19,
                   'debit': self.ciun_nt_mex,
                   'amount_currency': self.ciun_nt_mex}
            lines.append((0, 0, val))
            totciun_mex = totciun_mex + self.ciun_nt_mex
        if (self.ciun_talent_mex > 0):
            val = {'account_id': cta_ciun_talent_mex.id,
                   'currency_id': 19,
                   'debit': self.ciun_talent_mex,
                   'amount_currency': self.ciun_talent_mex}
            lines.append((0, 0, val))
            totciun_mex = totciun_mex + self.ciun_talent_mex
        if (totciun_mex > 0):
            val = {'account_id': cta_acobrar_ic_mex.id,
                   'currency_id': 19,
                   'credit': totciun_mex,
                   'amount_currency': totciun_mex * -1,
                   }
            lines.append((0, 0, val))
            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
            move.action_post()
        # recruitng usa
        totciun_usa = 0
        lines = [(5, 0, 0)]
        if (self.ciun_b1_usa > 0):
            val = {'account_id': cta_ciun_B1_usa.id,
                   'currency_id': 19,
                   'debit': self.ciun_b1_usa,
                   'amount_currency': self.ciun_b1_usa}
            lines.append((0, 0, val))
            totciun_usa = totciun_usa + self.ciun_b1_usa
        if (self.ciun_mkt_usa > 0):
            val = {'account_id': cta_ciun_MKT_usa.id,
                   'currency_id': 19,
                   'debit': self.ciun_mkt_usa,
                   'amount_currency': self.ciun_mkt_usa}
            lines.append((0, 0, val))
            totciun_usa = totciun_usa + self.ciun_mkt_usa
        if (self.ciun_s4_usa > 0):
            val = {'account_id': cta_ciun_S4_usa.id,
                   'currency_id': 19,
                   'debit': self.ciun_s4_usa,
                   'amount_currency': self.ciun_s4_usa}
            lines.append((0, 0, val))
            totciun_usa = totciun_usa + self.ciun_s4_usa
        if (self.ciun_nt_usa > 0):
            val = {'account_id': cta_ciun_NT_usa.id,
                   'currency_id': 19,
                   'debit': self.ciun_nt_usa,
                   'amount_currency': self.ciun_nt_usa}
            lines.append((0, 0, val))
            totciun_usa = totciun_usa + self.ciun_nt_usa
        if (self.ciun_talent_usa > 0):
            val = {'account_id': cta_ciun_talent_usa.id,
                   'currency_id': 19,
                   'debit': self.ciun_talent_usa,
                   'amount_currency': self.ciun_talent_usa}
            lines.append((0, 0, val))
            totciun_usa = totciun_usa + self.ciun_talent_usa
        if (totciun_usa > 0):
            val = {'account_id': cta_acobrar_ic_usa.id,
                   'currency_id': 19,
                   'credit': totciun_usa,
                   'amount_currency': totciun_usa * -1,
                   }
            lines.append((0, 0, val))

            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
            move.action_post()
        # ------ ASIENTO COMISIONES-UN -----------
        # lines = [(5, 0, 0)]
        # val = {'account_id': cta_comisionesun_mex.id,
        #        'currency_id': 19,
        #        'debit': self.comun_mex,
        #        'amount_currency': self.comun_mex}
        # lines.append((0, 0, val))
        # val = {'account_id': cta_comisionesun_usa.id,
        #        'currency_id': 19,
        #        'debit': self.comun_usa,
        #        'amount_currency': self.comun_usa}
        # lines.append((0, 0, val))
        #
        # val = {'account_id': cta_acobrar_ic_mex.id,
        #        'currency_id': 19,
        #        'credit': self.comun_mex,
        #        'amount_currency': self.comun_mex * -1,
        #        }
        # lines.append((0, 0, val))
        # val = {'account_id': cta_acobrar_ic_usa.id,
        #        'currency_id': 19,
        #        'credit': self.comun_usa,
        #        'amount_currency': self.comun_usa * -1,
        #        }
        # lines.append((0, 0, val))
        # move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
        # move.action_post()
        #
        # ------ ASIENTO COMISIONES TALENT -----------

        # lines = [(5, 0, 0)]
        # val = {'account_id': cta_comisionestalent_mex.id,
        #        'currency_id': 19,
        #        'debit': self.comi_mex,
        #        'amount_currency': self.comi_mex}
        # lines.append((0, 0, val))
        # val = {'account_id': cta_comisionestalent_usa.id,
        #        'currency_id': 19,
        #        'debit': self.comi_usa,
        #        'amount_currency': self.comi_usa}
        # lines.append((0, 0, val))
        # 
        # val = {'account_id': cta_acobrar_ic_mex.id,
        #        'currency_id': 19,
        #        'credit': self.comi_mex,
        #        'amount_currency': self.comi_mex * -1,
        #        }
        # lines.append((0, 0, val))
        # val = {'account_id': cta_acobrar_ic_usa.id,
        #        'currency_id': 19,
        #        'credit': self.comi_usa,
        #        'amount_currency': self.comi_usa * -1,
        #        }
        # lines.append((0, 0, val))
        # move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
        # move.action_post()

        # ------ ASIENTO LEADS MKT -----------
        # recruitng mex
        totleadsmkt_mex = 0
        lines = [(5, 0, 0)]
        if (self.leadsmkt_b1_mex > 0):
            val = {'account_id': cta_leads_B1_mex.id,
                   'currency_id': 19,
                   'debit': self.leadsmkt_b1_mex,
                   'amount_currency': self.leadsmkt_b1_mex}
            lines.append((0, 0, val))
            totleadsmkt_mex = totleadsmkt_mex + self.leadsmkt_b1_mex
        if (self.leadsmkt_mkt_mex > 0):
            val = {'account_id': cta_leads_MKT_mex.id,
                   'currency_id': 19,
                   'debit': self.leadsmkt_mkt_mex,
                   'amount_currency': self.leadsmkt_mkt_mex}
            lines.append((0, 0, val))
            totleadsmkt_mex = totleadsmkt_mex + self.leadsmkt_mkt_mex
        if (self.leadsmkt_s4_mex > 0):
            val = {'account_id': cta_leads_S4_mex.id,
                   'currency_id': 19,
                   'debit': self.leadsmkt_s4_mex,
                   'amount_currency': self.leadsmkt_s4_mex}
            lines.append((0, 0, val))
            totleadsmkt_mex = totleadsmkt_mex + self.leadsmkt_s4_mex
        if (self.leadsmkt_nt_mex > 0):
            val = {'account_id': cta_leads_NT_mex.id,
                   'currency_id': 19,
                   'debit': self.leadsmkt_nt_mex,
                   'amount_currency': self.leadsmkt_nt_mex}
            lines.append((0, 0, val))
            totleadsmkt_mex = totleadsmkt_mex + self.leadsmkt_nt_mex
        if (self.leadsmkt_talent_mex > 0):
            val = {'account_id': cta_leads_talent_mex.id,
                   'currency_id': 19,
                   'debit': self.leadsmkt_talent_mex,
                   'amount_currency': self.leadsmkt_talent_mex}
            lines.append((0, 0, val))
            totleadsmkt_mex = totleadsmkt_mex + self.leadsmkt_talent_mex
        if (totleadsmkt_mex > 0):
            val = {'account_id': cta_acobrar_ic_mex.id,
                   'currency_id': 19,
                   'credit': self.totleadsmkt_mex,
                   'amount_currency': self.totleadsmkt_mex * -1,
                   }
            lines.append((0, 0, val))
            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
            move.action_post()

        totleadsmkt_usa = 0
        lines = [(5, 0, 0)]
        if (self.leadsmkt_b1_usa > 0):
            val = {'account_id': cta_leads_B1_usa.id,
                   'currency_id': 19,
                   'debit': self.leadsmkt_b1_usa,
                   'amount_currency': self.leadsmkt_b1_usa}
            lines.append((0, 0, val))
            totleadsmkt_usa = totleadsmkt_usa + self.leadsmkt_b1_usa
        if (self.leadsmkt_mkt_usa > 0):
            val = {'account_id': cta_leads_MKT_usa.id,
                   'currency_id': 19,
                   'debit': self.leadsmkt_mkt_usa,
                   'amount_currency': self.leadsmkt_mkt_usa}
            lines.append((0, 0, val))
            totleadsmkt_usa = totleadsmkt_usa + self.leadsmkt_mkt_usa
        if (self.leadsmkt_s4_usa > 0):
            val = {'account_id': cta_leads_S4_usa.id,
                   'currency_id': 19,
                   'debit': self.leadsmkt_s4_usa,
                   'amount_currency': self.leadsmkt_s4_usa}
            lines.append((0, 0, val))
            totleadsmkt_usa = totleadsmkt_usa + self.leadsmkt_s4_usa
        if (self.leadsmkt_nt_usa > 0):
            val = {'account_id': cta_leads_NT_usa.id,
                   'currency_id': 19,
                   'debit': self.leadsmkt_nt_usa,
                   'amount_currency': self.leadsmkt_nt_usa}
            lines.append((0, 0, val))
            totleadsmkt_usa = totleadsmkt_usa + self.leadsmkt_nt_usa
        if (self.leadsmkt_talent_usa > 0):
            val = {'account_id': cta_leads_talent_usa.id,
                   'currency_id': 19,
                   'debit': self.leadsmkt_talent_usa,
                   'amount_currency': self.leadsmkt_talent_usa}
            lines.append((0, 0, val))
            totleadsmkt_usa = totleadsmkt_usa + self.leadsmkt_talent_usa
        if (totleadsmkt_usa > 0):
            val = {'account_id': cta_acobrar_ic_usa.id,
                   'currency_id': 19,
                   'credit': totleadsmkt_usa,
                   'amount_currency': totleadsmkt_usa * -1,
                   }
            lines.append((0, 0, val))

            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
            move.action_post()
        # publico
        self.state = 'post'

