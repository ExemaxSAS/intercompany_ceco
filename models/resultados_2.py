from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)


class ResultadosInterco2(models.Model):
    _inherit = 'resultados.interco'

    recupero_pais_ids = fields.Many2many('recupero.pais', string='Recupero por País')#, compute='process_results_to')

    def process_results_to(self):
        start_date = date(int(self.anio), int(self.mes), 1)
        end_date = start_date + relativedelta(day=31)
        _logger.info('start_date:' + str(start_date))
        _logger.info('end_date:' + str(end_date))

        # Realizar la consulta para obtener los registros
        # move_lines = self.env['account.move.line'].search([
        move_lines = self.env['account.move.line'].with_company(self.env.company.id).search([
            ('analytic_account_id', '!=', False),
            #('analytic_account_id.aa_region', '=', False), # Traigo todas las que estan sin region / ## TODO filtro para que no traiga CI y COM-LEADS
            ('parent_state', '=', 'posted'),            
            ('date', '>=', start_date),  #.strftime('%Y-%m-%d') #f'{self.anio}-{self.mes}-01'
            ('date', '<=', end_date) #,('company_id', '=', self.current_company_id.id)
            ])

        _logger.info('move_lines:' + str(move_lines))
        
        # Crear un conjunto para almacenar valores únicos de analytic_account_id
        analytic_account_set = set()
        for move_line in move_lines:
            analytic_account_id = move_line.analytic_account_id.id
            if analytic_account_id not in analytic_account_set:
                analytic_account_set.add(analytic_account_id)
            _logger.info('analytic_account_set:' + str(analytic_account_set))
            
        # Convertir el conjunto en una lista si es necesario
        analytic_account_list = list(analytic_account_set)
        _logger.info('analytic_account_list:' + str(analytic_account_list))

        move_lines.read_group(
            domain=[('analytic_account_id', '!=', False)],
            fields=['analytic_account_id', 'balance'],
            groupby=['analytic_account_id']
        )
        _logger.info('move_lines:' + str(move_lines))          

        analytic_totals = {}
        ci_totals = {}
        recupero_view = [(5, 0, 0)]
        for result in move_lines:
            analytic_account_id = result['analytic_account_id'][0]
            balance = result['balance']
            analytic_account_name = analytic_account_id.name
            
            aa_region_code = analytic_account_id.aa_region.code
            code_uniope = analytic_account_id.aa_unit.code
            code_linepl = analytic_account_id.aa_linepl.code
            code_pais = analytic_account_id.aa_pais.code
            valor_pais_recupero = round(balance, 2)

            aa_linepl_code = analytic_account_id.aa_linepl.code

            # Si es Latam Norte suma directo a Mexico
            if aa_region_code == 'LTN' and aa_linepl_code not in ('CO', 'LM'):
                recupero_view.append((0, 0, {
                    'code_uniope': code_uniope,
                    'code_linepl': code_linepl,
                    'valor_pais_recupero': valor_pais_recupero,
                    'pais': 'MEX'
                }))

            # Si es Latam SUR suma directo a Argentina
            elif aa_region_code == 'LTS' and aa_linepl_code not in ('CO', 'LM'):
                recupero_view.append((0, 0, {
                    'code_uniope': code_uniope,
                    'code_linepl': code_linepl,
                    'valor_pais_recupero': valor_pais_recupero,
                    'pais': 'ARG'
                }))

            # Si es COMISIONES o LEADS MKT suma directo sin revenue
            elif aa_linepl_code == 'CO' or aa_linepl_code == 'LM': 
                _logger.info('code_pais:' + str(code_pais))   
                recupero_view.append((0, 0, {
                    'code_uniope': code_uniope,
                    'code_linepl': code_linepl,
                    'valor_pais_recupero': valor_pais_recupero,
                    'pais': code_pais    
                }))

            # elif aa_linepl_code == 'LM':
            #     _logger.info('code_pais:' + str(code_pais)) 
            #     recupero_view.append((0, 0, {
            #         'code_uniope': code_uniope,
            #         'code_linepl': code_linepl,
            #         'valor_pais_recupero': valor_pais_recupero,
            #         'pais': code_pais                    
            #     }))


            # Si es CI multiplico por porcentaje de revenue            
            elif aa_linepl_code == 'CI':                
                if aa_linepl_code not in ci_totals:
                    ci_totals[aa_linepl_code] = {'balance': 0.0, 'object': None}
                ci_totals[aa_linepl_code]['balance'] += balance
                ci_totals[aa_linepl_code]['object'] = result['analytic_account_id']


            # Si es vacio calcula por porcentaje    
            elif not aa_region_code and aa_linepl_code not in ('CO', 'LM', 'CI'):
                # Comprueba si el nombre de la cuenta analítica ya está en el diccionario, si no, inicia
                if analytic_account_name not in analytic_totals:
                    analytic_totals[analytic_account_name] = {'balance': 0.0, 'object': None}

                # Incremento el balance y guarda el objeto analytic_account_id
                analytic_totals[analytic_account_name]['balance'] += balance
                analytic_totals[analytic_account_name]['object'] = result['analytic_account_id']

                _logger.info('balance:' + str(balance))
        _logger.info('ci_totals:' + str(ci_totals))
        _logger.info('analytic_totals:' + str(analytic_totals))

        # for m in analytic_totals.keys():
        #     m.aa_unit
        #     _logger.info('m:' + str(m.aa_unit))
        #     _logger.info('m:' + str(m))    
   
        # Filtrar registros de revenue.interco
        domain = [
            #('pais', 'in', ['ARG', 'MEX', 'USA']),
            ('mes', '=', self.mes),
            ('anio', '=', self.anio)
        ]

        # Lista de unidad/es operativa/s a procesar 
        ## TODO ver el revenue para que si se agregan nuevas unidades operativas las procese sin necesidad de cambiar el codigo ##
        campos = ['totb1', 'totmkt', 'totnt', 'tots4', 'tottalentlatam', 'tottalentusa']
        relacion_campo = {'B1': 'totb1',
                    'MKT': 'totmkt', 
                    'NT': 'totnt', 
                    'S4': 'tots4', 
                    'TL': 'tottalentlatam', 
                    'TU':'tottalentusa'
        }

        suma_campo = {}
        # Calcular la suma de total por unidad operativa (tot-unidad operativa) para los registros encontrados
        for campo in campos:
            sum_campo = round(sum(self.env['revenue.interco'].search(domain).mapped(campo)), 2)
            suma_campo[campo] = sum_campo
            _logger.info('campo:' + str(suma_campo[campo]))

        # # Calcular la suma de tot-unidad operativa para los registros encontrados
        # sum_totb1 = round(sum(self.env['revenue.interco'].search(domain).mapped('totb1')), 2)
        # _logger.info('sum_totb1:' + str(sum_totb1))
        # sum_totmkt = round(sum(self.env['revenue.interco'].search(domain).mapped('totmkt')), 2)
        # _logger.info('sum_totmkt:' + str(sum_totmkt))
        # sum_totnt = round(sum(self.env['revenue.interco'].search(domain).mapped('totnt')), 2)
        # _logger.info('sum_totnt:' + str(sum_totnt))
        # sum_tots4 = round(sum(self.env['revenue.interco'].search(domain).mapped('tots4')), 2)
        # _logger.info('sum_tots4:' + str(sum_tots4))
        # sum_tottalentlatam = round(sum(self.env['revenue.interco'].search(domain).mapped('tottalentlatam')), 2)
        # _logger.info('sum_tottalentlatam:' + str(sum_tottalentlatam))
        # sum_tottalentusa = round(sum(self.env['revenue.interco'].search(domain).mapped('tottalentusa')), 2)
        # _logger.info('sum_tottalentusa:' + str(sum_tottalentusa))

        # Obtengo la lista de paises del revenue
        paises = self.env['revenue.interco'].search(domain).mapped('pais')
        _logger.info('paises:' + str(paises))

        porcentaje_por_pais = {}
        for campo in campos:
            porcentaje_por_pais[campo] = {}
            for pais in paises:
                domain_pais = domain + [('pais', '=', pais)]
                valor_pais  = round(sum(self.env['revenue.interco'].search(domain_pais).mapped(campo)), 2)
                _logger.info('valor_pais:' + str(valor_pais))
                if suma_campo[campo] != 0:
                    porcentaje = ((valor_pais / suma_campo[campo]) * 100)
                    # porcentaje = round(((valor_pais / suma_campo[campo]) * 100), 2)
                else:
                    porcentaje = 0
                porcentaje_por_pais[campo][pais] = porcentaje

                _logger.info('porcentaje_por_pais:' + str(porcentaje_por_pais[campo][pais]))
                _logger.info('Campo: %s, Pais: %s, Porcentaje: %s', campo, pais, porcentaje_por_pais[campo][pais])
        _logger.info('porcentaje_por_pais: %s, Porcentaje: %s', porcentaje_por_pais, porcentaje_por_pais[campo][pais])

        # Actualizar el campo sum_totb1 con la suma calculada
        # self.write({'sum_totb1': sum_totb1})

        recupero = {}
        # recupero_view = []
        for er in analytic_totals:
            _logger.info('analytic_totals: %s', analytic_totals[er])  
            code_uniope = analytic_totals[er]['object'].aa_unit.code 
            _logger.info('code_uniope: %s', code_uniope)
            code_linepl = analytic_totals[er]['object'].aa_linepl.code    


            if code_uniope and code_linepl:
                if code_uniope in relacion_campo and relacion_campo[code_uniope] in porcentaje_por_pais:

                    porcentaje_unit_pais = porcentaje_por_pais[relacion_campo[code_uniope]]
                    _logger.info('porcentaje_unit_pais: %s', porcentaje_unit_pais)

                    valor_pais_recupero = {}
                    for rec in porcentaje_unit_pais:
                        valor_pais_recupero[rec] = round((porcentaje_unit_pais[rec] * analytic_totals[er]['balance']) / 100, 2)
                        _logger.info('valor_pais_recupero: %s', valor_pais_recupero[rec])
                        
                    for pais, valor_pais in valor_pais_recupero.items():
                        recupero_view.append((0, 0, {
                                'code_uniope': code_uniope,
                                'code_linepl': code_linepl,
                                'valor_pais_recupero': valor_pais,
                                'pais': pais
                            }))

                    if code_linepl not in recupero:
                        recupero[code_linepl] = []

                    recupero[code_linepl].append([code_uniope, valor_pais_recupero]) 

        _logger.info('domain que trae : %s', domain) 
        pais_total = self.env['revenue.interco'].read_group(
            domain=domain, 
            fields=['pais', 'total'],
            groupby=['pais']
        )
        _logger.info('pais_total: %s', pais_total)

        total_por_pais = {}
        porcentaje_ci_pais = {}
        suma_total = 0
        for res in pais_total:
            pais = res['pais']
            total = res['total'] if 'total' in res else 0.0
            total_por_pais[pais] = total
            suma_total += total_por_pais[pais]
            
            _logger.info('total_por_pais: %s, Pais: %s', total_por_pais[pais], pais)
        _logger.info('suma_total: %s', suma_total) 

        total_ci_pais = {}
        valor_total_uniope= {}
        for pais, total_pais in total_por_pais.items():
            porcentaj_revenue_pais = (total_por_pais[pais] / suma_total) * 100
            porcentaje_ci_pais[pais] = porcentaj_revenue_pais

            _logger.info('porcentaje_ci_pais: %s, Pais: %s', porcentaje_ci_pais[pais], pais)
            # ci_totals_balance = ci_totals['CI']['balance']
            # ci_totals_balance = ci_totals.get('CI', {}).get('balance', 0)
            if 'CI' in ci_totals:
                ci_totals_balance = ci_totals['CI']['balance']
            else:
                ci_totals_balance = 1
            
            ci_pais = round(ci_totals_balance * porcentaje_ci_pais[pais] / 100, 2)
            total_ci_pais[pais] = ci_pais
            _logger.info('ci_pais: %s', ci_pais) 
            _logger.info('total_ci_pais: %s, pais: %s ', total_ci_pais[pais], pais) 

            ## TODO cuando es CI y LTN o LTS, tengo que sumar al total_ci_pais[pais] Mexico o Argentina

        # Lista de campos porcentajes de unidad/es operativa/s a procesar 
        porc_campo = ['porc_B1', 'porc_MKT', 'porc_NT', 'porc_S4', 'porc_talentlatam', 'porc_talentusa']
        rel_porc_campo = {'porc_B1': 'B1',
                    'porc_MKT': 'MKT', 
                    'porc_NT': 'NT', 
                    'porc_S4': 'S4', 
                    'porc_talentlatam': 'TL', 
                    'porc_talentusa':'TU'
        }
        for campo in porc_campo:
            valor_total_uniope[campo] = {}
            for pais in paises:
                domain_pais = domain + [('pais', '=', pais)]
                valor_porc_uniope = sum(self.env['revenue.interco'].search(domain_pais).mapped(campo))
                valor_total_uniope[campo][pais] = round(valor_porc_uniope * total_ci_pais[pais] / 100, 2)
                _logger.info('valor_porc_uniope:' + str(valor_porc_uniope))

        _logger.info('valor_total_uniope:' + str(valor_total_uniope))  
        _logger.info('ci_totals_balance: %s', ci_totals_balance)   

        for campo, valores_por_pais in valor_total_uniope.items():
            for pais, valor_pais in valores_por_pais.items():
                recupero_view.append((0, 0, {
                        'code_uniope': rel_porc_campo.get(campo),
                        'code_linepl': 'CI',
                        'valor_pais_recupero': valor_pais,
                        'pais': pais
                    }))
                _logger.info('campo: %s, pais: %s, valor_pais: %s', rel_porc_campo.get(campo), pais, valor_pais)
           

        self.recupero_pais_ids = recupero_view
        _logger.info('recupero: %s', recupero) 


         #--------------- FIN CALCULOS -----------------
        self.state = 'checkpoint'
        
     #**********************  FIN PROCESO******************

    def post_prueba(self):
        #PARAMETROS
        CODCTA_IC_USA = self.env['ir.config_parameter'].get_param('codcta_ic_usa-' + str(self.current_company_id.id), '')
        CODCTA_IC_MEX = self.env['ir.config_parameter'].get_param('codcta_ic_mex-' + str(self.current_company_id.id), '')
        CODCTA_IC_ARG = self.env['ir.config_parameter'].get_param('codcta_ic_arg-' + str(self.current_company_id.id), '')

        pdiario = (self.env['ir.config_parameter'].get_param('diario-' + str(self.current_company_id.id)))
        _logger.info('----Diario de asiento final:' + CODCTA_IC_USA)
        _logger.info('----Diario de asiento final:' + CODCTA_IC_MEX)
        _logger.info('----Diario de asiento final:' + CODCTA_IC_ARG)
        _logger.info('----Diario de asiento final:' + pdiario)
        DIARIO = int(pdiario)

        

        lines = []
        suma_linepl_pais = {}
        total_por_pais = {}
        # suma_cuentas = 0
        for rp in self.recupero_pais_ids:
            code_linepl = rp.code_linepl
            pais = rp.pais
            valor_cuenta = rp.valor_pais_recupero
            if (pais, code_linepl) in suma_linepl_pais:
                suma_linepl_pais[(pais, code_linepl)] += valor_cuenta
            else:
                suma_linepl_pais[(pais, code_linepl)] = valor_cuenta   
        
             # Realizar la búsqueda de cuentas en account.account
            # recovery_account = self.env['account.account'].search([('tipo_cuenta', '=', 'recupero'),
            #                                                   ('aa_linepl.code', '=', code_linepl),
            #                                                   ('pais', '=', pais),
            #                                                   ], limit=1)
            # _logger.info('recovery_account: %s', recovery_account)
            # suma_cuentas += rp.valor_pais_recupero
            

            # Verifica si el país está en total_por_pais
            if pais in total_por_pais:
                total_por_pais[pais] += valor_cuenta
            else:
                total_por_pais[pais] = valor_cuenta
            _logger.info('total_por_pais: %s', total_por_pais) 
            _logger.info('suma_linepl_pais: %s', suma_linepl_pais) 

        for (pais, code_linepl), suma in suma_linepl_pais.items():
            if suma > 0: ### ver si es esto > 0: 
                # Realizo la busqueda de cuentas
                recovery_account = self.env['account.account'].with_company(self.env.company.id).search([
                    ('tipo_cuenta', '=', 'recupero'),
                    ('aa_linepl.code', '=', code_linepl),
                    ('pais', '=', pais),
                ], limit=1)
                _logger.info('recovery_account: %s', recovery_account) 
                
                if recovery_account:
                    val = {
                        'account_id': recovery_account.id,
                        'currency_id': self.company_id.currency_id.id,
                        'credit': round(suma, 2), ## antes debit
                        'amount_currency': round(suma, 2),
                    }
                    lines.append((0, 0, val))

        _logger.info('suma_linepl_pais: %s, linepl: %s, pais: %s', suma_linepl_pais[(pais, code_linepl)], code_linepl, pais)

        

        # if suma_cuentas > 0:
        #     val = {'account_id': recovery_account.id,
        #         'currency_id': self.company_id.currency_id.id,
        #         'debit': round(suma_cuentas, 2),
        #         'amount_currency': round(suma_cuentas, 2),
        #     }
        #     lines.append((0, 0, val))

            
        #CUENTAS
        cta_acobrar_ic_mex = self.env['account.account'].search([('code', '=', CODCTA_IC_MEX)])
        cta_acobrar_ic_usa = self.env['account.account'].search([('code', '=', CODCTA_IC_USA)])
        cta_acobrar_ic_arg = self.env['account.account'].search([('code', '=', CODCTA_IC_ARG)])

        ## COMPANY
        company_id_arg = self.env['res.company'].search([('id', '=', '1')], limit=1) 
        company_id_mex = self.env['res.company'].search([('id', '=', '2')], limit=1)
        company_id_usa = self.env['res.company'].search([('id', '=', '3')], limit=1)

        ## Diarios
        pdiario_ic_arg = (self.env['ir.config_parameter'].get_param('diario-' + str(company_id_arg.id)))
        pdiario_ic_mex = (self.env['ir.config_parameter'].get_param('diario-' + str(company_id_mex.id)))
        pdiario_ic_usa = (self.env['ir.config_parameter'].get_param('diario-' + str(company_id_usa.id)))

        # ## Parametros contra-asiento
        # CODCTA_IC_USA_CA = self.env['ir.config_parameter'].get_param('codcta_ic_usa-' + str(self.env.company.id.id), '')
        # CODCTA_IC_MEX_CA = self.env['ir.config_parameter'].get_param('codcta_ic_mex-' + str(self.env.company.id.id), '')
        # CODCTA_IC_ARG_CA = self.env['ir.config_parameter'].get_param('codcta_ic_arg-' + str(self.env.company.id.id), '')
        # ##TODO ver las cuentas a pagar para cada pais
        # cta_apagar_ic_mex = self.env['account.account'].with_company(company_id_mex.id).search([('code', '=', CODCTA_IC_MEX_CA)])
        # cta_apagar_ic_usa = self.env['account.account'].with_company(self.env.company.id).search([('code', '=', CODCTA_IC_USA_CA)])
        # cta_apagar_ic_arg = self.env['account.account'].with_company(self.env.company.id).search([('code', '=', CODCTA_IC_ARG_CA)])
        

        ## Debito *antes Credito
        ## cuentas a cobrar ic por pais y depende la compania, 1=ARG / 2=MEX / 3=USA
        if self.env.company.id == 1:
            cta_acobrar_ic = {'MEX': cta_acobrar_ic_mex.id,
                            'USA': cta_acobrar_ic_usa.id,

                                }
            ## MEX
            CODCTA_IC_ARG_CA = self.env['ir.config_parameter'].get_param('codcta_ic_arg-' + str(company_id_mex.id), '')
            cta_apagar_ic_mex = self.env['account.account'].with_company(company_id_mex.id).search([('code', '=', CODCTA_IC_ARG_CA)])
            ## USA
            CODCTA_IC_USA_CA = self.env['ir.config_parameter'].get_param('codcta_ic_arg-' + str(company_id_usa.id), '')
            cta_apagar_ic_usa = self.env['account.account'].with_company(company_id_usa.id).search([('code', '=', CODCTA_IC_USA_CA)])

            cta_apagar_ic = {'MEX': cta_apagar_ic_mex.id,
                            'USA': cta_apagar_ic_usa.id,
                            
                                }
            currency_ic = {'MEX': 'MXN',
                            'USA': 'USD',
                                                        
                                }
            company_ic = {'MEX': company_id_mex,
                            'USA': company_id_usa,
                                                        
                                }
            diario_ic = {'MEX': pdiario_ic_mex,
                        'USA': pdiario_ic_usa,
                                                   
                                }
        elif self.env.company.id == 2:
            cta_acobrar_ic = {
                            'USA': cta_acobrar_ic_usa.id,
                            'ARG': cta_acobrar_ic_arg.id,
                                }
            ## ARG
            CODCTA_IC_ARG_CA = self.env['ir.config_parameter'].get_param('codcta_ic_mex-' + str(company_id_arg.id), '')
            cta_apagar_ic_arg = self.env['account.account'].with_company(company_id_arg.id).search([('code', '=', CODCTA_IC_ARG_CA)])
            ## USA
            CODCTA_IC_USA_CA = self.env['ir.config_parameter'].get_param('codcta_ic_mex-' + str(company_id_usa.id), '')
            cta_apagar_ic_usa = self.env['account.account'].with_company(company_id_usa.id).search([('code', '=', CODCTA_IC_USA_CA)])

            cta_apagar_ic = {
                            'USA': cta_apagar_ic_usa.id,
                            'ARG': cta_apagar_ic_arg.id,
                                }
            currency_ic = {
                            'USA': 'USD',
                            'ARG' : 'ARS',                            
                                }
            company_ic = {
                            'USA': company_id_usa,
                            'ARG' : company_id_arg,                            
                                }
            diario_ic = {
                        'USA': pdiario_ic_usa,
                        'ARG': pdiario_ic_arg,                           
                                }
        elif self.env.company.id == 3:
            cta_acobrar_ic = {'MEX': cta_acobrar_ic_mex.id,
                            
                            'ARG': cta_acobrar_ic_arg.id,
                                }
             ## ARG
            CODCTA_IC_ARG_CA = self.env['ir.config_parameter'].get_param('codcta_ic_usa-' + str(company_id_arg.id), '')
            cta_apagar_ic_arg = self.env['account.account'].with_company(company_id_arg.id).search([('code', '=', CODCTA_IC_ARG_CA)])
            ## MEX
            CODCTA_IC_USA_CA = self.env['ir.config_parameter'].get_param('codcta_ic_usa-' + str(company_id_mex.id), '')
            cta_apagar_ic_mex = self.env['account.account'].with_company(company_id_mex.id).search([('code', '=', CODCTA_IC_USA_CA)])

            cta_apagar_ic = {'MEX': cta_apagar_ic_mex.id,
                            
                            'ARG': cta_apagar_ic_arg.id,
                                }
            currency_ic = {'MEX': 'MXN',
                            
                            'ARG' : 'ARS',                            
                                }
            company_ic = {'MEX': company_id_mex,

                            'ARG' : company_id_arg,                            
                                }
            diario_ic = {'MEX': pdiario_ic_mex,
                        
                        'ARG': pdiario_ic_arg,                           
                                }

        lines_ctas_apagar = {}
        for pais, total in total_por_pais.items():            
            if total > 0 and pais in cta_acobrar_ic:
                val = {'account_id': cta_acobrar_ic[pais], 
                    'currency_id': self.company_id.currency_id.id,
                    'debit': round(total_por_pais[pais], 2), # antes credit
                    'amount_currency': round(total_por_pais[pais] * -1, 2),
                }
                lines.append((0, 0, val))   

                #### CONTRA ASIENTO ###########
            if total > 0 and pais in cta_apagar_ic:
                currency = self.env['res.currency'].with_company(self.env.company.id).search([('name', '=', currency_ic[pais])], limit=1)
                exchange_rate = currency.rate
                amount_total = total_por_pais[pais] * exchange_rate

                val_credit = {'account_id': cta_apagar_ic[pais], 
                    'currency_id': company_ic[pais].currency_id.id,
                    'credit': round(amount_total, 2), 
                    'amount_currency': round(amount_total * -1, 2),
                }
                val_debit = {'account_id': cta_apagar_ic[pais], 
                    'currency_id': company_ic[pais].currency_id.id,
                    'debit': round(amount_total, 2),
                    'amount_currency': round(amount_total, 2),
                }
            # # if  total > 0 and pais == 'USA':
            # #     currency = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
            # #     exchange_rate = currency.rate
            # #     amount_total = total_por_pais[pais] * exchange_rate

            # #     val_credit = {'account_id': cta_apagar_ic[pais], 
            # #         'currency_id': company_id_arg.currency_id.id,
            # #         'credit': round(amount_total, 2), 
            # #         'amount_currency': round(amount_total, 2),
            # #     }
            # #     val_debit = {'account_id': cta_apagar_ic[pais], 
            # #         'currency_id': company_id_mex.currency_id.id,
            # #         'debit': round(amount_total, 2),
            # #         'amount_currency': round(amount_total * -1, 2),
            # #     }
            # # if  total > 0 and pais == 'ARG':
            # #     currency = self.env['res.currency'].search([('name', '=', 'ARS')], limit=1)
            # #     exchange_rate = currency.rate
            # #     amount_total = total_por_pais[pais] * exchange_rate

            # #     val_credit = {'account_id': cta_apagar_ic[pais], 
            # #         'currency_id': company_id_arg.currency_id.id,
            # #         'credit': round(amount_total, 2), 
            # #         'amount_currency': round(amount_total, 2),
            # #     }
            # #     val_debit = {'account_id': cta_apagar_ic[pais], 
            # #         'currency_id': company_id_arg.currency_id.id,
            # #         'debit': round(amount_total, 2),
            # #         'amount_currency': round(amount_total * -1, 2),
            # #     }
            

                _logger.info('------cta_acobrar_ic---pais: %s', cta_acobrar_ic[pais])  
                _logger.info('-------pais------: %s', pais)  

                # Verifica si el país ya existe en el diccionario
                if pais in lines_ctas_apagar:
                    lines_ctas_apagar[pais].append((0, 0, val_credit))
                    lines_ctas_apagar[pais].append((0, 0, val_debit))
                else:
                    lines_ctas_apagar[pais] = [(0, 0, val_credit), (0, 0, val_debit)]  
                    # lines_ctas_apagar[pais] = [(0, 0, val_debit)] 

        for pais, lineas in lines_ctas_apagar.items():
            if pais in company_ic:
                company = company_ic[pais]
                DIARIO_IC = int(diario_ic[pais])
                _logger.info('-------DIARIO_IC------: %s', DIARIO_IC)
                _logger.info('-------company------: %s', company)  
                currency_id = company.currency_id.id
                move = self.env['account.move'].with_company(company.id).create({
                    'journal_id': DIARIO_IC,
                    'currency_id': currency_id,
                    'line_ids': lineas,
                })
                
            # if pais == 'MEX':
            #     _logger.info('------company_id_mex---------: %s', company_id_mex)  
            #     move = self.env['account.move'].with_company(company_id_mex.id).create({
            #         'journal_id': DIARIO, 
            #         'currency_id': company_id_mex.currency_id.id, 
            #         'line_ids': lines,
            #     })

            # elif pais == 'USA':
            #     _logger.info('------company_id_usa---------: %s', company_id_usa)
            #     move = self.env['account.move'].with_company(company_id_usa.id).create({
            #         'journal_id': DIARIO, 
            #         'currency_id': company_id_usa.currency_id.id, 
            #         'line_ids': lines,
            #     })
            # elif pais == 'ARG':
            #     _logger.info('------company_id_arg---------: %s', company_id_arg)
            #     move = self.env['account.move'].with_company(company_id_arg.id).create({
            #         'journal_id': DIARIO, 
            #         'currency_id': company_id_arg.currency_id.id, 
            #         'line_ids': lines,
            #     })

        _logger.info('lines: %s', lines)

        

        if lines:
            move = self.env['account.move'].with_company(self.env.company.id).create({'journal_id': DIARIO, 
                                                    'currency_id': self.company_id.currency_id.id, 
                                                    'line_ids': lines
                                                    })
            move.action_post()

        # publico
        self.state = 'post'




class ResultadosRecuperoPais(models.Model):
    _name = 'recupero.pais'

    code_linepl = fields.Char(string='Código de P&L')
    code_uniope = fields.Char(string='Código de Unidad Operativa')
    valor_pais_recupero = fields.Float(string='Valor de Recupero')
    pais = fields.Char(string='Pais')
    resultados_interco_id = fields.Many2one(
        'resultados.interco',
        string='Resultado Interco',
    )     
       