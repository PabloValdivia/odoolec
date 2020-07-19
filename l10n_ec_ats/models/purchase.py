# -*- coding: utf-8 -*-
###############################################################################
#
#    INGEINT SA.
#    Copyright (C) 2020 INGEINT SA-(<http://www.ingeint.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    document_no = fields.Char('Numero de Documento')
    authorization_code = fields.Char('Codigo de autorizacion')
    auth_date = fields.Date('Fecha de autorizacion')

    @api.onchange('authorization_code')
    def _authorization_code(self):
        if self.authorization_code:
            if len(self.authorization_code) != 10 and len(self.authorization_code) != 49:
                raise ValidationError("Error the code is not valid")