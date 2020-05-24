from odoo import fields, models, api


class SriAuthorization (models.Model):
    _name = 'sri.authorization'
    _description = 'SRI Authorization'

    sri_authorization_code = fields.Char()
    sri_authorization_date = fields.Date()
    processed = fields.Boolean(default=False)
    env_service = fields.Selection(
        [
            ('1', 'Test'),
            ('2', 'Production')
        ],
        string='Environment Type',
        required=True,
        )

    account_move = fields.Many2one('account.move', string='Invoice Related')

    


