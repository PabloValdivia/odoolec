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


class Company(models.Model):
    _inherit = 'res.company'

    taxid_type = fields.Many2one('lec.taxid.type', string='TaxID Type')
    taxpayer_type = fields.Many2one('lec.taxpayer.type', string='Tax Payer Type')

    @api.constrains('vat')
    def check_vat(self):
        tt = self.env['lec.taxid.type'].search([
            ('id', '=', self.taxid_type.id)])

        if len(self.vat) < tt.min_length:
            raise UserError('tax id is minor than allowed')
        elif len(self.vat) > tt.max_length:
            raise UserError('tax id is major than allowed')
