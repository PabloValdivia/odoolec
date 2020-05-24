from odoo import fields, models, api


class SriParameters(models.Model):
    _name = 'sri.parameters'
    _description = 'SRI Parameters'

    site_base_test = fields.Char(string='Site Base Test')
    site_base_prod = fields.Char(string='Site Base Production')
    ws_test_url = fields.Char(string='SRI WS test url')
    ws_test_auth = fields.Char(string='SRI WS test auth')
    ws_prod_url = fields.Char(string='SRI WS production url')
    ws_prod_auth = fields.Char(string='SRI WS production auth')

