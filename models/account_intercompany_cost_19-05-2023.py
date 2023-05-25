# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging, math

from collections import defaultdict
_logger = logging.getLogger(__name__)

HORAS_SUELDO=160

class IntercompanyCostGroups(models.Model):
    _name = 'intercompany.cost.groups'
    _description = 'Grupos costos'
    
    # company_id
    company_id = fields.Many2one('res.company', string='Compañia')

    @api.model
    def create(self, vals):
        if 'company_id' not in vals:
            # vals['company_id'] = self.env.user.company_id.id
            vals['company_id'] = self.env.company.id
        return super(IntercompanyCostGroups, self).create(vals)
    #
    
    name=fields.Char('Nombre', required=True)
    subgrupos=fields.One2many('intercompany.cost.subgroups','grupo_id', string='Subgrupo',copy=True, auto_join=True)
    ctas_comunes = fields.One2many('intercompany.cost.ctascomunes', 'grupo_id', string='Ctas comunes', copy=True, auto_join=True)
    #pais = fields.Selection([('MEX','MEX'),('USA','USA'),('ARG','ARG'),('','')],'Pais para COM-LEADS')
    # tomo pais directo de la cuenta
    
    
class IntercompanyCostSubGroups(models.Model):
    _name = 'intercompany.cost.subgroups'
    _description = 'Sugrupos costos'

    # company_id
    company_id = fields.Many2one('res.company', string='Compañia')

    @api.model
    def create(self, vals):
        if 'company_id' not in vals:
            # vals['company_id'] = self.env.user.company_id.id
            vals['company_id'] = self.env.company.id
        return super(IntercompanyCostSubGroups, self).create(vals)
    #
    
    name=fields.Char('Nombre', required=True)
    grupo_id= fields.Many2one('intercompany.cost.groups',string='Grupo padre', required=True)
    distribucion_costo = fields.Selection([
        ('B1', 'B1'),
        ('NT', 'NT'),
        ('MKT', 'MKT'),
        ('S4', 'S4'),
        ('TUSA', 'TALENT USA'),
        ('TLATAM', 'TALENT LATAM'),
    ], 'Distribución de costo',)



class IntercompanyCostCtasComunes(models.Model):
    _name = 'intercompany.cost.ctascomunes'
    _description = 'Cuentas comunes'
    
    # company_id
    company_id = fields.Many2one('res.company', string='Compañia')

    @api.model
    def create(self, vals):
        if 'company_id' not in vals:
           # vals['company_id'] = self.env.user.company_id.id
            vals['company_id'] = self.env.company.id
        return super(IntercompanyCostCtasComunes, self).create(vals)
    #

    grupo_id= fields.Many2one('intercompany.cost.groups',string='Grupo padre', required=True)
    centro_costos = fields.Many2one('account.analytic.account', string='Centro de Costos',required=True)
    account_id = fields.Many2one('account.account',string='Cuenta Contable')
    distribucion_costo = fields.Selection([
        ('B1', 'B1'),
        ('NT', 'NT'),
        ('MKT', 'MKT'),
        ('S4', 'S4'),
        ('TUSA', 'TALENT USA'),
        ('TLATAM', 'TALENT LATAM'),
    ], 'Distribución de costo',)

class IntercompanyCostLine(models.Model):
    _name = 'intercompany.cost.line'
    _description = 'Detalle costo entre empresas'

    # company_id
    company_id = fields.Many2one('res.company', string='Compañia')

    @api.model
    def create(self, vals):
        if 'company_id' not in vals:
            # vals['company_id'] = self.env.user.company_id.id
            vals['company_id'] = self.env.company.id
        return super(IntercompanyCostLine, self).create(vals)
    #

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
    costo_honorario = fields.Float('Costo Honorario',digits=(12,2))
    tipo= fields.Char(string="Tipo de Costo")
    #es_freelance= fields.Boolean('Es freelance',store=True)
    cuenta_sueldo = fields.Char('Cta.Sueldo')
    cuenta_contribucion = fields.Char('Cta.Contribucion')
    cuenta_honorario = fields.Char('Cta.Honorario')


class AccountIntercompanyCost(models.Model):
    _name = 'account.intercompany.cost'
    _description = 'Costo entre empresas'

    # company_id
    company_id = fields.Many2one('res.company', string='Compañia', default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        if 'company_id' not in vals:
            # vals['company_id'] = self.env.user.company_id.id
            vals['company_id'] = self.env.company.id
        return super(AccountIntercompanyCost, self).create(vals)
    #

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('checkpoint', 'Checkpoint'),
        ('post', 'Publicado')
    ], 'Estado', default = 'draft')
    name = fields.Char('Nombre', required=True)
    date_from = fields.Date('Fecha desde', required=True)
    date_to = fields.Date('Fecha hasta', required=True)
    responsible_user = fields.Many2one('res.users','Responsable', required=True)
    analytic_line_ids = fields.Many2many('account.analytic.line', 'Cuentas analíticas', compute='_compute_analytic_line')
    intercompany_cost_line = fields.One2many('intercompany.cost.line', 'account_itc_id', string='Intercompany Cost Lines',
                                 copy=True,auto_join=True)
    comentarios = fields.Text('Datos a verificar')

    # _sql_constraints = [('unique_icperiodo', 'unique(date_from, date_to)',
    #                      'Ya existe un periodo cargado con iguales fechas desde-hasta')]
    

    @api.depends('date_from', 'date_to')
    def _compute_analytic_line(self):
        # if company o se lo asigno aca.
        aline_ids = self.env['account.analytic.line'].search([('employee_id','!=',False),('date','>=', self.date_from),('date','<=', self.date_to), ('company_id', '=', self.company_id.id)])
        self.analytic_line_ids = aline_ids
        _logger.info('aline_ids:' + str(aline_ids) )

    def prepost_intercompany_cost(self):

        COSTOS_INDIRECTOS = int(self.env['ir.config_parameter'].get_param('idcostos_indirectos-' + str(self.company_id.id), ''))
        COSTOS_DIRECTOS = int(self.env['ir.config_parameter'].get_param('idcostos_directos-' + str(self.company_id.id), ''))
        _logger.info('costos directos:' + str(COSTOS_DIRECTOS) )
        _logger.info('costos indirectos:' + str(COSTOS_INDIRECTOS))
        #borro datos existentes si no est está publicado
        lines_unlink = self.env['intercompany.cost.line'].search([('account_itc_id','=', self.id)])
        _logger.info('Borro' +  str(lines_unlink))
        lines_unlink.unlink()
        #busco proyectos que no estén diferenciados en directos/indirectos
        self.comentarios=''
        request_ctrl = "SELECT distinct(account.id), account.name as name  FROM account_analytic_line as acc_line INNER JOIN account_analytic_account as account on account.id=acc_line.account_id " \
                  " WHERE account.group_id is null and acc_line.date >='" + str(self.date_from) + "' and acc_line.date<='" + str(self.date_to) +"' and account.company_id='" + str(self.company_id.id) +"' "
        self.env.cr.execute(request_ctrl)

        _logger.info('ctas sin costo:' + request_ctrl)
        for record in self.env.cr.dictfetchall():
                self.comentarios += "Cuenta analitica sin definir como directo/indirecto: " + str(record['name']) +".\n"
        # busco empleados
        result = self.env['account.analytic.line'].read_group(
            [('employee_id', '!=', False), ('date', '>=', self.date_from), ('date', '<=', self.date_to), ('company_id', '=', self.company_id.id)],
            fields=['employee_id', 'unit_amount'],
            groupby=['employee_id'])
        _logger.info('AAAAAAAAAAAAAAA:' + str(result) )

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
                honorario_cuenta = 0
                id_cuenta = ''
                tipo_costo=''
                valor_honorario = 0

                # ******* ---------**********
                if valores_sueldo_empleado:
                    if len(valores_sueldo_empleado) > 1:
                        #raro que se dé, igual controlo para evitar error en la asignacion
                        _logger.info('empleado con mas de un valor sueldo:' + str(id_empleado))
                        self.comentarios+= 'El empleado '  + empleado.name + ' registra mas de un valor. (Sueldos-Contribuciones-Honorarios) \n'
                        
                    else:
                        # es_freelance = not(valores_sueldo_empleado.hr_employee_es_rd)
                        valor_sueldo = valores_sueldo_empleado.hr_sueldo_facturado
                        valor_contribucion = valores_sueldo_empleado.hr_contribuciones
                        valor_honorario = valores_sueldo_empleado.hr_honorario
                else:
                    # busco el menor valor mas proximo
                    valores_sueldo_empleado = self.env['employee.cost.hour.line'].search([('hr_employee_id', '=', id_empleado),
                                                                                          ('hr_cost_date', '<=',
                                                                                           self.date_to)],
                                                                                         order='hr_cost_date desc')
                    if valores_sueldo_empleado:                        
                      #  es_freelance = not (valores_sueldo_empleado[0].hr_employee_es_rd)
                        valor_sueldo = valores_sueldo_empleado[0].hr_sueldo_facturado
                        valor_contribucion = valores_sueldo_empleado[0].hr_contribuciones
                        valor_honorario = valores_sueldo_empleado[0].hr_honorario
                    else:
                        self.comentarios+= 'El empleado '  + empleado.name + ' no registra valor sueldo. \n'
                _logger.info('empleado '  + str(id_empleado)+ ' freelance'  )
                        # raise UserError(_("No se encontró valor suelde para  empleado" ))

                valor_hora_sueldo = valor_sueldo / HORAS_SUELDO
                valor_hora_contribucion = valor_contribucion / HORAS_SUELDO
                valor_hora_honorario = valor_honorario / HORAS_SUELDO


                _logger.info('--- valor sueldo:' + str(
                    valor_sueldo) + ' valor contribucion:' + str(valor_contribucion))

                #CALCULO sueldo . primero agrupo cuentas directas
                _logger.info('id_empleado:' + str(id_empleado))
                _logger.info('self.date_from:' + str(self.date_from))
                _logger.info('self.date_to:' + str(self.date_to))
                _logger.info('self.company_id.id:' + str(self.company_id.id))
                _logger.info('COSTOS_DIRECTOS:' + str(COSTOS_DIRECTOS))
                total_employee_directas = self.env['account.analytic.line'].sudo().read_group(
                    [('employee_id', '=', id_empleado), ('date', '>=', self.date_from), ('date', '<=', self.date_to), ('company_id', '=', self.company_id.id), 
                     ('group_id', '=', COSTOS_DIRECTOS)],
                    fields=['unit_amount','group_id'],
                    groupby=['group_id'])
                _logger.info('DIRECTAS:' + str(total_employee_directas))
                # return
                #if len(total_employee_directas) > 0:
                #    _logger.info('DIRECTAS:' + str(total_employee_directas))
                #inicializo indirectas por si no trabaja directas
                horas_indirectas = HORAS_SUELDO

                #
                for tot_directas in total_employee_directas:   
                    _logger.info('BBBBBBBentro al for:')                
                    if len(tot_directas)>0:
                        total_hrs_directas=tot_directas.get('unit_amount')
                        result_employee = self.env['account.analytic.line'].read_group(
                            [('employee_id', '=', id_empleado), ('date', '>=', self.date_from), ('date', '<=', self.date_to), ('company_id', '=', self.company_id.id),('group_id','=',COSTOS_DIRECTOS)],
                            fields=['account_id', 'unit_amount'],
                            groupby=['account_id'])
                        _logger.info('CUENTAS:' + str(result_employee))
                        for cuenta  in result_employee:
                            tipo_costo='directos'

                            id_cuenta = cuenta.get('account_id')[0]
                            horas_trabajadas = cuenta.get('unit_amount')
                            if (total_hrs_directas<=HORAS_SUELDO):
                                _logger.info('total_hrs_directas<=HORAS_SUELDO')
                                if (horas_total_empleado<=total_hrs_directas):
                                    _logger.info('horas_total_empleado<=total_hrs_directas')
                                    #solo trabajó directas
                                    #horas_cuenta = HORAS_SUELDO
                                    horas_cuenta = horas_trabajadas
                                    horas_indirectas = HORAS_SUELDO - total_hrs_directas
                                else:
                                    _logger.info('else')
                                    horas_cuenta= horas_trabajadas
                                   # horas_indirectas = HORAS_SUELDO - horas_trabajadas
                                    horas_indirectas = HORAS_SUELDO - total_hrs_directas
                            else:
                                horas_cuenta = HORAS_SUELDO
                            if total_hrs_directas>0:
                                porcentaje_cuenta=  horas_trabajadas * 100 / total_hrs_directas
                            else:
                                porcentaje_cuenta=0

                            _logger.info('valor_sueldo ' + str(valor_sueldo))
                            _logger.info('HORAS_SUELDO ' + str(HORAS_SUELDO))
                            _logger.info('horas_cuenta ' + str(horas_cuenta))
                            sueldo_cuenta = (valor_sueldo / HORAS_SUELDO) * horas_cuenta
                            #sueldo_cuenta = valor_hora_sueldo * horas_cuenta * porcentaje_cuenta / 100
                            _logger.info('horas_trabajadas :' + str(horas_trabajadas))
                            _logger.info('total_hrs_directas :' + str(total_hrs_directas))
                            _logger.info('directa :' + str(horas_cuenta) + '-' + str(horas_indirectas) + '-' + str(porcentaje_cuenta)  )

                            cuenta_sueldo=None
                            cuenta_honorarios=None
                            cuenta_contribucion=None
                        
                            #contribuciones_cuenta = valor_hora_contribucion * horas_cuenta * porcentaje_cuenta/100
                            contribuciones_cuenta = (valor_contribucion / HORAS_SUELDO) * horas_cuenta
                            #honorario_cuenta = valor_hora_honorario * horas_cuenta * porcentaje_cuenta/100
                            honorario_cuenta = (valor_honorario / HORAS_SUELDO) * horas_cuenta

                            cta_sueldo = self.env['account.account'].search(
                                [('area', '=', area), ('unidad_operativa', '=', unidad_operativa), ('company_id', '=', self.company_id.id),
                                    ('tipo_cuenta', '=', 'sueldo')],
                                limit=1)
                            _logger.info('AAAAAAAAActa_sueldo DIR ' + str(cta_sueldo))
                            if cta_sueldo:
                                cuenta_sueldo = cta_sueldo.name
                            cta_contribucion = self.env['account.account'].search(
                                [('area', '=', area), ('unidad_operativa', '=', unidad_operativa), ('company_id', '=', self.company_id.id),
                                    ('tipo_cuenta', '=', 'contribucion')], limit=1)
                            _logger.info('AAAAAAAAActa_contribucion DIR ' + str(cta_contribucion))
                            if cta_contribucion:
                                cuenta_contribucion = cta_contribucion.name
                     
                            cta_honorarios = self.env['account.account'].search(
                                [('area', '=', area), ('unidad_operativa', '=', unidad_operativa), ('company_id', '=', self.company_id.id),
                                    ('tipo_cuenta', '=', 'honorario')], limit=1)
                            _logger.info('AAAAAAAAActa_honorarios DIR ' + str(cta_honorarios))
                            if cta_honorarios:
                                cuenta_honorarios = cta_honorarios.name
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
                                    'costo_honorario':honorario_cuenta,
                                    'tipo':tipo_costo,
                                   # 'es_freelance' :es_freelance,
                                    'cuenta_honorario' : cuenta_honorarios,
                                    'cuenta_sueldo': cuenta_sueldo,
                                    'cuenta_contribucion': cuenta_contribucion
                                }
                            self.env['intercompany.cost.line'].create(vals)
                #***********  si corresponde indirectas , busco costos indirectos********
                _logger.info(
                    'HORAS INDIRECTAS :' + str(horas_indirectas))
                if horas_indirectas>0:
                    # busco total de cuentas indirectas del empleado
                    request = "SELECT  SUM(unit_amount) as total_employee_indirectas FROM account_analytic_line " \
                              " WHERE group_id="+ str(COSTOS_INDIRECTOS) +" and employee_id ="+ str(id_empleado)+\
                              " and date >='" +  str(self.date_from) + "' and date<='"+  str(self.date_to) + "'  GROUP BY group_id"
                    self.env.cr.execute(request)

                    for record in self.env.cr.dictfetchall():
                        _logger.info(
                            'HORAS INDIRECTAS empleado:' + str(record['total_employee_indirectas']))
                        if record['total_employee_indirectas'] == 0:
                            record['total_employee_indirectas'] = horas_indirectas
                        if record['total_employee_indirectas']>0:
                            total_hrs_indirectas = horas_indirectas                           
                           # total_hrs_indirectas = record['total_employee_indirectas']
                            #if total_hrs_indirectas == 0:
                            #    total_hrs_indirectas = horas_indirectas
                            _logger.info(
                            'total_hrs_indirectas:' + str(total_hrs_indirectas))
                            result_employee = self.env['account.analytic.line'].read_group(
                                [('employee_id', '=', id_empleado), ('date', '>=', self.date_from),
                                 ('date', '<=', self.date_to), ('company_id', '=', self.company_id.id), ('group_id', '=', COSTOS_INDIRECTOS)],
                                fields=['account_id', 'unit_amount'],
                                groupby=['account_id'])
                            _logger.info(
                                'cuentas INDIRECTAS:' + str(result_employee))
                            for cuenta in result_employee:
                                id_cuenta = cuenta.get('account_id')[0]
                                horas_trabajadas = cuenta.get('unit_amount')
                                tipo_costo = 'indirectos'
                                
                                if total_hrs_indirectas>0:
                                    porcentaje_cuenta = horas_trabajadas * 100 / total_hrs_indirectas
                                else:
                                    porcentaje_cuenta=0
                                _logger.info('valor_sueldo ' + str(valor_sueldo))
                                _logger.info('HORAS_SUELDO ' + str(HORAS_SUELDO))
                                _logger.info('horas_cuenta ' + str(total_hrs_indirectas))
                                sueldo_cuenta = (valor_sueldo / HORAS_SUELDO) * total_hrs_indirectas
                                #sueldo_cuenta = valor_hora_sueldo * horas_indirectas * porcentaje_cuenta / 100
                                _logger.info('horas_trabajadas :' + str(horas_trabajadas))
                                _logger.info('total_hrs_indirectas :' + str(total_hrs_indirectas))
                                _logger.info('porcentaje_cuenta :' + str(porcentaje_cuenta) )

                                
                                cuenta_sueldo = ''
                                cuenta_honorarios = ''
                                cuenta_contribucion = ''

                            
                                contribuciones_cuenta = (valor_contribucion / HORAS_SUELDO) * total_hrs_indirectas
                                honorario_cuenta =  (valor_honorario / HORAS_SUELDO) * total_hrs_indirectas

                                cta_sueldo = self.env['account.account'].search(
                                    [('area', '=', area), ('unidad_operativa', '=', unidad_operativa), ('company_id', '=', self.company_id.id),
                                        ('tipo_cuenta', '=', 'sueldo')],
                                    limit=1)
                                _logger.info('AAAAAAAAActa_sueldo IND ' + str(cta_sueldo))
                                if cta_sueldo:
                                    cuenta_sueldo=cta_sueldo.name
                                cta_contribucion = self.env['account.account'].search(
                                    [('area', '=', area), ('unidad_operativa', '=', unidad_operativa), ('company_id', '=', self.company_id.id),
                                        ('tipo_cuenta', '=', 'contribucion')], limit=1)
                                _logger.info('AAAAAActa_contribucion IND ' + str(cta_contribucion))
                                if cta_contribucion:
                                    cuenta_contribucion=cta_contribucion.name
                  
                                cta_honorarios = self.env['account.account'].search(
                                    [('area', '=', area), ('unidad_operativa', '=', unidad_operativa), ('company_id', '=', self.company_id.id),
                                        ('tipo_cuenta', '=', 'honorario')],
                                    limit=1)
                                _logger.info('AAAAAActa_honorarios IND ' + str(cta_honorarios))
                                if cta_honorarios:
                                    cuenta_honorarios=cta_honorarios.name
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
                                    'costo_honorario':honorario_cuenta,
                                    'tipo': tipo_costo,
                                  #  'es_freelance': es_freelance,
                                    'cuenta_honorario': cuenta_honorarios,
                                    'cuenta_sueldo': cuenta_sueldo,
                                    'cuenta_contribucion': cuenta_contribucion
                                }
                                self.env['intercompany.cost.line'].create(vals)


        self.state='checkpoint'

    def post_intercompany_cost(self):
        #PARAMETROS
        DIARIO = int(self.env['ir.config_parameter'].get_param('diario-' + str(self.company_id.id), '')) #mex 2 = id 15 #usa 3= -23
        CUENTA_SUELDOS_APAGAR =int(self.env['ir.config_parameter'].get_param('cta_sueldosapagar-' + str(self.company_id.id), ''))
        
        _logger.info('CUENTA_SUELDOS_APAGAR ' + str(CUENTA_SUELDOS_APAGAR))
        #agrupo por area y cuenta para crear el asiento
        lines = [(5, 0, 0)]
        request= "SELECT  SUM(costo_sueldo) as sum_costosueldo,SUM(costo_contribuciones) as sum_costo_contribuciones,SUM(costo_honorario) as sum_costo_honorario,  area, unidad_operativa, account_id " \
                 " FROM intercompany_cost_line  WHERE account_itc_id =" + str(self.id) + " GROUP BY area, unidad_operativa, account_id"

        self.env.cr.execute(request)
        monto_total = 0

        for record in self.env.cr.dictfetchall():
            area = record['area']
            analytic_account_id = record['account_id']
            unidad_operativa = record['unidad_operativa']
            cuenta_sueldo = self.env['account.account'].search(
                [('area', '=', area), ('unidad_operativa', '=', unidad_operativa), ('company_id', '=', self.company_id.id), ('tipo_cuenta','=','sueldo')], limit=1)
            
            _logger.info(
                'AREA UNIOPE: ' + str(area) + '-' + str(unidad_operativa) + '- Cuenta sueldo' +  str(cuenta_sueldo))
            
            # lo limito a uno para evitar errores, de todos modos el constraint deberia evitarlo
            monto= round(record['sum_costosueldo'],2)
            #freelance= record['es_freelance']
            #--------------- SUELDO EMPLEADO------------------#
            if cuenta_sueldo and (monto>0): # and not(freelance):
                #genero linea
                monto_total += monto
                val = {'account_id':cuenta_sueldo.id,
                          'analytic_account_id':analytic_account_id  ,
                          'currency_id':self.company_id.currency_id.id,
                          'debit':monto,
                          'amount_currency':monto}
                lines.append((0,0 , val))

            # --------------- HONORARIOS FREELANCE ------------------#
            monto = round(record['sum_costo_honorario'],2)
            cuenta_honorarios = self.env['account.account'].search(
                [('area', '=', area), ('unidad_operativa', '=', unidad_operativa), ('company_id', '=', self.company_id.id), ('tipo_cuenta', '=', 'honorario')],
                limit=1)
            _logger.info(
                'AREA UNIOPE: ' + str(area) + '-' + str(unidad_operativa) + '- Cuenta honorario' + str(cuenta_honorarios))
                
            if cuenta_honorarios and (monto > 0): # and freelance:
                # genero linea
                monto_total += monto
                val = {'account_id': cuenta_honorarios.id,
                        'analytic_account_id': analytic_account_id,
                        'currency_id': self.company_id.currency_id.id,
                        'debit': monto,
                        'amount_currency': monto}
                lines.append((0, 0, val))

            #"________CONTRIBUCIONES------"
            monto = round(record['sum_costo_contribuciones'],2)
            cuenta_contribucion = self.env['account.account'].search(
                [('area', '=', area), ('unidad_operativa', '=', unidad_operativa), ('company_id', '=', self.company_id.id),('tipo_cuenta','=','contribucion')], limit=1)
            _logger.info(
                'MOV : analitica' + str(analytic_account_id) + '- Cuenta' + str(cuenta_contribucion))

            if cuenta_contribucion and (monto > 0):
                # genero linea
                monto_total += monto
                val = {'account_id': cuenta_contribucion.id,
                       'analytic_account_id': analytic_account_id,
                       'currency_id': self.company_id.currency_id.id,
                       'debit': monto,
                       'amount_currency': monto}
                lines.append((0, 0, val))
        #END FOR
        if monto_total>0:
            _logger.info('MONTO TOTAL' + str(monto_total))
            val={'account_id': CUENTA_SUELDOS_APAGAR,
                'currency_id': self.company_id.currency_id.id,
                'credit': monto_total,
                'amount_currency': monto_total * -1,
            }
            lines.append((0, 0, val))
            move = self.env['account.move'].create({'journal_id': DIARIO, 'currency_id': self.company_id.currency_id.id,'line_ids':lines })
            move.action_post()

        #publico
        self.state='post'
