# -*- coding: utf-8 -*-
import base64
from odoo import http
from odoo.http import request
from odoo.addons.survey.controllers.main import Survey


class Survey(Survey):

    @http.route(["/web/binary/download/<int:file_id>"], type='http', auth="public", website=True, sitemap=False)
    def binary_download(self, file_id=None, **post):
        if file_id:
            binary_file = request.env['survey.binary'].browse([file_id])
            if binary_file:
                content = base64.b64decode(binary_file.binary_data)
                if content:
                    return request.make_response(content, [
                        ('Content-Type', 'application/octet-stream'),
                        ('Content-Length', len(content)),
                        ('Content-Disposition', 'attachment; filename=' + binary_file.binary_filename + ';')
                    ])
        return False
