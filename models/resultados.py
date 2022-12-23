from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

CODCTA_IC_USA='112003'
CODCTA_IC_MEX='112004'
DIARIO =3
COMPANY=1
class TypeResults(models.Model):
    _name = 'type.results'

    resultado=fields.Char('Resultado',required=True)
    grupo = fields.Many2many('intercompany.cost.groups', string='Grupo',required=True)
    ctacontable_mex=fields.Many2one('account.account',string='Cuenta Contable Recupero MEX')
    ctacontable_usa = fields.Many2one('account.account', string='Cuenta Contable Recupero USA')
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
        #***********  PROCESO RECRUITING *******************
        recruiting = self.env['type.results'].search([('resultado', '=', 'RECRUITING')], limit=1)
        if recruiting:
            # Si encuentra la configuracion busco los grupos
            suma_resultado = 0
            for grupo in recruiting.grupo:
                # por cada grupo, busco las cuentas relacionadas
                suma_grupo = 0
                cuentas = self.env['account.account'].search([('grupo', '=', grupo.id)])
                #_logger.info('GRUPO:' + grupo.name + 'CUENTAS:' + str(cuentas))
                for cuenta in cuentas:
                    request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + " and parent_state='posted' and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['balance_account']:
                            suma_grupo += record['balance_account']
                # mando a log el total por grupo
                suma_resultado += suma_grupo
                #_logger.info('TOTAL grupo:' + str(suma_resultado))
                #_logger.info(' revenue mex:' + str(self.revenue_interco_mex))
                #_logger.info(' revenue usa:' + str(self.revenue_interco_usa))
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
            _logger.info('ACA GRUPO MKT :')
            _logger.info('   suma b1:' + str(suma_b1))
            _logger.info('   suma nt:' + str(suma_nt))
            _logger.info('   suma mkt:' + str(suma_mkt) + ' total_mkt:' + str(self.revenue_interco_total_mkt))
            _logger.info('   suma s4:' + str(suma_s4))
            _logger.info('   suma tlatam:' + str(suma_tlatam))
            _logger.info('   suma talentusa:' + str(suma_tusa))
            # calculos finales-----
            mkt_b1_usa,mkt_nt_usa, mkt_mkt_usa, mkt_s4_usa,mkt_latam_usa, mkt_usa_usa =0,0,0,0,0,0
            if self.revenue_interco_total_b1>0:
                mkt_b1_usa=suma_b1 * (self.revenue_b1_usa/self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_usa:' + str(
                    self.revenue_b1_usa / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt>0:
                porc_mkt_revenue=0.00
                porc_mkt_revenue=self.revenue_mkt_usa/self.revenue_interco_total_mkt
                mkt_mkt_usa=suma_mkt * porc_mkt_revenue
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_usa:' + str(
                porc_mkt_revenue))
            if self.revenue_interco_total_nt>0:
                mkt_nt_usa=suma_nt * (self.revenue_nt_usa/self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_usa:' + str(
                    self.revenue_nt_usa / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4>0:
                mkt_s4_usa= suma_s4 * (self.revenue_s4_usa / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_usa:' + str(
                    self.revenue_s4_usa / self.revenue_interco_total_s4))
            # usa no suma tlatam
            if self.revenue_interco_total_usa>0:
                mkt_usa_usa=suma_tusa * (self.revenue_tusa_usa / self.revenue_interco_total_usa)
                _logger.info('  suma_tusa:' + str(suma_tusa) + ' revenue_tusa_usa:' + str(
                    self.revenue_tusa_usa / self.revenue_interco_total_usa))
            self.mkt_usa = mkt_b1_usa + mkt_nt_usa + mkt_mkt_usa + mkt_s4_usa+ mkt_latam_usa +mkt_usa_usa
            _logger.info('   b1 usa:' + str(mkt_b1_usa))
            _logger.info('   nt usa:' + str(mkt_nt_usa))
            _logger.info('   mkt usa:' + str(mkt_mkt_usa))
            _logger.info('   s4 usa:' + str(mkt_s4_usa))
            _logger.info('   tlatam:' + str(mkt_latam_usa))
            _logger.info('   tusa:' + str(mkt_usa_usa))
            # calculos mexico
            mkt_b1_mex, mkt_nt_mex, mkt_mkt_mex, mkt_s4_mex, mkt_mex_latam = 0, 0, 0, 0, 0
            if self.revenue_interco_total_b1 > 0:
                mkt_b1_mex = suma_b1 * (self.revenue_b1_mex / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_mex:' + str(
                    self.revenue_b1_mex / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                porc_mkt_revenue = 0.00
                porc_mkt_revenue = self.revenue_mkt_mex / self.revenue_interco_total_mkt
                mkt_mkt_mex = suma_mkt * porc_mkt_revenue
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_mex:' + str(
                    porc_mkt_revenue))
            if self.revenue_interco_total_nt > 0:
                mkt_nt_mex = suma_nt * (self.revenue_nt_mex / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_mex:' + str(
                    self.revenue_nt_mex / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                mkt_s4_mex = suma_s4 * (self.revenue_s4_mex / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_mex:' + str(
                    self.revenue_s4_mex / self.revenue_interco_total_s4))
            # mex no suma tusa
            if self.revenue_interco_total_latam > 0:
                mkt_mex_tlatam = suma_tlatam * (self.revenue_tlatam_mex / self.revenue_interco_total_latam)
                _logger.info('  suma_tlatam:' + str(suma_tlatam) + ' revenue_tmex_mex:' + str(
                    self.revenue_tlatam_mex / self.revenue_interco_total_latam))
            self.mkt_mex = mkt_b1_mex + mkt_nt_mex + mkt_mkt_mex + mkt_s4_mex + mkt_mex_tlatam
            _logger.info('---------MEX--------- :')

            _logger.info('   b1 mex:' + str(mkt_b1_mex))
            _logger.info('   nt mex:' + str(mkt_nt_mex))
            _logger.info('   mkt mex:' + str(mkt_mkt_mex))
            _logger.info('   s4 mex:' + str(mkt_s4_mex))
            _logger.info('   tlatam:' + str(mkt_mex_tlatam))

            self.mkt_total = self.mkt_usa + self.mkt_mex
        # ---------------- PROCESO OP -----------------
        op = self.env['type.results'].search([('resultado', '=', 'OP')], limit=1)
        if op:
            suma_mkt, suma_b1, suma_nt, suma_s4, suma_tusa, suma_tlatam = 0, 0, 0, 0, 0, 0
            for grupo in op.grupo:
                suma_b1= self.calc_subgrupos('B1',grupo.id)
                suma_nt = self.calc_subgrupos('NT', grupo.id)
                suma_mkt = self.calc_subgrupos('MKT', grupo.id)
                suma_s4 = self.calc_subgrupos('S4', grupo.id)
                suma_tusa = self.calc_subgrupos('TUSA', grupo.id)
                suma_tlatam = self.calc_subgrupos('TLATAM', grupo.id)
            _logger.info('ACA GRUPO OP :')
            _logger.info('   suma b1:' + str(suma_b1))
            _logger.info('   suma nt:' + str(suma_nt))
            _logger.info('   suma mkt:' + str(suma_mkt) + ' total_mkt:' + str(self.revenue_interco_total_mkt))
            _logger.info('   suma s4:' + str(suma_s4))
            _logger.info('   suma tlatam:' + str(suma_tlatam))
            _logger.info('   suma talentusa:' + str(suma_tusa))
            # calculos finales-----
            op_b1_usa,op_nt_usa, op_mkt_usa, op_s4_usa,op_latam_usa, op_usa_usa =0,0,0,0,0,0
            if self.revenue_interco_total_b1>0:
                op_b1_usa=suma_b1 * (self.revenue_b1_usa/self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_usa:' + str(
                    self.revenue_b1_usa / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt>0:
                op_mkt_usa=suma_mkt * (self.revenue_mkt_usa/self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_usa:' + str(
                    self.revenue_mkt_usa / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt>0:
                op_nt_usa=suma_nt * (self.revenue_nt_usa/self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_usa:' + str(
                    self.revenue_nt_usa / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4>0:
                op_s4_usa= suma_s4 * (self.revenue_s4_usa / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_usa:' + str(
                    self.revenue_s4_usa / self.revenue_interco_total_s4))
            # usa no suma tlatam
            if self.revenue_interco_total_usa>0:
                op_usa_usa=suma_tusa * (self.revenue_tusa_usa / self.revenue_interco_total_usa)
                _logger.info('  suma_tusa:' + str(suma_tusa) + ' revenue_tusa_usa:' + str(
                    self.revenue_tusa_usa / self.revenue_interco_total_usa))
            self.op_usa = op_b1_usa + op_nt_usa + op_mkt_usa + op_s4_usa+ op_latam_usa +op_usa_usa
            _logger.info('ACA GRUPO OPERACIONES :')

            _logger.info('   b1 usa:' + str(op_b1_usa))
            _logger.info('   nt usa:' + str(op_nt_usa))
            _logger.info('   mkt usa:' + str(op_mkt_usa))
            _logger.info('   s4 usa:' + str(op_s4_usa))
            _logger.info('   tlatam:' + str(op_latam_usa))
            _logger.info('   tusa:' + str(op_usa_usa))
            # calculos mexico
            op_b1_mex, op_nt_mex, op_mkt_mex, op_s4_mex, op_latam_mex, op_mkt_mex = 0, 0, 0, 0, 0, 0
            if self.revenue_interco_total_b1 > 0:
                op_b1_mex = suma_b1 * (self.revenue_b1_mex / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_mex:' + str(
                    self.revenue_b1_mex / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                op_op_mex = suma_mkt * self.revenue_mkt_mex / self.revenue_interco_total_mkt
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_mex:' + str(
                    self.revenue_mkt_mex / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                op_nt_mex = suma_nt * (self.revenue_nt_mex / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_mex:' + str(
                    self.revenue_nt_mex / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                op_s4_mex = suma_s4 * (self.revenue_s4_mex / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_mex:' + str(
                    self.revenue_s4_mex / self.revenue_interco_total_s4))
            # mex no suma tusa
            if self.revenue_interco_total_latam > 0:
                op_mex_tlatam = suma_tlatam * (self.revenue_tlatam_mex / self.revenue_interco_total_latam)
                _logger.info('  suma_tlatam:' + str(suma_tlatam) + ' revenue_tmex_mex:' + str(
                    self.revenue_tlatam_mex / self.revenue_interco_total_latam))
            self.op_mex = op_b1_mex + op_nt_mex + op_mkt_mex + op_s4_mex +  op_mex_tlatam
            _logger.info('---------MEX--------- :')

            _logger.info('   b1 mex:' + str(op_b1_mex))
            _logger.info('   nt mex:' + str(op_nt_mex))
            _logger.info('   mkt mex:' + str(op_op_mex))
            _logger.info('   s4 mex:' + str(op_s4_mex))
            _logger.info('   tlatam:' + str(op_mex_tlatam))

            # calculos Arg
            op_b1_arg, op_nt_arg, op_mkt_arg, op_s4_arg, op_latam_arg, op_mkt_arg = 0, 0, 0, 0, 0, 0
            if self.revenue_interco_total_b1 > 0:
                op_b1_arg = suma_b1 * (self.revenue_b1_arg / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_arg:' + str(
                    self.revenue_b1_arg / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                op_op_arg = suma_mkt * self.revenue_mkt_arg / self.revenue_interco_total_mkt
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
            _logger.info('   mkt arg:' + str(op_op_arg))
            _logger.info('   s4 arg:' + str(op_s4_arg))
            _logger.info('   tlatam:' + str(op_arg_tlatam))

            self.op_total = self.op_usa + self.op_mex + self.op_arg
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
            _logger.info('ACA GRUPO SALES :')
            _logger.info('   suma b1:' + str(suma_b1))
            _logger.info('   suma nt:' + str(suma_nt))
            _logger.info('   suma mkt:' + str(suma_mkt) )
            _logger.info('   suma s4:' + str(suma_s4))
            _logger.info('   suma tlatam:' + str(suma_tlatam))
            _logger.info('   suma talentusa:' + str(suma_tusa))
            # calculos finales-----
            sales_b1_usa, sales_nt_usa, sales_mkt_usa, sales_s4_usa, sales_latam_usa, sales_usa_usa = 0, 0, 0, 0, 0, 0
            if self.revenue_interco_total_b1 > 0:
                sales_b1_usa = suma_b1 * (self.revenue_b1_usa / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_usa:' + str(
                    self.revenue_b1_usa / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                sales_mkt_usa = suma_mkt * (self.revenue_mkt_usa / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_usa:' + str(
                    self.revenue_mkt_usa / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                sales_nt_usa = suma_nt * (self.revenue_nt_usa / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_usa:' + str(
                    self.revenue_nt_usa / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                sales_s4_usa = suma_s4 * (self.revenue_s4_usa / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_usa:' + str(
                    self.revenue_s4_usa / self.revenue_interco_total_s4))
            # usa no suma tlatam
            if self.revenue_interco_total_usa > 0:
                sales_usa_usa = suma_tusa * (self.revenue_tusa_usa / self.revenue_interco_total_usa)
                _logger.info('  suma_tusa:' + str(suma_tusa) + ' revenue_tusa_usa:' + str(
                    self.revenue_tusa_usa / self.revenue_interco_total_usa))
            self.sales_usa = sales_b1_usa + sales_nt_usa + sales_mkt_usa + sales_s4_usa + sales_latam_usa + sales_usa_usa
            _logger.info('   b1 usa:' + str(sales_b1_usa))
            _logger.info('   nt usa:' + str(sales_nt_usa))
            _logger.info('   mkt usa:' + str(sales_mkt_usa))
            _logger.info('   s4 usa:' + str(sales_s4_usa))
            _logger.info('   tlatam:' + str(sales_latam_usa))
            _logger.info('   tusa:' + str(sales_usa_usa))
            # calculos mexico
            sales_b1_mex, sales_nt_mex, sales_mkt_mex, sales_s4_mex, sales_mex_latam = 0, 0, 0, 0, 0
            if self.revenue_interco_total_b1 > 0:
                sales_b1_mex = suma_b1 * (self.revenue_b1_mex / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_mex:' + str(
                    self.revenue_b1_mex / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                sales_mkt_mex = suma_mkt * ( self.revenue_mkt_mex / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_sales_mex:' + str(
                    self.revenue_mkt_mex / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                sales_nt_mex = suma_nt * (self.revenue_nt_mex / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_mex:' + str(
                    self.revenue_nt_mex / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                sales_s4_mex = suma_s4 * (self.revenue_s4_mex / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_mex:' + str(
                    self.revenue_s4_mex / self.revenue_interco_total_s4))
            # mex no suma tusa
            if self.revenue_interco_total_latam > 0:
                sales_mex_tlatam = suma_tlatam * (self.revenue_tlatam_mex / self.revenue_interco_total_latam)
                _logger.info('  suma_tlatam:' + str(suma_tlatam) + ' revenue_tmex_mex:' + str(
                    self.revenue_tlatam_mex / self.revenue_interco_total_latam))
            self.sales_mex = sales_b1_mex + sales_nt_mex + sales_mkt_mex + sales_s4_mex + sales_mex_tlatam
            _logger.info('---------MEX--------- :')

            _logger.info('   b1 mex:' + str(sales_b1_mex))
            _logger.info('   nt mex:' + str(sales_nt_mex))
            _logger.info('   mkt mex:' + str(sales_mkt_mex))
            _logger.info('   s4 mex:' + str(sales_s4_mex))
            _logger.info('   tlatam:' + str(sales_mex_tlatam))

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
            _logger.info('ACA GRUPO PRESALES :')
            _logger.info('   suma b1:' + str(suma_b1))
            _logger.info('   suma nt:' + str(suma_nt))
            _logger.info('   suma mkt:' + str(suma_mkt))
            _logger.info('   suma s4:' + str(suma_s4))
            _logger.info('   suma tlatam:' + str(suma_tlatam))
            _logger.info('   suma talentusa:' + str(suma_tusa))
            # calculos finales-----
            presales_b1_usa, presales_nt_usa, presales_mkt_usa, presales_s4_usa, presales_latam_usa, presales_usa_usa = 0, 0, 0, 0, 0, 0
            if self.revenue_interco_total_b1 > 0:
                presales_b1_usa = suma_b1 * (self.revenue_b1_usa / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_usa:' + str(
                    self.revenue_b1_usa / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                presales_mkt_usa = suma_mkt * (self.revenue_mkt_usa / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_usa:' + str(
                    self.revenue_mkt_usa / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                presales_nt_usa = suma_nt * (self.revenue_nt_usa / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_usa:' + str(
                    self.revenue_nt_usa / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                presales_s4_usa = suma_s4 * (self.revenue_s4_usa / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_usa:' + str(
                    self.revenue_s4_usa / self.revenue_interco_total_s4))
            # usa no suma tlatam
            if self.revenue_interco_total_usa > 0:
                presales_usa_usa = suma_tusa * (self.revenue_tusa_usa / self.revenue_interco_total_usa)
                _logger.info('  suma_tusa:' + str(suma_tusa) + ' revenue_tusa_usa:' + str(
                    self.revenue_tusa_usa / self.revenue_interco_total_usa))
            # busco en ctas comunes

            self.presales_usa = presales_b1_usa + presales_nt_usa + presales_mkt_usa + presales_s4_usa + presales_latam_usa + presales_usa_usa
            _logger.info('   b1 usa:' + str(presales_b1_usa))
            _logger.info('   nt usa:' + str(presales_nt_usa))
            _logger.info('   mkt usa:' + str(presales_mkt_usa))
            _logger.info('   s4 usa:' + str(presales_s4_usa))
            _logger.info('   tlatam:' + str(presales_latam_usa))
            _logger.info('   tusa:' + str(presales_usa_usa))
            # calculos mexico
            presales_b1_mex, presales_nt_mex, presales_mkt_mex, presales_s4_mex, presales_mex_latam = 0, 0, 0, 0, 0
            if self.revenue_interco_total_b1 > 0:
                presales_b1_mex = suma_b1 * (self.revenue_b1_mex / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_mex:' + str(
                    self.revenue_b1_mex / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                presales_mkt_mex = suma_mkt * (self.revenue_mkt_mex / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_presales_mex:' + str(
                    self.revenue_mkt_mex / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                presales_nt_mex = suma_nt * (self.revenue_nt_mex / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_mex:' + str(
                    self.revenue_nt_mex / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                presales_s4_mex = suma_s4 * (self.revenue_s4_mex / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_mex:' + str(
                    self.revenue_s4_mex / self.revenue_interco_total_s4))
            # mex no suma tusa
            if self.revenue_interco_total_latam > 0:
                presales_mex_tlatam = suma_tlatam * (self.revenue_tlatam_mex / self.revenue_interco_total_latam)
                _logger.info('  suma_tlatam:' + str(suma_tlatam) + ' revenue_tmex_mex:' + str(
                    self.revenue_tlatam_mex / self.revenue_interco_total_latam))
            self.presales_mex = presales_b1_mex + presales_nt_mex + presales_mkt_mex + presales_s4_mex + presales_mex_tlatam
            _logger.info('---------MEX--------- :')

            _logger.info('   b1 mex:' + str(presales_b1_mex))
            _logger.info('   nt mex:' + str(presales_nt_mex))
            _logger.info('   mkt mex:' + str(presales_mkt_mex))
            _logger.info('   s4 mex:' + str(presales_s4_mex))
            _logger.info('   tlatam:' + str(presales_mex_tlatam))

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
            _logger.info('ACA GRUPO CI-UN :')
            _logger.info('   suma b1:' + str(suma_b1))
            _logger.info('   suma nt:' + str(suma_nt))
            _logger.info('   suma mkt:' + str(suma_mkt))
            _logger.info('   suma s4:' + str(suma_s4))
            _logger.info('   suma tlatam:' + str(suma_tlatam))
            _logger.info('   suma talentusa:' + str(suma_tusa))
            # calculos finales-----
            ciun_b1_usa, ciun_nt_usa, ciun_mkt_usa, ciun_s4_usa, ciun_latam_usa, ciun_usa_usa = 0, 0, 0, 0, 0, 0
            if self.revenue_interco_total_b1 > 0:
                ciun_b1_usa = suma_b1 * (self.revenue_b1_usa / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_usa:' + str(
                    self.revenue_b1_usa / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                ciun_mkt_usa = suma_mkt * (self.revenue_mkt_usa / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_mkt_usa:' + str(
                    self.revenue_mkt_usa / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                ciun_nt_usa = suma_nt * (self.revenue_nt_usa / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_usa:' + str(
                    self.revenue_nt_usa / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                ciun_s4_usa = suma_s4 * (self.revenue_s4_usa / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_usa:' + str(
                    self.revenue_s4_usa / self.revenue_interco_total_s4))
            # usa no suma tlatam
            if self.revenue_interco_total_usa > 0:
                ciun_usa_usa = suma_tusa * (self.revenue_tusa_usa / self.revenue_interco_total_usa)
                _logger.info('  suma_tusa:' + str(suma_tusa) + ' revenue_tusa_usa:' + str(
                    self.revenue_tusa_usa / self.revenue_interco_total_usa))
            # busco en ctas comunes

            self.ciun_usa = ciun_b1_usa + ciun_nt_usa + ciun_mkt_usa + ciun_s4_usa + ciun_latam_usa + ciun_usa_usa
            _logger.info('   b1 usa:' + str(ciun_b1_usa))
            _logger.info('   nt usa:' + str(ciun_nt_usa))
            _logger.info('   mkt usa:' + str(ciun_mkt_usa))
            _logger.info('   s4 usa:' + str(ciun_s4_usa))
            _logger.info('   tlatam:' + str(ciun_latam_usa))
            _logger.info('   tusa:' + str(ciun_usa_usa))
            # calculos mexico
            ciun_b1_mex, ciun_nt_mex, ciun_mkt_mex, ciun_s4_mex, ciun_mex_latam = 0, 0, 0, 0, 0
            if self.revenue_interco_total_b1 > 0:
                ciun_b1_mex = suma_b1 * (self.revenue_b1_mex / self.revenue_interco_total_b1)
                _logger.info('  suma_b1:' + str(suma_b1) + ' revenue_b1_mex:' + str(
                    self.revenue_b1_mex / self.revenue_interco_total_b1))
            if self.revenue_interco_total_mkt > 0:
                ciun_mkt_mex = suma_mkt * (self.revenue_mkt_mex / self.revenue_interco_total_mkt)
                _logger.info('  suma_mkt:' + str(suma_mkt) + ' revenue_ciun_mex:' + str(
                    self.revenue_mkt_mex / self.revenue_interco_total_mkt))
            if self.revenue_interco_total_nt > 0:
                ciun_nt_mex = suma_nt * (self.revenue_nt_mex / self.revenue_interco_total_nt)
                _logger.info('  suma_nt:' + str(suma_nt) + ' revenue_nt_mex:' + str(
                    self.revenue_nt_mex / self.revenue_interco_total_nt))
            if self.revenue_interco_total_s4 > 0:
                ciun_s4_mex = suma_s4 * (self.revenue_s4_mex / self.revenue_interco_total_s4)
                _logger.info('  suma_s4:' + str(suma_s4) + ' revenue_s4_mex:' + str(
                    self.revenue_s4_mex / self.revenue_interco_total_s4))
            # mex no suma tusa
            if self.revenue_interco_total_latam > 0:
                ciun_mex_tlatam = suma_tlatam * (self.revenue_tlatam_mex / self.revenue_interco_total_latam)
                _logger.info('  suma_tlatam:' + str(suma_tlatam) + ' revenue_tmex_mex:' + str(
                    self.revenue_tlatam_mex / self.revenue_interco_total_latam))
            self.ciun_mex = ciun_b1_mex + ciun_nt_mex + ciun_mkt_mex + ciun_s4_mex + ciun_mex_tlatam
            _logger.info('---------MEX--------- :')

            _logger.info('   b1 mex:' + str(ciun_b1_mex))
            _logger.info('   nt mex:' + str(ciun_nt_mex))
            _logger.info('   mkt mex:' + str(ciun_mkt_mex))
            _logger.info('   s4 mex:' + str(ciun_s4_mex))
            _logger.info('   tlatam:' + str(ciun_mex_tlatam))

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
                    request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + "  and parent_state='posted' and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['balance_account']:
                            suma_grupo_usa += record['balance_account']
                # -------------MEX
                cuentas_mex = self.env['account.account'].search([('grupo', '=', grupo.id), ('pais', '=', 'MEX')])
           #     _logger.info('GRUPO:' + grupo.name + 'CUENTAS MEX:' + str(cuentas_usa))
                for cuenta in cuentas_mex:
                    request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + " and parent_state='posted' and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"
             #       _logger.info('QUERY:' + request)
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['balance_account']:
                            suma_grupo_mex += record['balance_account']

            # calculos finales-----
            # _logger.info('GRUPO COMISIONES MKT')
            # _logger.info(' total:' + str(suma_grupo_usa))
            self.comimkt_usa = suma_grupo_usa
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
       #         _logger.info('GRUPO:' + grupo.name + 'CUENTAS USA:' + str(cuentas_usa))
                for cuenta in cuentas_usa:
                    request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + " and parent_state='posted' and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['balance_account']:
                            suma_grupo_usa += record['balance_account']
                # -------------MEX
                cuentas_mex = self.env['account.account'].search([('grupo', '=', grupo.id), ('pais', '=', 'MEX')])
          #      _logger.info('GRUPO:' + grupo.name + 'CUENTAS MEX:' + str(cuentas_usa))
                for cuenta in cuentas_mex:
                    request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
                              " WHERE account_id = " + str(cuenta.id) + " and parent_state='posted' and date_part('month',date)=" + str(
                        self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"
                    self.env.cr.execute(request)
                    for record in self.env.cr.dictfetchall():
                        if record['balance_account']:
                            suma_grupo_mex += record['balance_account']

                # calculos finales-----
                # _logger.info('GRUPO LEADS MKT')
                # _logger.info(' total:' + str(suma_grupo_usa))
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
       #         _logger.info('GRUPO:' + grupo.name + 'CUENTAS USA:' + str(cuentas_usa))
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
        # CALCULA SOBRE SUMA DE GRUPOS COMO EN RECRUITING
        comisiones = self.env['type.results'].search([('resultado', '=', 'CI')], limit=1)
        if comisiones:
            # Si encuentra la configuracion busco los grupos
            suma_resultado = 0
            for grupo in comisiones.grupo:
                # ----------- busca en ctas contables COMUNES
                #request_cta = "SELECT account_id as id, centro_costos FROM intercompany_cost_ctascomunes as cta where cta.grupo_id= " \
                #              + str(grupo.id)
#                self.env.cr.execute(request_cta)
 #               _logger.info('Busco Ctas Comunes:' + request_cta)

                cuentas_comunes= self.env['intercompany.cost.ctascomunes'].search([('grupo_id','=',grupo.id)])
                _logger.info('grupo ci:' + str(grupo.id))
                _logger.info('cuentas_comunes:' + str(cuentas_comunes))
                suma_grupo=0
                if cuentas_comunes:
                    for record_cta in cuentas_comunes:
                        _logger.info('GRUPO CI :' + grupo.name + 'CUENTAS comunes:' + str(record_cta))
                        request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
                                  " WHERE account_id = " + str(record_cta.account_id.id) + " and parent_state='posted'  " \
                                                                                   " and analytic_account_id=" + str(
                            record_cta.centro_costos.id) + " and date_part('month',date)=" + str(
                            self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"
                        _logger.info('QUERY:' + request)
                        self.env.cr.execute(request)
                        for record in self.env.cr.dictfetchall():
                            if record['balance_account']:
                                _logger.info(
                                    '  parcial cta comun :' + str(record_cta['id']) + '- centro costo :' + str(record_cta['centro_costos']) + ' $' + str(
                                        record['balance_account']))
                                suma_grupo += record['balance_account']
                    _logger.info('TOTAL grupo:' + str(suma_grupo))
                    suma_resultado += suma_grupo
                else:
                    #sino tenia datos en ctas comunes busco las cuentas relacionadas al grupo en su totalidad
                    suma_grupo = 0
                    cuentas = self.env['account.account'].search([('grupo', '=', grupo.id)])
                    _logger.info('GRUPO CI :' + grupo.name + 'CUENTAS:' + str(cuentas))
                    for cuenta in cuentas:
                        request = "SELECT  SUM(balance) as balance_account  FROM account_move_line " \
                                  " WHERE account_id = " + str(cuenta.id) + " and parent_state='posted' and date_part('month',date)=" + str(
                            self.mes) + " and date_part('year',date)=" + str(self.anio) + " and company_id=1"
                        _logger.info(request)
                        self.env.cr.execute(request)
                        for record in self.env.cr.dictfetchall():
                            if record['balance_account']:
                                suma_grupo += record['balance_account']

                    # mando a log el total por grupo
                    _logger.info('TOTAL grupo:' + str(suma_grupo))
                    suma_resultado += suma_grupo
            # calculos finales-----
            _logger.info('suma total CI:' + str(suma_resultado))
            _logger.info('revenue mex:' + str(self.revenue_interco_mex))
            _logger.info('revenue usa:' + str(self.revenue_interco_usa))
            self.ci_mex = (suma_resultado * self.revenue_interco_mex)
            self.ci_usa = (suma_resultado * self.revenue_interco_usa)
            #self.ci_arg = (suma_resultado * self.revenue_interco_arg)
            self.ci_total = self.ci_mex + self.ci_usa

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
    #busco cuentas, luego genero asientos
        cta_recruiting_mex,cta_recruiting_usa =None,None
        cta_mkt_mex, cta_mkt_usa = None, None
        cta_op_mex, cta_op_usa = None, None
        cta_ci_mex, cta_ci_usa = None, None
        cta_sales_mex, cta_sales_usa = None, None
        cta_presales_mex, cta_presales_usa = None, None
        cta_ciun_mex, cta_ciun_usa = None, None
        cta_comisionesun_mex, cta_comisionesun_usa = None, None
        cta_comisionesmkt_mex, cta_comisionesmkt_usa = None, None
        cta_comisionestalent_mex, cta_comisionestalent_usa = None, None
        cta_leadsmkt_mex, cta_leadsmkt_usa = None, None
        cuentas = self.env['type.results'].search([('resultado', '=', 'RECRUITING')])
        for ctas in cuentas:
            cta_recruiting_mex= ctas.ctacontable_mex
            cta_recruiting_usa = ctas.ctacontable_usa
        if  not(cta_recruiting_mex) or not(cta_recruiting_usa):
            raise UserError(('Falta definir las cuentas contables de recupero para RECRUITiNG'))
        #--------------------------------------------------#
        cuentas = self.env['type.results'].search([('resultado', '=', 'MKT')])
        for ctas in cuentas:
            cta_mkt_mex= ctas.ctacontable_mex
            cta_mkt_usa = ctas.ctacontable_usa
        if  not(cta_mkt_mex) or not(cta_mkt_usa):
            raise UserError(('Falta definir las cuentas contables de recupero para MKT'))
        # --------------------------------------------------#
        cuentas = self.env['type.results'].search([('resultado', '=', 'OP')])
        for ctas in cuentas:
            cta_op_mex = ctas.ctacontable_mex
            cta_op_usa = ctas.ctacontable_usa
        if not (cta_op_mex) or not (cta_op_usa):
            raise UserError(('Falta definir las cuentas contables de recupero para OP'))
        # --------------------------------------------------#
        cuentas = self.env['type.results'].search([('resultado', '=', 'CI')])
        for ctas in cuentas:
            cta_ci_mex = ctas.ctacontable_mex
            cta_ci_usa = ctas.ctacontable_usa
        if not (cta_ci_mex) or not (cta_ci_usa):
            raise UserError(('Falta definir las cuentas contables de recupero para CI'))
        # --------------------------------------------------#
        cuentas = self.env['type.results'].search([('resultado', '=', 'SALES')])
        for ctas in cuentas:
            cta_sales_mex = ctas.ctacontable_mex
            cta_sales_usa = ctas.ctacontable_usa
        if not (cta_sales_mex) or not (cta_sales_usa):
            raise UserError(('Falta definir las cuentas contables de recupero para SALES'))
        # --------------------------------------------------#
        cuentas = self.env['type.results'].search([('resultado', '=', 'PRESALES')])
        for ctas in cuentas:
            cta_presales_mex = ctas.ctacontable_mex
            cta_presales_usa = ctas.ctacontable_usa
        if not (cta_presales_mex) or not (cta_presales_usa):
            raise UserError(('Falta definir las cuentas contables de recupero para PRESALES'))
        # --------------------------------------------------#
        cuentas = self.env['type.results'].search([('resultado', '=', 'CI-UN')])
        for ctas in cuentas:
            cta_ciun_mex = ctas.ctacontable_mex
            cta_ciun_usa = ctas.ctacontable_usa
        if not (cta_ciun_mex) or not (cta_ciun_usa):
            raise UserError(('Falta definir las cuentas contables de recupero para CI-UN'))
        #--------------------------------------------------------
        cuentas = self.env['type.results'].search([('resultado', '=', 'COMISIONES UN')])
        for ctas in cuentas:
            cta_comisionesun_mex = ctas.ctacontable_mex
            cta_comisionesun_usa = ctas.ctacontable_usa
        if not (cta_comisionesun_mex) or not (cta_comisionesun_usa):
            raise UserError(('Falta definir las cuentas contables de recupero para COMISIONES UN'))
        #--------------------------------------------------------
        cuentas = self.env['type.results'].search([('resultado', '=', 'COMISIONES MKT')])
        for ctas in cuentas:
            cta_comisionesmkt_mex = ctas.ctacontable_mex
            cta_comisionesmkt_usa = ctas.ctacontable_usa
        if not (cta_comisionesmkt_mex) or not (cta_comisionesmkt_usa):
            raise UserError(('Falta definir las cuentas contables de recupero para COMISIONES MKT'))
        #--------------------------------------------------------
        cuentas = self.env['type.results'].search([('resultado', '=', 'COMISIONES TALENT')])
        for ctas in cuentas:
            cta_comisionestalent_mex = ctas.ctacontable_mex
            cta_comisionestalent_usa = ctas.ctacontable_usa
        if not (cta_comisionestalent_mex) or not (cta_comisionestalent_usa):
            raise UserError(('Falta definir las cuentas contables de recupero para COMISIONES TALENT'))
        #--------------------------------------------------------
        cuentas = self.env['type.results'].search([('resultado', '=', 'LEADS MKT')])
        for ctas in cuentas:
            cta_leadsmkt_mex = ctas.ctacontable_mex
            cta_leadsmkt_usa = ctas.ctacontable_usa
        if not (cta_leadsmkt_mex) or not (cta_leadsmkt_usa):
            raise UserError(('Falta definir las cuentas contables de recupero para LEADS MKT'))

        #**************** genero asientos  ***********************
        cta_acobrar_ic_mex = self.env['account.account'].search([('code', '=', CODCTA_IC_MEX)])
        cta_acobrar_ic_usa = self.env['account.account'].search([('code', '=', CODCTA_IC_USA)])

            # ------ ASIENTO RECRUITING-----------
        lines = [(5, 0, 0)]
        val = {'account_id': cta_recruiting_mex.id,
                'currency_id': 19,
                'debit': self.recruiting_mex,
                'amount_currency': self.recruiting_mex}
        lines.append((0, 0, val))
        val = {'account_id': cta_recruiting_usa.id,
               'currency_id': 19,
               'debit': self.recruiting_usa,
               'amount_currency': self.recruiting_usa}
        lines.append((0, 0, val))

        val = {'account_id': cta_acobrar_ic_mex.id,
               'currency_id': 19,
               'credit': self.recruiting_mex,
               'amount_currency': self.recruiting_mex * -1,
               }
        lines.append((0, 0, val))
        val = {'account_id': cta_acobrar_ic_usa.id,
               'currency_id': 19,
               'credit': self.recruiting_usa,
               'amount_currency': self.recruiting_usa * -1,
               }
        lines.append((0, 0, val))
        move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
        move.action_post()
            # ------ ASIENTO MKT-----------
        lines = [(5, 0, 0)]
        val = {'account_id': cta_mkt_mex.id,
               'currency_id': 19,
               'debit': self.mkt_mex,
               'amount_currency': self.mkt_mex}
        lines.append((0, 0, val))
        val = {'account_id': cta_mkt_usa.id,
               'currency_id': 19,
               'debit': self.mkt_usa,
               'amount_currency': self.mkt_usa}
        lines.append((0, 0, val))

        val = {'account_id': cta_acobrar_ic_mex.id,
               'currency_id': 19,
               'credit': self.mkt_mex,
               'amount_currency': self.mkt_mex * -1,
               }
        lines.append((0, 0, val))
        val = {'account_id': cta_acobrar_ic_usa.id,
               'currency_id': 19,
               'credit': self.mkt_usa,
               'amount_currency': self.mkt_usa * -1,
               }
        lines.append((0, 0, val))
        move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
        move.action_post()
        # ------ ASIENTO OP-----------
        lines = [(5, 0, 0)]
        val = {'account_id': cta_op_mex.id,
               'currency_id': 19,
               'debit': self.op_mex,
               'amount_currency': self.op_mex}
        lines.append((0, 0, val))
        val = {'account_id': cta_op_usa.id,
               'currency_id': 19,
               'debit': self.op_usa,
               'amount_currency': self.op_usa}
        lines.append((0, 0, val))

        # val = {'account_id': cta_op_arg.id,
        #        'currency_id': 19,
        #        'debit': self.op_arg,
        #        'amount_currency': self.op_arg}
        # lines.append((0, 0, val))

        val = {'account_id': cta_acobrar_ic_mex.id,
               'currency_id': 19,
               'credit': self.op_mex,
               'amount_currency': self.op_mex * -1,
               }
        lines.append((0, 0, val))
        val = {'account_id': cta_acobrar_ic_usa.id,
               'currency_id': 19,
               'credit': self.op_usa,
               'amount_currency': self.op_usa * -1,
               }
        lines.append((0, 0, val))
        move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
        move.action_post()
        # ------ ASIENTO SALES-----------
        lines = [(5, 0, 0)]
        val = {'account_id': cta_sales_mex.id,
               'currency_id': 19,
               'debit': self.sales_mex,
               'amount_currency': self.sales_mex}
        lines.append((0, 0, val))
        val = {'account_id': cta_sales_usa.id,
               'currency_id': 19,
               'debit': self.sales_usa,
               'amount_currency': self.sales_usa}
        lines.append((0, 0, val))

        val = {'account_id': cta_acobrar_ic_mex.id,
               'currency_id': 19,
               'credit': self.sales_mex,
               'amount_currency': self.sales_mex * -1,
               }
        lines.append((0, 0, val))
        val = {'account_id': cta_acobrar_ic_usa.id,
               'currency_id': 19,
               'credit': self.sales_usa,
               'amount_currency': self.sales_usa * -1,
               }
        lines.append((0, 0, val))
        move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
        move.action_post()

        # ------ ASIENTO PRESALES-----------
        lines = [(5, 0, 0)]
        val = {'account_id': cta_presales_mex.id,
               'currency_id': 19,
               'debit': self.presales_mex,
               'amount_currency': self.presales_mex}
        lines.append((0, 0, val))
        val = {'account_id': cta_presales_usa.id,
               'currency_id': 19,
               'debit': self.presales_usa,
               'amount_currency': self.presales_usa}
        lines.append((0, 0, val))

        val = {'account_id': cta_acobrar_ic_mex.id,
               'currency_id': 19,
               'credit': self.presales_mex,
               'amount_currency': self.presales_mex * -1,
               }
        lines.append((0, 0, val))
        val = {'account_id': cta_acobrar_ic_usa.id,
               'currency_id': 19,
               'credit': self.presales_usa,
               'amount_currency': self.presales_usa * -1,
               }
        lines.append((0, 0, val))
        move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
        move.action_post()

        # ------ ASIENTO CI-----------

        lines = [(5, 0, 0)]
        val = {'account_id': cta_ci_mex.id,
               'currency_id': 19,
               'debit': self.ci_mex,
               'amount_currency': self.ci_mex}
        lines.append((0, 0, val))
        val = {'account_id': cta_ci_usa.id,
               'currency_id': 19,
               'debit': self.ci_usa,
               'amount_currency': self.ci_usa}
        lines.append((0, 0, val))

        val = {'account_id': cta_acobrar_ic_mex.id,
               'currency_id': 19,
               'credit': self.ci_mex,
               'amount_currency': self.ci_mex * -1,
               }
        lines.append((0, 0, val))
        val = {'account_id': cta_acobrar_ic_usa.id,
               'currency_id': 19,
               'credit': self.ci_usa,
               'amount_currency': self.ci_usa * -1,
               }
        lines.append((0, 0, val))
        move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
        move.action_post()

        # ------ ASIENTO CI-UN -----------

        lines = [(5, 0, 0)]
        val = {'account_id': cta_ciun_mex.id,
               'currency_id': 19,
               'debit': self.ciun_mex,
               'amount_currency': self.ciun_mex}
        lines.append((0, 0, val))
        val = {'account_id': cta_ciun_usa.id,
               'currency_id': 19,
               'debit': self.ciun_usa,
               'amount_currency': self.ciun_usa}
        lines.append((0, 0, val))

        val = {'account_id': cta_acobrar_ic_mex.id,
               'currency_id': 19,
               'credit': self.ciun_mex,
               'amount_currency': self.ciun_mex * -1,
               }
        lines.append((0, 0, val))
        val = {'account_id': cta_acobrar_ic_usa.id,
               'currency_id': 19,
               'credit': self.ciun_usa,
               'amount_currency': self.ciun_usa * -1,
               }
        lines.append((0, 0, val))
        move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
        move.action_post()

        # ------ ASIENTO COMISIONES-UN -----------

        lines = [(5, 0, 0)]
        val = {'account_id': cta_comisionesun_mex.id,
               'currency_id': 19,
               'debit': self.comun_mex,
               'amount_currency': self.comun_mex}
        lines.append((0, 0, val))
        val = {'account_id': cta_comisionesun_usa.id,
               'currency_id': 19,
               'debit': self.comun_usa,
               'amount_currency': self.comun_usa}
        lines.append((0, 0, val))

        val = {'account_id': cta_acobrar_ic_mex.id,
               'currency_id': 19,
               'credit': self.comun_mex,
               'amount_currency': self.comun_mex * -1,
               }
        lines.append((0, 0, val))
        val = {'account_id': cta_acobrar_ic_usa.id,
               'currency_id': 19,
               'credit': self.comun_usa,
               'amount_currency': self.comun_usa * -1,
               }
        lines.append((0, 0, val))
        move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
        move.action_post()

        # ------ ASIENTO COMISIONES TALENT -----------

        lines = [(5, 0, 0)]
        val = {'account_id': cta_comisionestalent_mex.id,
               'currency_id': 19,
               'debit': self.comi_mex,
               'amount_currency': self.comi_mex}
        lines.append((0, 0, val))
        val = {'account_id': cta_comisionestalent_usa.id,
               'currency_id': 19,
               'debit': self.comi_usa,
               'amount_currency': self.comi_usa}
        lines.append((0, 0, val))

        val = {'account_id': cta_acobrar_ic_mex.id,
               'currency_id': 19,
               'credit': self.comi_mex,
               'amount_currency': self.comi_mex * -1,
               }
        lines.append((0, 0, val))
        val = {'account_id': cta_acobrar_ic_usa.id,
               'currency_id': 19,
               'credit': self.comi_usa,
               'amount_currency': self.comi_usa * -1,
               }
        lines.append((0, 0, val))
        move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
        move.action_post()

        # ------ ASIENTO LEADS MKT -----------

        lines = [(5, 0, 0)]
        val = {'account_id': cta_leadsmkt_mex.id,
               'currency_id': 19,
               'debit': self.leadsmkt_mex,
               'amount_currency': self.leadsmkt_mex}
        lines.append((0, 0, val))
        val = {'account_id': cta_leadsmkt_usa.id,
               'currency_id': 19,
               'debit': self.leadsmkt_usa,
               'amount_currency': self.leadsmkt_usa}
        lines.append((0, 0, val))

        val = {'account_id': cta_acobrar_ic_mex.id,
               'currency_id': 19,
               'credit': self.leadsmkt_mex,
               'amount_currency': self.leadsmkt_mex * -1,
               }
        lines.append((0, 0, val))
        val = {'account_id': cta_acobrar_ic_usa.id,
               'currency_id': 19,
               'credit': self.leadsmkt_usa,
               'amount_currency': self.leadsmkt_usa * -1,
               }
        lines.append((0, 0, val))
        move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19, 'line_ids': lines})
        move.action_post()

        # publico
        self.state = 'post'

