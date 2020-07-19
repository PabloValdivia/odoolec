# -*- coding: utf-8 -*-
# from odoo import http


# class L10nEcPurchase(http.Controller):
#     @http.route('/l10n_ec_purchase/l10n_ec_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_ec_purchase/l10n_ec_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_ec_purchase.listing', {
#             'root': '/l10n_ec_purchase/l10n_ec_purchase',
#             'objects': http.request.env['l10n_ec_purchase.l10n_ec_purchase'].search([]),
#         })

#     @http.route('/l10n_ec_purchase/l10n_ec_purchase/objects/<model("l10n_ec_purchase.l10n_ec_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_ec_purchase.object', {
#             'object': obj
#         })
