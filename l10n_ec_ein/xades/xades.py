# -*- coding: utf-8 -*-

import base64
import os
import subprocess
import logging


class CheckDigit(object):
    # Definicion modulo 11
    _MODULO_11 = {
        'BASE': 11,
        'FACTOR': 2,
        'RETORNO11': 0,
        'RETORNO10': 1,
        'PESO': 2,
        'MAX_WEIGHT': 7
    }

    @classmethod
    def _eval_mod11(self, modulo):
        if modulo == self._MODULO_11['BASE']:
            return self._MODULO_11['RETORNO11']
        elif modulo == self._MODULO_11['BASE'] - 1:
            return self._MODULO_11['RETORNO10']
        else:
            return modulo

    @classmethod
    def compute_mod11(self, dato):
        """
        Calculo mod 11
        return int
        """
        total = 0
        weight = self._MODULO_11['PESO']

        for item in reversed(dato):
            total += int(item) * weight
            weight += 1
            if weight > self._MODULO_11['MAX_WEIGHT']:
                weight = self._MODULO_11['PESO']
        mod = 11 - total % self._MODULO_11['BASE']

        mod = self._eval_mod11(mod)
        return mod


class Xades(object):

    def sign(self, to_sign_file, password):
        JAR_PATH = 'firma/IngeintXades.jar'
        JAVA_CMD = 'java'
        pk_12_file = 'sign.p12'
        jar_path = os.path.join(os.path.dirname(__file__), JAR_PATH)

        command = [
            JAVA_CMD,
            '-jar',
            jar_path,
            to_sign_file.name,
            pk_12_file,
            password
        ]
        try:
            logging.info('Probando comando de firma digital')
            subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            returncode = e.returncode
            output = e.output
            logging.error('Llamada a proceso JAVA codigo: %s' % returncode)
            logging.error('Error: %s' % output)

        p = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        res = p.communicate()
        return res[0]
