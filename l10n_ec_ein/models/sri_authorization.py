from odoo import fields, models, api


class SriAuthorization (models.Model):
    _name = 'sri.authorization'
    _description = 'SRI Authorization'

    sri_authorization_code = fields.Char()
    sri_create_date = fields.Datetime()
    sri_authorization_date = fields.Datetime()
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

    error_code = fields.Selection(
        [
            ('2', 'RUC del emisor NO se encuentra ACTIVO'),
            ('2', 'Production')
        ],
        string='Environment Type',
        required=False,
    )


    


