from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    grupo_id = fields.Many2one('res.groups', string="Grupo")
    inscripcion_ids = fields.One2many('slide.channel.inscripciones', 'product_id', string="Inscripciones")
    
    def get_atributo_duracion(self):
        # Busca el atributo 'Duración meses' en la lista de valores de atributos
        duracion = self.product_template_attribute_value_ids.filtered(
            lambda x: x.attribute_id.display_name == 'Duración meses')
        # Si el atributo se encuentra, devuelve su valor convertido en integer
        if duracion:
            return int(duracion.name)
        # Si el atributo no se encuentra, devuelve 0
        return 0

class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    inscripcion_ids = fields.One2many('slide.channel.inscripciones', 'product_id', string="Inscripciones")

    def get_atributo_duracion(self):
        # Busca el atributo 'Duración meses' en la lista de valores de atributos
        duracion = self.product_template_attribute_value_ids.filtered(
            lambda x: x.attribute_id.display_name == 'Duración meses')
        # Si el atributo se encuentra, devuelve su valor convertido en integer
        if duracion:
            return int(duracion.name)
        # Si el atributo no se encuentra, devuelve 0
        return 0


class SlideChannelInscripciones(models.Model):
    _name = 'slide.channel.inscripciones'
    _description = "Inscripciones de cursos"

    partner_id = fields.Many2one('res.partner', string="Cliente")
    product_id = fields.Many2one('product.product', string="Producto")
    fecha_inicio = fields.Date(string="Fecha de inicio")
    fecha_fin = fields.Date(string="Fecha de fin")
    grupo_id = fields.Many2one('res.groups', string="Grupo")
    activo = fields.Boolean(string="Activo", default=True)
    #cursos_ids = fields.One2many('slide.channel.partner', 'partner_id', string="Cursos")


    @api.model
    def create(self, vals):
        record = super().create(vals)
        if 'grupo_id' in vals and vals['activo']:
            user = self.env['res.users'].search([('partner_id', '=', record.partner_id.id)], limit=1)
            if user:
                user.groups_id |= record.grupo_id
        return record

    def write(self, vals):
        res = super().write(vals)
        user = self.env['res.users'].search([('partner_id', '=', self.partner_id.id)], limit=1)
        for record in self:
            if 'activo' in vals:
                if vals['activo']:
                    if user:
                        user.groups_id |= record.grupo_id
                else:
                    user.groups_id -= record.grupo_id
        return res

    def check_end_dates(self):
        # Get today's date
        today = fields.Date.today()
        # Iterate over records that need to be deactivated
        for record in self.search([('fecha_fin', '<', today), ('activo', '=', True)]):
            user = self.env['res.users'].search([('partner_id', '=', record.partner_id.id)], limit=1)
            # Deactivate records
            record.activo = False
            # Remove group from partner
            user.groups_id -= record.grupo_id

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        res = super(AccountMove, self).action_post()
        """ inscripciones = self.env['slide.channel.inscripciones']
        for invoice in self:
            if invoice.move_type == 'out_invoice':
                user = self.env['res.users'].search([('partner_id', '=', invoice.partner_id.id)], limit=1)
                for line in invoice.invoice_line_ids:
                    if line.product_id.detailed_type == 'service':
                        inscripciones.create({
                            'partner_id': line.partner_id.id,
                            'product_id': line.product_id.id,
                            'fecha_inicio': invoice.invoice_date,
                            'fecha_fin': invoice.invoice_date + relativedelta(months=line.product_id.get_atributo_duracion()),
                            'grupo_id': line.product_id.grupo_id.id,
                            'activo': True,
                        })
                        user.groups_id |= line.product_id.grupo_id """

        inscripciones = self.env['slide.channel.inscripciones']
        for invoice in self:
            if invoice.move_type == 'out_invoice':
                user = self.env['res.users'].search([('partner_id', '=', invoice.partner_id.id)], limit=1)
                for line in invoice.invoice_line_ids:
                    if line.product_id.detailed_type == 'service':
                        fecha_inicio = invoice.invoice_date
                        fecha_fin = fecha_inicio
                        
                        grupo_id = line.product_id.grupo_id

                        # Buscar registros existentes con las mismas condiciones de partner_id y product_tmpl_id
                        existing_inscriptions = inscripciones.search([
                            ('partner_id', '=', line.partner_id.id),
                            ('product_id.product_tmpl_id', '=', line.product_id.product_tmpl_id.id),
                            ('activo', '=', True),
                            ('fecha_fin', '>', invoice.invoice_date),
                        ])

                        # Encontrar la fecha_fin más alta entre los registros existentes que cumplen el filtro
                        max_fecha_fin = max(existing_inscriptions.mapped('fecha_fin'), default=fecha_inicio)
                        fecha_fin = max_fecha_fin + relativedelta(months=line.product_id.get_atributo_duracion())

                        for inscription in existing_inscriptions:
                            inscription.activo = False
                        # Crear una nueva inscripción con las fechas adecuadas
                        inscripciones.create({
                            'partner_id': line.partner_id.id,
                            'product_id': line.product_id.id,
                            'fecha_inicio': fecha_inicio,
                            'fecha_fin': max(fecha_fin, max_fecha_fin),
                            'grupo_id': line.product_id.grupo_id.id,
                            'activo': True,
                        })

                        # Actualizar los grupos del usuario
                        user.groups_id |= line.product_id.grupo_id
        return res