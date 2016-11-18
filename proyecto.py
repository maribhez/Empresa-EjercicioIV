#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, url_for, redirect
from flask import render_template
import flask_login
import flask
import os
from flask.ext import shelve
from jinja2 import Environment, PackageLoader
from flask.ext.script import Manager

env = Environment(loader=PackageLoader(__name__, 'templates'))
#
# #Para testing.
# COV = None
# if os.environ.get('FlASK_COVERAGE'):
#     import coverage
#     COV = coverage.coverage(branch=True, include='app/*')
#     COV.start()
# #Acaba testing.


app = Flask(__name__, static_url_path = "", static_folder = "")
app.secret_key = 'asecret'
app.config['SHELVE_FILENAME'] = 'shelve.db'


shelve.init_app(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass

def listarShelve():
    d = shelve.get_shelve('c')
    v = d.keys()
    for i in v:
        print (i)

    d.close()
    return v


@login_manager.user_loader
def load_user(user_id):
    d = shelve.get_shelve('c')
    user_pass = d[str(user_id)]
    if user_pass == "":
        return

    user = User()
    user.id = user_id
    return user

@app.route("/")
def hello():
    return render_template("principal.html")

@app.route("/principal")
@app.route("/principal/<name>", methods = ['POST', 'GET'])
def principal(name=None):
    if request.method == 'GET':
        lista = listarShelve()

        return render_template("principal.html", name=lista)


@app.route("/crear_empresa")
def crear_empresa():
    return render_template("creacion_empresa.html")


@app.route("/creacion_empresa", methods=['POST', 'GET'])
def accion_registro():

    if request.method == 'POST':
        empresa = request.form['nombre_empresa']
        valoracion = request.form['calificacion']
        d = shelve.get_shelve('c')
        if d.has_key(str(empresa)):
            return 'La empresa ya existe'
        else:
            d[str(empresa)] = valoracion
            d.close()
            return redirect(url_for('principal'))


@app.route("/votaciones/<empresas>", methods = ['POST', 'GET'])
@app.route("/votaciones")
def votaciones():
    d = shelve.get_shelve('c')
    empresas = d.keys()
    d.close()
    return render_template("votaciones.html")



@app.route("/valorar",  methods=['POST', 'GET'])
def valorar():

    if request.method == 'POST':
        empresa = request.form['nombre_empresa']
        valoracion = request.form['calificacion']
        d = shelve.get_shelve('c')
        if d.has_key(str(empresa)):
            d[str(empresa)] = d[str(empresa)] + valoracion
            puntos = d[str(empresa)]
            d.close()
            return 'Calificacion añadida. '
        else:
            d.close()
            return 'La empresa no está registrada.'


@app.route('/borrar')
def logout():
    flask_login.logout_user()
    current_user = flask_login.current_user
    return env.get_template('principal.html').render(current_user=current_user)

# manager = Manager(app)
# @manager.command
# def test(coverage=False):
#     """Run de unit test."""
#     if coverage and not os.environ.get('FLASK_COVERAGE'):
#         import sys
#         os.environ['FLASK_COVERAGE'] = '1'
#         os.execvp(sys.executable, [sys.executable] + sys.argv)
#     import unittest
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)
#     if COV:
#         COV.stop()
#         COV.save()
#         print('Resumen')
#         COV.report()
#         basedir = os.path.abspath(os.path.dirname(__file__))
#         covdir = os.path.join(basedir, 'tmp/coverage')
#         COV.html_report(directory=covdir)
#         print('HTML Version: file://%s/index.html' % covdir)
#         COV.erase()
#






if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
