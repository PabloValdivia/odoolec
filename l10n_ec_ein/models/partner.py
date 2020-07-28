from odoo import fields, models, api
from odoo.exceptions import AccessError, ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    notify_invoice = fields.Boolean('notify_invoice', default=False)
    notify_shipment = fields.Boolean('notify_shipment', default=False)
    notify_withholding = fields.Boolean('notify_withholding', default=False)

    @api.constrains('vat')
    def validate_tax_code(self):
        if not self.parent_id:
            for row in self:
                vat_bp = [x.id for x in self.search(
                    [('vat', '=', row.vat)])]
                vat_bp.remove(row.id)
                if len(vat_bp) >= 1:
                    raise ValidationError('You are doubling the identification number')

