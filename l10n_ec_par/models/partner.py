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
from .utils import validator_identifier


class Partner(models.Model):
    _inherit = 'res.partner'

    taxid_type = fields.Many2one('lec.taxid.type', string='TaxID Type')
    taxpayer_type = fields.Many2one('lec.taxpayer.type', string='Tax Payer Type')

    @api.constrains('vat', 'taxid_type', 'taxpayer_type')
    def check_vat(self):

        for record in self:
            if record.vat:
                tt = record.env['lec.taxid.type'].search([
                    ('id', '=', record.taxid_type.id)])
                if tt.min_length > 0 or tt.max_length > 0:
                    if record.vat == False or len(record.vat) < tt.min_length:
                        raise ValidationError('Tax id is minor than allowed')
                    elif len(record.vat) > tt.max_length:
                        raise ValidationError('Tax id is major than allowed')

    _sql_constraints = [('vat_unique', 'unique(vat,taxid_type)', 'Error, Identificador duplicado')]

    @api.depends('vat', 'name')
    def name_get(self):
        data = []
        for partner in self:
            display_val = u'{0} {1}'.format(
                partner.vat or '*',
                partner.name
            )
            data.append((partner.id, display_val))
        return data

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=80):
        if not args:
            args = []
        if name:
            partners = self.search([('vat', operator, name)] + args, limit=limit)  # noqa
            if not partners:
                partners = self.search([('name', operator, name)] + args, limit=limit)  # noqa
        else:
            partners = self.search(args, limit=limit)
        return partners.name_get()
