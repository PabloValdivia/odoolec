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


class TaxIDType(models.Model):
    _name = "lec.taxid.type"
    _description = "Tax ID Type"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True

    code = fields.Char('code')
    name = fields.Char('name')
    min_length = fields.Integer('min_length')
    max_length = fields.Integer('max_length')
    default = fields.Boolean('default', default=False)



