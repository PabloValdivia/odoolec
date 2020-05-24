from odoo import fields, models, api


class Company(models.Model):
    _inherit = 'res.company'

    electronic_signature = fields.Many2many(comodel_name="ir.attachment",
                                     relation="m2m_ir_identity_card_rel",
                                     column1="m2m_id",
                                     column2="attachment_id",
                                     string="Electronic Signature")
    password_electronic_signature = fields.Char(
        'Electronic Password',
        size=255,
    )

    env_service = fields.Selection(
        [
            ('1', 'Test'),
            ('2', 'Production')
        ],
        string='Environment Type',
        required=True,
        default='1'
    )


