from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'

    notify_invoice = fields.Boolean('notify_invoice', default=False)
    notify_shipment = fields.Boolean('notify_shipment', default=False)
    notify_withholding = fields.Boolean('notify_withholding', default=False)
