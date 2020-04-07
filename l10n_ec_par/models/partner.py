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


class Partner(models.Model):
    _inherit = 'res.partner'

    taxid_type = fields.Many2one('lec.taxid.type', string='TaxID Type')
    taxpayer_type = fields.Many2one('lec.taxpayer.type', string='Tax Payer Type')

    @api.constrains('vat', 'taxid_type', 'taxpayer_type')
    def check_vat(self):
        for record in self:
            if record.vat == False or len(record.vat) < 13:
                raise ValidationError('Tax id is minor than allowed')
            elif len(record.vat) > 13:
                raise ValidationError('Tax id is major than allowed')

    
#    def _inverse_taxpayer(self):
#        for company in self:
#            company.partner_id.taxpayer_type = company.taxpayer_type
            
#            tt = record.env['lec.taxid.type'].search([
#                ('id', '=', record.taxid_type.id)])
#            if tt.id == 0:
#                raise ValidationError('Tax id type is mandatory')

#            if tt.min_length > 0 or tt.max_length > 0:

#                if record.vat == False or len(record.vat) < tt.min_length:
#                    raise ValidationError('Tax id is minor than allowed')
#                elif len(record.vat) > tt.max_length:
#                    raise ValidationError('Tax id is major than allowed')

#            if record.commercial_partner_id.id == record.id:

#                if record.taxpayer_type.id == 0:
#                    raise ValidationError('Taxpayer type is mandatory')

                
