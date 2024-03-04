# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SlideChannelTagGroupWebsite(models.Model):
    _name = 'slide.channel.tag.group.website'
    _description = 'Channel/Course Groups'
    _inherit = 'website.published.mixin'
    _order = 'sequence asc'
    
    website_id = fields.Many2one('website', string='Website', required=True, ondelete='cascade', help="Website in which this group is available.")

    @api.model
    def get_website_groups(self):
        """Método para obtener los grupos disponibles para el sitio web actual."""
        return self.search([('website_id', '=', self.env.context.get('website_id'))])
