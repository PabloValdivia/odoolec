# -*- coding: utf-8 -*-
# from odoo import http


# class L10nEcEin(http.Controller):
#     @http.route('/l10n_ec_ein/l10n_ec_ein/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_ec_ein/l10n_ec_ein/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_ec_ein.listing', {
#             'root': '/l10n_ec_ein/l10n_ec_ein',
#             'objects': http.request.env['l10n_ec_ein.l10n_ec_ein'].search([]),
#         })

#     @http.route('/l10n_ec_ein/l10n_ec_ein/objects/<model("l10n_ec_ein.l10n_ec_ein"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_ec_ein.object', {
#             'object': obj
#         })
