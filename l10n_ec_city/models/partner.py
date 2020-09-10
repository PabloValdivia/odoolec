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


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('code', '=', 'EC')], limit=1)
        return country

    country_id = fields.Many2one('res.country', string='Country',
                                 default=_get_default_country)
    city_id = fields.Many2one('res.country.city', string='city')

    @api.onchange('city_id')
    def onchange_city(self):
        self.city = self.city_id.name
