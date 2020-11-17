# Copyright 2020 Carlos Lopez Mite<celm1990@gmail.com>
import base64
import logging
import subprocess
import tempfile
from datetime import datetime
from random import randrange
from xml.etree import ElementTree

import xmlsig
from lxml import etree
from OpenSSL import crypto
from xades import XAdESContext, template
from xades.policy import ImpliedPolicy

from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
KEY_TO_PEM_CMD = "openssl pkcs12 -nocerts -in %s -out %s -passin pass:%s -passout pass:%s"
STATES = {"unverified": [("readonly", False),]}


class SriKeyType(models.Model):
    _name = "sri.key.type"
    _description = "Tipo de Llave electronica"

    name = fields.Char(string="Nombre", readonly=True, states=STATES)
    file_content = fields.Binary("Archivo de Firma", readonly=True, states=STATES)
    file_name = fields.Char("Nombre de archivo", readonly=True)
    password = fields.Char("Clave de firma", readonly=True, states=STATES)
    private_key = fields.Text(string="Private Key", readonly=True)
    active = fields.Boolean("Activo?", default=True)
    company_id = fields.Many2one("res.company", "Compañia", default=lambda self: self.env.user.company_id)
    state = fields.Selection(
        [("unverified", "Sin Verificar"), ("valid", "Firma Valida"), ("expired", "Firma Vencida")],
        string="Estado",
        default="unverified",
        readonly=True,
    )
    # datos informativos del certificado
    emision_date = fields.Date(string="Fecha de Emision", readonly=True)
    expire_date = fields.Date(string="Fecha de Vencimiento", readonly=True)
    subject_serial_number = fields.Char(string="Numero de Serie(Asunto)", readonly=True)
    subject_common_name = fields.Char(string="Organizacion(Asunto)", readonly=True)
    issuer_common_name = fields.Char(string="Organizacion(Emisor)", readonly=True)
    cert_serial_number = fields.Char(string="Numero de serie(cerificado)", readonly=True)
    cert_version = fields.Char(string="Version", readonly=True)

    def action_validate_and_load(self):
        filecontent = base64.b64decode(self.file_content)
        try:
            p12 = crypto.load_pkcs12(filecontent, self.password)
        except Exception as ex:
            _logger.warning(tools.ustr(ex))
            raise UserError(
                _(
                    "Error opening the signature, possibly the signature key has been entered incorrectly or the file is not supported. \n%s"
                ) % (tools.ustr(ex))
            )

        private_key = self.convert_key_cer_to_pem(filecontent, self.password)
        start_index = private_key.find("Signing Key")
        # cuando el archivo tiene mas de una firma electronica
        # viene varias secciones con BEGIN ENCRYPTED PRIVATE KEY
        # diferenciandose por:
        # * Decryption Key
        # * Signing Key
        # asi que tomar desde Signing Key en caso de existir
        if start_index >= 0:
            private_key = private_key[start_index:]
        start_index = private_key.find("-----BEGIN ENCRYPTED PRIVATE KEY-----")
        private_key = private_key[start_index:]
        cert = self._extract_x509(p12)
        issuer = cert.get_issuer()
        subject = cert.get_subject()
        vals = {
            "emision_date": datetime.strptime(cert.get_notBefore().decode("utf-8"), "%Y%m%d%H%M%SZ"),
            "expire_date": datetime.strptime(cert.get_notAfter().decode("utf-8"), "%Y%m%d%H%M%SZ"),
            "subject_common_name": subject.CN,
            "subject_serial_number": subject.serialNumber,
            "issuer_common_name": issuer.CN,
            "cert_serial_number": cert.get_serial_number(),
            "cert_version": cert.get_version(),
            "private_key": private_key,
            "state": "valid",
        }
        self.write(vals)
        return True

    def convert_key_cer_to_pem(self, key, password):
        # TODO compute it from a python way
        with tempfile.NamedTemporaryFile(
            "wb", suffix=".key", prefix="edi.ec.tmp."
        ) as key_file, tempfile.NamedTemporaryFile("rb", suffix=".key", prefix="edi.ec.tmp.") as keypem_file:
            key_file.write(key)
            key_file.flush()
            subprocess.call((KEY_TO_PEM_CMD % (key_file.name, keypem_file.name, password, password)).split())
            key_pem = keypem_file.read().decode()
        return key_pem

    def action_sign(self, xml_string_data):
        def new_range():
            return randrange(100000, 999999)

        filecontent = base64.b64decode(self.file_content)
        try:
            private_key = crypto.load_privatekey(
                crypto.FILETYPE_PEM, self.private_key.encode("ascii"), self.password.encode()
            )
            p12 = crypto.load_pkcs12(filecontent, self.password)
        except Exception as ex:
            _logger.warning(tools.ustr(ex))
            raise UserError(
                _(
                    "Error opening the signature, possibly the signature key has been entered incorrectly or the file "
                    "is not supported. \n%s "
                ) % (tools.ustr(ex))
            )
        data = open(xml_string_data.name, 'rb')
        xslt_content = data.read()
        doc = etree.fromstring(xslt_content)
        signature_id = f"Signature{new_range()}"
        signature_property_id = f"{signature_id}-SignedPropertiesID{new_range()}"
        certificate_id = f"Certificate{new_range()}"
        reference_uri = f"Reference-ID-{new_range()}"
        signature = xmlsig.template.create(
            xmlsig.constants.TransformInclC14N, xmlsig.constants.TransformRsaSha1, signature_id,
        )
        xmlsig.template.add_reference(
            signature,
            xmlsig.constants.TransformSha1,
            name=f"SignedPropertiesID{new_range()}",
            uri=f"#{signature_property_id}",
            uri_type="http://uri.etsi.org/01903#SignedProperties",
        )
        xmlsig.template.add_reference(signature, xmlsig.constants.TransformSha1, uri=f"#{certificate_id}")
        ref = xmlsig.template.add_reference(
            signature, xmlsig.constants.TransformSha1, name=reference_uri, uri="#comprobante"
        )
        xmlsig.template.add_transform(ref, xmlsig.constants.TransformEnveloped)
        ki = xmlsig.template.ensure_key_info(signature, name=certificate_id)
        data = xmlsig.template.add_x509_data(ki)
        xmlsig.template.x509_data_add_certificate(data)
        xmlsig.template.add_key_value(ki)
        qualifying = template.create_qualifying_properties(signature, name=signature_id)
        props = template.create_signed_properties(qualifying, name=signature_property_id)
        signed_do = template.ensure_signed_data_object_properties(props)
        template.add_data_object_format(
            signed_do, f"#{reference_uri}", description="contenido comprobante", mime_type="text/xml",
        )
        doc.append(signature)
        x509 = self._extract_x509(p12)
        if x509 is not None:
            p12.set_certificate(x509)
            p12.set_privatekey(private_key)
        ctx = XAdESContext(ImpliedPolicy(xmlsig.constants.TransformSha1))
        ctx.load_pkcs12(p12)
        ctx.sign(signature)
        ctx.verify(signature)
        return etree.tostring(doc, encoding="UTF-8", pretty_print=True).decode()

    def _extract_x509(self, p12):
        is_digital_signature = False
        x509 = None
        # revisar si el certificado tiene la extension digital_signature activada
        # caso contrario tomar del listado de certificados el primero que tengan esta extension
        x509_to_review = p12.get_certificate().to_cryptography()
        for exten in x509_to_review.extensions:
            if exten.oid._name == "keyUsage" and exten.value.digital_signature:
                is_digital_signature = True
                x509 = p12.get_certificate()
                break
        if not is_digital_signature:
            # cuando hay mas de un certificado, tomar el certificado correcto
            # este deberia tener entre las extensiones digital_signature = True
            # pero si el certificado solo tiene uno, devolvera None
            ca_certificates_list = p12.get_ca_certificates()
            if ca_certificates_list is not None:
                for x509_inst in ca_certificates_list:
                    x509_cryp = x509_inst.to_cryptography()
                    for exten in x509_cryp.extensions:
                        if exten.oid._name == "keyUsage" and exten.value.digital_signature:
                            x509 = x509_inst
        return x509
