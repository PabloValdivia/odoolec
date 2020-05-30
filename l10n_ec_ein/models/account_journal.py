from odoo import fields, models, api


class Company(models.Model):
    _inherit = 'account.journal'

    is_electronic_document = fields.Boolean(default=False)
    sri_doctype = fields.Selection(
        [
            ('01', 'Invoice'),
            ('03', 'Purchase Liquidation'),
            ('04', 'Credit Note'),
            ('05', 'Debit Note'),
            ('06', 'Referral Guide'),
            ('07', 'Withholding')
        ]
    )

