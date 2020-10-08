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

import logging

_logger = logging.getLogger(__name__)


class Company(models.Model):
    _inherit = 'res.company'

    help = fields.Char(
        default='** Very large text that I need to display in the res.company form view if it is possible as one '
                'single line depending on the size of the view.',
        readonly=True)
    taxid_type = fields.Many2one('lec.taxid.type')
    taxpayer_type = fields.Many2one('lec.taxpayer.type', related='partner_id.taxpayer_type', string='Tax Payer Type',
                                    compute='_compute_taxpayertype', inverse='_inverse_taxpayer')

    @api.constrains('vat')
    def check_vat(self):
        if len(self.vat) < 13:
            raise UserError('tax id is minor than allowed company')
        elif len(self.vat) > 13:
            raise UserError('tax id is major than allowed')

    # The next method returns the value inserted in res.partner taxpayer_type field and assign to respective field
    # in the res.company form
    def _inverse_taxpayer(self):
        for company in self:
            company.partner_id.taxpayer_type = company.taxpayer_type

    # The next method set and assign the value inserted in res.company to the corresponding field in its respective
    # partner's contact payertype in res.partner.

    @api.model
    def create(self, vals):
        company = super(Company, self).create(vals)
        if company.partner_id:
            company.partner_id.write({'taxid_type': company.taxid_type.id})
        return company
