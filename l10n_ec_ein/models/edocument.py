# -*- coding: utf-8 -*-

import base64
import os
import logging
import itertools
from io import StringIO
from shutil import copyfile

from jinja2 import Environment, FileSystemLoader

from odoo import api, fields, models
from odoo.exceptions import Warning as UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

from . import utils
from ..xades.sri import SriService


class EDocument(models.AbstractModel):
    _name = 'account.edocument'
    _FIELDS = {
        'account.move': 'invoice_number'
    }
    SriServiceObj = SriService()

    clave_acceso = fields.Char(
        'Clave de Acceso',
        size=49,
        readonly=True
    )
    numero_autorizacion = fields.Char(
        'Número de Autorización',
        size=37,
        readonly=True
    )
    estado_autorizacion = fields.Char(
        'Estado de Autorización',
        size=64,
        readonly=True
    )
    fecha_autorizacion = fields.Datetime(
        'Fecha Autorización',
        readonly=True
    )
    ambiente = fields.Char(
        'Ambiente',
        size=64,
        readonly=True
    )
    autorizado_sri = fields.Boolean('¿Autorizado SRI?', readonly=True)
    security_code = fields.Char('Código de Seguridad', size=8, readonly=True)
    emission_code = fields.Char('Tipo de Emisión', size=1, readonly=True)
    sent = fields.Boolean('Enviado?')

    def get_auth(self, document):
        partner = document.company_id.partner_id
        if document._name == 'account.invoice':
            return document.auth_inv_id
        elif document._name == 'account.retention':
            return partner.get_authorisation('ret_in_invoice')

    def seq(self):
        return getattr(self, self._FIELDS[self._name])[6:]

    def _info_tributaria(self, document, access_key, emission_code):
        """
        """
        company = document.company_id
        infoTributaria = {
            'ambiente': self.env.user.company_id.env_service,
            'tipoEmision': '1',
            'razonSocial': company.name,
            'nombreComercial': company.name,
            'ruc': company.partner_id.vat,
            'claveAcceso': access_key,
            'codDoc': self.journal_id.sri_doctype,
            'estab': self.name[0:3],
            'ptoEmi': self.name[4:7],
            'secuencial': self.name[8:17],
            'dirMatriz': company.street
        }
        return infoTributaria

    def _get_codes(self, name='account.move'):
        ak_temp = self.get_access_key(name)
        self.SriServiceObj.set_active_env(self.env.user.company_id.env_service)
        access_key = self.SriServiceObj.create_access_key(ak_temp)
        emission_code = self.journal_id.sequence_id.prefix[0:3]
        return access_key, emission_code

    def get_access_key(self, name):
        date_doc = self.invoice_date.strftime("%d%m%Y")
        auth = self.journal_id.sri_doctype
        ruc = self.company_id.partner_id.vat
        environment = self.company_id.env_service
        sequence = self.name[8:17]
        emission = self.name[0:3]
        establishment = self.name[4:7]
        emission_type = '1'
        sri_document_code = self.company_id.partner_id.vat[5:13]
        access_key = (
            [date_doc, auth, ruc,
             environment, emission+establishment, sequence, sri_document_code],
        )
        return access_key






