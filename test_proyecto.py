import unittest2 as unittest
import proyecto
from flask import Flask, current_app, request
from flask.ext import shelve
import flask_login
import flask_testing
import pytest

from jinja2 import Environment, PackageLoader
# from test import test_support

app = Flask(__name__)

class test_proyecto(unittest.TestCase):


    def setUp(self):
        app.config['TESTING'] = True
        app.config['SHELVE_FILENAME'] = 'shelve.db'
        shelve.init_app(app)
        return app


    def test_creacion(self):
          with app.app_context():
            import shelve
            nombre_empresa = 'Empresa Prueba'
            calificacion = 9
            d = shelve.open('shelve.db')
            d[str(nombre_empresa)] = calificacion
            self.assertEqual(d[str(nombre_empresa)],calificacion)



    def main():
        unittest.main()

    if __name__ == '__main__':
        unittest.main()
