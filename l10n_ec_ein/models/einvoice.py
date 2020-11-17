import base64
import os
import logging
import itertools
from io import StringIO
from shutil import copyfile
from xml.dom import minidom

from odoo.addons.account.models.account_payment import MAP_INVOICE_TYPE_PARTNER_TYPE

import pytz
from jinja2 import Environment, FileSystemLoader, Template

from odoo import api, models, fields
from odoo.exceptions import Warning as UserError

from odoo.addons.base.models.ir_attachment import IrAttachment
from odoo.tools import safe_eval

from . import utils
from . import edocument

MAP_INVOICE_TYPE_PARTNER_TYPE.update({'liq_purchase': 'supplier'})
from ..xades.sri import DocumentXML, SriService
from ..xades.xades import Xades
import os.path
from os import path

sign = '/tmp/sign.p12'


class Invoice(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'account.edocument']
    _logger = logging.getLogger('account.edocument')
    TEMPLATES = {
        'out_invoice': 'out_invoice.xml',
        'out_refund': 'out_refund.xml'
    }

    SriServiceObj = SriService()

    sri_authorization = fields.Many2one('sri.authorization', copy=False)
    sri_payment_type = fields.Many2one('sri.payment_type', copy=False)

    def _info_invoice(self):
        """
        """
        company = self.company_id
        partner = self.partner_id
        infoFactura = {
            'fechaEmision': self.invoice_date.strftime("%d/%m/%Y"),
            'dirEstablecimiento': company.street,
            'obligadoContabilidad': company.is_force_keep_accounting,
            'tipoIdentificacionComprador': partner.taxid_type.code,
            'razonSocialComprador': partner.name,
            'identificacionComprador': partner.vat,
            'direccionComprador': partner.street,
            'totalSinImpuestos': '%.2f' % (self.amount_untaxed),
            'totalDescuento': '0.00',
            'propina': '0.00',
            'importeTotal': '{:.2f}'.format(self.amount_total),
            'moneda': 'USD',
            'formaPago': self.sri_payment_type.code,
            'valorRetIva': '0.00',
            'valorRetRenta': '0.00',
            'contribuyenteEspecial': company.is_special_taxpayer
        }

        totalConImpuestos = []
        for lines in self.invoice_line_ids:
            totalImpuesto = {
                'codigo': lines.tax_ids.sri_code.code,
                'codigoPorcentaje': lines.tax_ids.sri_rate.code,
                'baseImponible': '{:.2f}'.format(lines.price_subtotal),
                'tarifa': lines.tax_ids.amount,
                'valor': '{:.2f}'.format(lines.price_subtotal * (lines.tax_ids.amount / 100))
            }
            totalConImpuestos.append(totalImpuesto)

        infoFactura.update({'totalConImpuestos': totalConImpuestos})

        if self.type == 'out_refund':
            inv = self.search([('name', '=', self.origin)], limit=1)
            inv_number = self.name
            notacredito = {
                'codDocModificado': inv.auth_inv_id.type_id.code,
                'numDocModificado': inv_number,
                'motivo': self.name,
                'fechaEmisionDocSustento': (inv.invoice_date),
                'valorModificacion': self.amount_total
            }
            infoFactura.update(notacredito)
        return infoFactura

    def _detalles(self, invoice):
        """
        """
        def fix_chars(code):
            special = [
                [u'%', ' '],
                [u'º', ' '],
                [u'Ñ', 'N'],
                [u'ñ', 'n']
            ]
            for f, r in special:
                code = code.replace(f, r)
            return code

        detalle_adicional = {
            'nombre': 'Unidad',
            'valor': 1
        }

        detalles = []
        for line in invoice.invoice_line_ids:
            codigoPrincipal = line.product_id and \
                              line.product_id.default_code and \
                              fix_chars(line.product_id.default_code) or '001'
            priced = line.price_unit * (1 - (line.discount or 0.00) / 100.0)
            discount = (line.price_unit - priced) * line.quantity
            detalle = {
                'codigoPrincipal': codigoPrincipal,
                'descripcion': fix_chars(line.name.strip()),
                'cantidad': '%.6f' % line.quantity,
                'precioUnitario': '%.6f' % line.price_unit,
                'descuento': '%.2f' % discount,
                'precioTotalSinImpuesto': '%.2f' % line.price_subtotal,
                'detalle_adicional': detalle_adicional
            }
            impuestos = []
            for tax_line in line:
                percent = int(tax_line.tax_ids.amount)
                impuesto = {
                    'codigo': tax_line.tax_ids.sri_code.code,
                    'codigoPorcentaje': tax_line.tax_ids.sri_rate.code,
                    'tarifa': percent,
                    'baseImponible': '{:.2f}'.format(tax_line.price_subtotal),
                    'valor': '{:.2f}'.format(tax_line.price_subtotal * (tax_line.tax_ids.amount / 100))
                }
                impuestos.append(impuesto)
        detalle.update({'impuestos': impuestos})
        detalles.append(detalle)
        return {'detalles': detalles}

    def render_authorized_einvoice(self, autorizacion):
        tmpl_path = os.path.join(os.path.dirname(__file__), 'templates')
        env = Environment(loader=FileSystemLoader(tmpl_path))
        einvoice_tmpl = env.get_template('authorized_einvoice.xml')
        auth_xml = {
            'estado': autorizacion.estado,
            'numeroAutorizacion': autorizacion.numeroAutorizacion,
            'ambiente': autorizacion.ambiente,
            'fechaAutorizacion': str(autorizacion.fechaAutorizacion.strftime("%d/%m/%Y %H:%M:%S")),
            'comprobante': autorizacion.comprobante
        }
        auth_invoice = einvoice_tmpl.render(auth_xml)
        return auth_invoice

    def action_generate_einvoice(self):
        for obj in self:
            if obj.type not in ['out_invoice', 'out_refund'] and not obj.journal_id.is_electronic_document:
                continue
            access_key, emission_code = self._get_codes(name='account.move')
            einvoice = self.render_document(obj, access_key, emission_code)
            inv_xml = DocumentXML(einvoice, obj.type)
            if not inv_xml.validate_xml():
                raise UserError("Not Valid Schema")

            xades = self.env['sri.key.type'].search([
                ('company_id', '=', self.company_id.id)
            ])
            x_path = "/tmp/ComprobantesGenerados/"
            if not path.exists(x_path):
                os.mkdir(x_path)
            to_sign_file = open(x_path+'FACTURA_SRI_'+self.name+".xml", 'w')
            to_sign_file.write(einvoice)
            to_sign_file.close()
            signed_document = xades.action_sign(to_sign_file)
            ok, errores = inv_xml.send_receipt(signed_document)
            if not ok:
                raise UserError(errores)
            auth, m = inv_xml.request_authorization(access_key)
            if not auth:
                msg = ' '.join(list(itertools.chain(*m)))
                raise UserError(msg)
            auth_einvoice = self.render_authorized_einvoice(auth)
            sri_auth = self.env['sri.authorization'].create({
                'sri_authorization_code': auth['numeroAutorizacion'],
                'sri_authorization_date': auth['fechaAutorizacion'],
                'account_move': self.id,
                'env_service': self.company_id.env_service
            })
            self.write({'sri_authorization': sri_auth.id})
            attach = self.add_attachment(auth_einvoice, auth)
            message = """
            DOCUMENTO ELECTRONICO GENERADO <br><br>
            CLAVE DE ACCESO: %s <br>
            NUMERO DE AUTORIZACION %s <br>
            FECHA AUTORIZACION: %s <br>
            ESTADO DE AUTORIZACION: %s <br>
            AMBIENTE: %s <br>
            """ % (
                auth['numeroAutorizacion'],
                auth['numeroAutorizacion'],
                auth['fechaAutorizacion'],
                auth['estado'],
                'PRUEBAS' if self.company_id.env_service == '1' else 'PRODUCCION'
            )
            self.message_post(body=message, attachments=auth_einvoice)
            # self.send_document(
            #    attachments=[a.id for a in attach],
            #    tmpl='l10n_ec_ein.email_template_einvoice'
            # )

    def add_attachment(self, xml_element, auth):
        attach = self.env['ir.attachment'].create(
            {
                'name': '{0}.xml'.format(auth['numeroAutorizacion']),
                'datas': xml_element,
                'res_model': self._name,
                'res_id': self.id,
                'type': 'binary'
            },
        )
        return attach

    @api.model
    def send_document(self, attachments=None, tmpl=False):
        self.ensure_one()
        self._logger.info('Enviando documento electronico por correo')
        tmpl = self.env.ref(tmpl)
        tmpl.send_mail(  # noqa
            self.id,
            email_values={'attachment_ids': attachments}
        )
        self.sent = True
        return True

    def _compute_discount(self, detalles):
        total = sum([float(det['descuento']) for det in detalles['detalles']])
        return {'totalDescuento': total}

    def render_document(self, invoice, access_key, emission_code):
        tmpl_path = os.path.join(os.path.dirname(__file__), 'templates')
        env = Environment(loader=FileSystemLoader(tmpl_path))
        einvoice_tmpl = env.get_template(self.TEMPLATES[self.type])
        data = {}
        data.update(self._info_tributaria(invoice, access_key, emission_code))
        data.update(self._info_invoice())
        detalles = self._detalles(invoice)

        data.update(detalles)
        data.update(self._compute_discount(detalles))
        einvoice = einvoice_tmpl.render(data)
        return einvoice

    @staticmethod
    def _read_template(type):
        with open(os.path.join(os.path.dirname(__file__), 'templates', type + ".xml")) as template:
            return template

    @staticmethod
    def render(self, template_path, **kwargs):
        return Template(
            self._read_template(template_path)
        ).substitute(**kwargs)
