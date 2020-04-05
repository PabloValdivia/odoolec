# -*- coding: utf-8 -*-
# from odoo import http


# class Odoo-lec(http.Controller):
#     @http.route('/odoo-lec/odoo-lec/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo-lec/odoo-lec/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo-lec.listing', {
#             'root': '/odoo-lec/odoo-lec',
#             'objects': http.request.env['odoo-lec.odoo-lec'].search([]),
#         })

#     @http.route('/odoo-lec/odoo-lec/objects/<model("odoo-lec.odoo-lec"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo-lec.object', {
#             'object': obj
#         })
