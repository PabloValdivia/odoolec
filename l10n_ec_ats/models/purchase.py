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

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    document_no = fields.Char('Numero de Documento')
    authorization_code = fields.Char('Codigo de autorizacion')
    auth_date = fields.Date('Fecha de autorizacion')
    sustento_id = fields.Many2one('sustents.tax', 'Sustento Tributario')

    @api.onchange('authorization_code')
    def _authorization_code(self):
        if self.authorization_code:
            if len(self.authorization_code) != 10 and len(self.authorization_code) != 49:
                raise ValidationError("Error the code is not valid")

    @api.constrains('document_no')
    def validate_number_invoice(self):
        count = 0
        moves = self.env['account.move'].search([
            ('document_no', '=', self.document_no),
            ('partner_id', '=', self.partner_id.id),
            ('state', '=', 'posted')
        ])
        for move in moves:
            credit_note = self.env['account.move'].search([
                ('reversed_entry_id', '=', move.id),
                ('state', '=', 'posted')
            ])
            if not credit_note:
                count += 1
        if count > 1:
            raise ValidationError('El numero de factura del proveedor ya esta registrada')

    @api.onchange('document_no')
    def create_number(self):
        if self.document_no:
            if len(self.document_no) != 17:
                if self.document_no.isdigit() and len(self.document_no) == 15:
                    first = self.document_no[0:3] + '-'
                    two = self.document_no[3:6] + '-'
                    three = self.document_no[6:17]
                    self.document_no = str(first) + str(two) + str(three)
                else:
                    raise ValidationError(_('Error the document number is incorrect'))
