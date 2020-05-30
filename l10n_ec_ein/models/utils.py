# -*- coding: utf-8 -*-

import requests

tipoIdentificacion = {
    'ruc': '04',
    'cedula': '05',
    'pasaporte': '06',
    'venta_consumidor_final': '07',
    'identificacion_exterior': '08',
    'placa': '09',
}

codigoImpuesto = {
    'vat': '2',
    'vat0': '2',
    'ice': '3',
    'other': '5'
}

tabla17 = {
    'vat': '2',
    'vat0': '2',
    'ice': '3',
    'irbpnr': '5'
}

tabla18 = {
    0: '0',
    12: '2',
    14: '3'
}

tabla20 = {
    'ret_ir': '1',
    'ret_vat_b': '2',
    'ret_vat_srv': '2',
    'ret_isd': '6'
}

tabla21 = {
    '10': '9',
    '20': '10',
    '30': '1',
    '50': '11',
    '70': '2',
    '100': '3'
}

codigoImpuestoRetencion = {
    'ret_ir': '1',
    'ret_vat_b': '2',
    'ret_vat_srv': '2',
    'ice': '3',
}

tarifaImpuesto = {
    'vat0': '0',
    'vat': '2',
    'novat': '6',
    'other': '7',
}

MSG_SCHEMA_INVALID = u"El sistema generó el XML pero"
" el comprobante electrónico no pasa la validación XSD del SRI."


def check_service(env, url):
    flag = False
    if env == 'test':
        URL = url
    else:
        URL = url

    for i in [1, 2, 3]:
        try:
            res = requests.head(URL, timeout=3)
            flag = True
        except requests.exceptions.RequestException:
            return flag, False
    return flag, res

def get_authorisation(type_document):
    map_type = {
                'out_invoice': '18',
                'in_invoice': '01',
                'out_refund': '04',
                'in_refund': '05',
                'liq_purchase': '03',
                'ret_in_invoice': '07',
            }
    code = map_type[type_document]
    return code
