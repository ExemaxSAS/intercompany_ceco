# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging, math

from collections import defaultdict
_logger = logging.getLogger(__name__)

HORAS_SUELDO=160
COSTOS_INDIRECTOS=3
COSTOS_DIRECTOS=5
DIARIO= 67 #sueldos y jornales
CUENTA_SUELDOS_APAGAR = 116

class IntercompanyCostGroups(models.Model):
    _name = 'intercompany.cost.groups'
    _description = 'Grupos costos'

    name=fields.Char('Nombre', required=True)

class IntercompanyCostSubGroups(models.Model):
    _name = 'intercompany.cost.subgroups'
    _description = 'Sugrupos costos'

    name=fields.Char('Nombre', required=True)
    grupo_id= fields.Many2one('intercompany.cost.groups',string='Grupo padre', required=True)

class IntercompanyCostLine(models.Model):
    _name = 'intercompany.cost.line'
    _description = 'Detalle costo entre empresas'

    account_itc_id = fields.Many2one('account.intercompany.cost', string='account intercompany cost')
    date_from = fields.Date('Fecha desde', required=True)
    date_to = fields.Date('Fecha hasta', required=True)
    hr_employee_id= fields.Many2one('hr.employee','Empleado',required=True)
    account_id =  fields.Many2one('account.analytic.account','Centro de costo')
    area_uniope = fields.Char(string="Area/Unidad Operativa")
    area = fields.Integer('id Area',store=True)
    unidad_operativa = fields.Integer('Unidad Operativa',store=True)
    costo_sueldo = fields.Float('Costo Sueldo',digits=(12,2))
    costo_contribuciones = fields.Float('Costo Contribuciones',digits=(12,2))
    tipo= fields.Char(string="Tipo de Costo")
    es_freelance= fields.Boolean('Es freelance',store=True)

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
    intercompany_cost_line = fields.One2many('intercompany.cost.line', 'account_itc_id', string='Intercompany Cost Lines',
                                 copy=True,auto_join=True)
    @api.depends('date_from', 'date_to')
    def _compute_analytic_line(self):
        aline_ids = self.env['account.analytic.line'].search([('employee_id','!=',False),('date','>=', self.date_from),('date','<=', self.date_to)])
        self.analytic_line_ids = aline_ids

    def prepost_intercompany_cost(self):

        #borro datos existentes si no est está publicado

        lines_unlink = self.env['intercompany.cost.line'].search([('account_itc_id','=', self.id)])
#        _logger.info('Borro' +  str(lines_unlink))
        lines_unlink.unlink()
        # busco empleados
        result = self.env['account.analytic.line'].read_group(
            [('employee_id', '!=', False), ('date', '>=', self.date_from), ('date', '<=', self.date_to)],
            fields=['employee_id', 'unit_amount'],
            groupby=['employee_id'])

        for employee in result:

            horas_total_empleado=employee.get('unit_amount')
            #filtro porque agrupado trae en cero registros fuera de domain
            if horas_total_empleado>0:
                #este total horas se podria usar para el % por proyecto en el mes0
                #busco datos por empleado y luego calculo
                id_empleado= employee.get('employee_id')[0]
                empleado= self.env['hr.employee'].search([('id', '=', id_empleado)])
                area=empleado.department_id.id
                unidad_operativa=empleado.uni_oper.id
                area_uniope= empleado.area_uniope

                _logger.info(
                    'empleado:' + str(employee.get('employee_id')[0]) + ' Horas totales:' + str(horas_total_empleado))
                _logger.info(
                    'AREA unidad oper:' + str(area) + '-' + str(unidad_operativa))
                es_freelance = False
                valores_sueldo_empleado = self.env['employee.cost.hour.line'].search([('hr_employee_id', '=', id_empleado),
                                                                                      (
                                                                                      'hr_cost_date', '>=', self.date_from),
                                                                                      ('hr_cost_date', '<=', self.date_to)])
                #******* inicializo**********
                valor_sueldo = 0
                valor_contribucion = 0
                sueldo_cuenta = 0
                contribuciones_cuenta = 0
                id_cuenta = ''
                tipo_costo=''

                # ******* ---------**********
                if valores_sueldo_empleado:
                    if len(valores_sueldo_empleado) > 1:
                        #raro que se dé, igual controlo para evitar error en la asignacion
                        _logger.info('empleado con mas de un valor sueldo:' + str(id_empleado))
                    else:
                        es_freelance = not(valores_sueldo_empleado.hr_employee_es_rd)
                        valor_sueldo = valores_sueldo_empleado.hr_sueldo_facturado
                        valor_contribucion = valores_sueldo_empleado.hr_contribuciones
                else:
                    # busco el menor valor mas proximo
                    valores_sueldo_empleado = self.env['employee.cost.hour.line'].search([('hr_employee_id', '=', id_empleado),
                                                                                          ('hr_cost_date', '<=',
                                                                                           self.date_to)],
                                                                                         order='hr_cost_date desc')
                    if valores_sueldo_empleado:
                        valor_sueldo = valores_sueldo_empleado[0].hr_sueldo_facturado
                        valor_contribucion = valores_sueldo_empleado[0].hr_contribuciones
                    else:
                        _logger.info('empleado '  + str(id_empleado)+ ' no registra valor sueldo')
                        # raise UserError(_("No se encontró valor suelde para  empleado" ))

                valor_hora_sueldo = valor_sueldo / HORAS_SUELDO
                valor_hora_contribucion = valor_contribucion / HORAS_SUELDO

                _logger.info('--- valor sueldo:' + str(
                    valor_sueldo) + ' valor contribucion:' + str(valor_contribucion))

                #CALCULO sueldo . primero agrupo cuentas directas
                total_employee_directas = self.env['account.analytic.line'].read_group(
                    [('employee_id', '=', id_empleado), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
                     ('group_id', '=', COSTOS_DIRECTOS)],
                    fields=['unit_amount','group_id'],
                    groupby=['group_id'])
                _logger.info('DIRECTAS:' + str(total_employee_directas))

                for tot_directas in total_employee_directas:
                    if len(tot_directas)>0:
                        total_hrs_directas=tot_directas.get('unit_amount')
                        result_employee = self.env['account.analytic.line'].read_group(
                            [('employee_id', '=', id_empleado), ('date', '>=', self.date_from), ('date', '<=', self.date_to),('group_id','=',COSTOS_DIRECTOS)],
                            fields=['account_id', 'unit_amount'],
                            groupby=['account_id'])
                        _logger.info('CUENTAS:' + str(result_employee))
                        for cuenta  in result_employee:
                            tipo_costo='directos'

                            id_cuenta = cuenta.get('account_id')[0]
                            horas_trabajadas = cuenta.get('unit_amount')
                            horas_indirectas=0
                            #if (horas_trabajadas<=HORAS_SUELDO):
                            if (total_hrs_directas<=HORAS_SUELDO):
                                horas_cuenta= horas_trabajadas
                                horas_indirectas = HORAS_SUELDO - horas_trabajadas
                            else:
                                horas_cuenta = HORAS_SUELDO
                            porcentaje_cuenta=  horas_trabajadas * 100 / total_hrs_directas
                            sueldo_cuenta= valor_hora_sueldo * horas_cuenta * porcentaje_cuenta/100
                            _logger.info('directa :' + str(horas_cuenta) + '-' + str(horas_indirectas) + '-' + str(porcentaje_cuenta)  )

                            if not(es_freelance):
                                contribuciones_cuenta = valor_hora_contribucion * horas_cuenta * porcentaje_cuenta/100
                            vals ={
                                    'account_itc_id': self.id,
                                    'date_from': self.date_from,
                                    'date_to': self.date_to,
                                    'hr_employee_id':id_empleado,
                                    'account_id':id_cuenta,
                                    'area_uniope':area_uniope,
                                    'area':area,
                                    'unidad_operativa':unidad_operativa,
                                    'costo_sueldo':sueldo_cuenta,
                                    'costo_contribuciones':contribuciones_cuenta,
                                    'tipo':tipo_costo,
                                    'es_freelance' :es_freelance,
                                }
                            self.env['intercompany.cost.line'].create(vals)
                            #***********  si corresponde indirectas , busco costos indirectos********
                            if horas_indirectas>0:
                                # busco total de cuentas indirectas del empleado
                                request = "SELECT  SUM(unit_amount) as total_employee_indirectas FROM account_analytic_line " \
                                          " WHERE group_id="+ str(COSTOS_INDIRECTOS) +" and employee_id ="+ str(id_empleado)+\
                                          " and date >='" +  str(self.date_from) + "' and date<='"+  str(self.date_to) + "'  GROUP BY group_id"
                                self.env.cr.execute(request)
                                for record in self.env.cr.dictfetchall():
                                    if record['total_employee_indirectas']>0:
                                        total_hrs_indirectas = record['total_employee_indirectas']
                                        #f total_hrs_indirectas> horas_indirectas:
                                        #   total_hrs_indirectas=horas_indirectas

                                        result_employee = self.env['account.analytic.line'].read_group(
                                            [('employee_id', '=', id_empleado), ('date', '>=', self.date_from),
                                             ('date', '<=', self.date_to), ('group_id', '=', COSTOS_INDIRECTOS)],
                                            fields=['account_id', 'unit_amount'],
                                            groupby=['account_id'])
                                        for cuenta in result_employee:
                                            id_cuenta = cuenta.get('account_id')[0]
                                            horas_trabajadas = cuenta.get('unit_amount')
                                            tipo_costo = 'indirectos'
                                            porcentaje_cuenta = horas_trabajadas * 100 / total_hrs_indirectas
                                            sueldo_cuenta = valor_hora_sueldo * horas_indirectas * porcentaje_cuenta / 100

                                            if not (es_freelance):
                                                contribuciones_cuenta = valor_hora_contribucion * horas_indirectas * porcentaje_cuenta / 100
                                            vals = {
                                                'account_itc_id': self.id,
                                                'date_from': self.date_from,
                                                'date_to': self.date_to,
                                                'hr_employee_id': id_empleado,
                                                'account_id': id_cuenta,
                                                'area_uniope': area_uniope,
                                                'area': area,
                                                'unidad_operativa': unidad_operativa,
                                                'costo_sueldo': sueldo_cuenta,
                                                'costo_contribuciones': contribuciones_cuenta,
                                                'tipo': tipo_costo,
                                                'es_freelance': es_freelance,
                                            }
                                            self.env['intercompany.cost.line'].create(vals)

    def post_intercompany_cost(self):
        #agrupo por area y cuenta para crear el asiento
        lines = [(5, 0, 0)]
        request= "SELECT  SUM(costo_sueldo) as sum_costosueldo,SUM(costo_contribuciones) as sum_costo_contribuciones,  area, unidad_operativa, account_id, es_freelance " \
                 " FROM intercompany_cost_line  WHERE account_itc_id =" + str(self.id) + "GROUP BY area, unidad_operativa, account_id, es_freelance" \

        self.env.cr.execute(request)
        monto_total = 0

        for record in self.env.cr.dictfetchall():
            area = record['area']
            analytic_account_id = record['account_id']
            unidad_operativa = record['unidad_operativa']
            cuenta_sueldo = self.env['account.account'].search(
                [('area', '=', area), ('unidad_operativa', '=', unidad_operativa),('tipo_cuenta','=','sueldo')], limit=1)
            cuenta_honorarios = self.env['account.account'].search(
                [('area', '=', area), ('unidad_operativa', '=', unidad_operativa), ('tipo_cuenta', '=', 'honorarios')],
                limit=1)
            _logger.info(
                'MOV : analytica' + str(analytic_account_id) + '- Cuenta' + str(cuenta_sueldo))
            # lo limito a uno para evitar errores, de todos modos el constraint deberia evitarlo
            monto= round(record['sum_costosueldo'],2)
            freelance= record['es_freelance']
            #--------------- SUELDO EMPLEADO------------------#
            if cuenta_sueldo and (monto>0) and not(freelance):
                #genero linea
                monto_total += monto
                val = {'account_id':cuenta_sueldo.id,
                          'analytic_account_id':analytic_account_id  ,
                          'currency_id':19,
                          'debit':monto,
                          'amount_currency':monto}
                lines.append((0,0 , val))

            # --------------- HONORARIOS FREELANCE ------------------#
            if cuenta_honorarios and (monto > 0) and freelance:
                    # genero linea
                    monto_total += monto
                    val = {'account_id': cuenta_honorarios.id,
                           'analytic_account_id': analytic_account_id,
                           'currency_id': 19,
                           'debit': monto,
                           'amount_currency': monto}
                    lines.append((0, 0, val))

            #"________CONTRIBUCIONES------"
            monto = round(record['sum_costo_contribuciones'],2)
            cuenta_contribucion = self.env['account.account'].search(
                [('area', '=', area), ('unidad_operativa', '=', unidad_operativa),('tipo_cuenta','=','contribucion')], limit=1)
            _logger.info(
                'MOV : analitica' + str(analytic_account_id) + '- Cuenta' + str(cuenta_contribucion))

            if cuenta_contribucion and (monto > 0):
                # genero linea
                monto_total += monto
                val = {'account_id': cuenta_contribucion.id,
                       'analytic_account_id': analytic_account_id,
                       'currency_id': 19,
                       'debit': monto,
                       'amount_currency': monto}
                lines.append((0, 0, val))
        #END FOR
        if monto_total>0:
            _logger.info('MONTO TOTAL' + str(monto_total))
            val={'account_id': CUENTA_SUELDOS_APAGAR,
                'currency_id': 19,
                'credit': monto_total,
                'amount_currency': monto_total * -1,
            }
            lines.append((0, 0, val))
            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': 19,'line_ids':lines })
            move.action_post()

            #publico
            #self.state='post'
