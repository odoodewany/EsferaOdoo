import logging,requests,json
from odoo.http import request
from odoo import models, fields, api, _
from odoo.exceptions import UserError
_logger=logging.getLogger(__name__)
class ResCompany(models.Model):
    _inherit = 'res.company'
    url_base_redirect = fields.Char(string="URL Base Redirección")

    
    def _comute_callback(self):
        for domain_sequence in self:
            domain_sequence.redirect_urls = str(self.url_base_redirect) + \
                    "/zoom/"+str(self.id)+"/OAuth2"