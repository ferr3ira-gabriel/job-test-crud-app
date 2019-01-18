#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Flask, jsonify, request

from flask_mysqldb import MySQL

from flask_selfdoc import Autodoc

import logging

import os

import unicodedata

app = Flask(__name__)
auto = Autodoc(app)

app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']

mysql = MySQL(app)

logging.basicConfig(filename='crud-app.log', level=logging.DEBUG, format='%(asctime)s level=%(levelname)s message=%(message)s')


@app.route('/', methods=['GET'])
@auto.doc()
def index():
    return "Crud App: A simple CRUD app to save deploys events! check /help to learn how to use this application - GuiaBolso"


@app.route('/add', methods=['POST'])
@auto.doc()
def insert():
    """
    POST: Salva um evento na base de dados de acordo com o JSON passado junto com a requisicao.
    Exemplo: curl --header "Content-Type: application/json" -XPOST -d \
    '{
        "componente": "App-Z",
        "id": 3,
        "responsavel": "Gabriel Ferreira",
        "status": "Updated",
        "versao": "1.0"
    }' \
    http://localhost:5000/add
    """
    try:
        jsoninfo = request.get_json()
        jsoninfo['data'] = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO deploy_infos (id, componente, versao, responsavel, status, data) VALUES (%(id)s, %(componente)s, %(versao)s, %(responsavel)s, %(status)s, %(data)s)", (jsoninfo))
        mysql.connection.commit()
        logging.info('A new deploy info saved.')
        return ("A new deploy info saved.")
    except Exception:
        logging.error('MySQL connection is NOT OK!')
        return jsonify({"mysql": "down"})


@app.route('/list', methods=['GET'])
@auto.doc()
def list():
    """
    GET: Mostra todos os eventos salvos na base de dados
    Exemplo: curl -X "GET" http://localhost:5000/list
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM deploy_infos")
    data = cur.fetchall()
    datalist = []
    if data is not None:
        for item in data:
            datatempobj = {
                'id': item[0],
                'componente': item[1],
                'versao': item[2],
                'responsavel': item[3],
                'status': item[4],
                'data': item[5]
            }
            datalist.append(datatempobj)
        return jsonify(datalist)


@app.route('/list/<id>', methods=['GET'])
@auto.doc()
def list_id(id):
    """
    GET: Busca um evento evento no banco com base no ID passado na URI.
    Exemplo: curl -X "GET" http://localhost:5000/list/4
    """
    try:
        unicodedata.numeric(id)
        cur = mysql.connection.cursor()
        query = """SELECT * FROM deploy_infos where id=%s"""
        cur.execute(query, (id, ))
        data = cur.fetchall()
        datalist = []
        if data is not None:
            for item in data:
                datatempobj = {
                    'id': item[0],
                    'componente': item[1],
                    'versao': item[2],
                    'responsavel': item[3],
                    'status': item[4],
                    'data': item[5]
                }
                datalist.append(datatempobj)
            return jsonify(datalist)
    except:
        logging.error('The ID number must be int!')
        return ('The ID number must be int!')


@app.route('/delete/<id>', methods=['DELETE'])
@auto.doc()
def delete(id):
    """
    DELETE: Remove um evento do banco com base no ID passado na URI.
    Exemplo: curl -X "DELETE" http://localhost:5000/delete/
    """
    try:
        unicodedata.numeric(id)
        cur = mysql.connection.cursor()
        query = """DELETE FROM deploy_infos where id=%s"""
        cur.execute(query, (id, ))
        mysql.connection.commit()
        logging.info('The deploy with ID %s was deleted sucessfuly.' % id)
        return ('The deploy with' + id + ' was deleted sucessfuly.')
    except:
        logging.error('The ID number must be int!')
        return ('The ID number must be int!')


@app.route('/status')
@auto.doc()
def healthcheck():
    """
    GET: Retorna se a conexao com os componentes esta OK.
    Exemplo: curl -XGET http://localhost:5000:port/status
    """
    try:
        cur = mysql.connection.cursor()
        logging.info('MySQL connection is OK!')
        return jsonify({"mysql": "up"})
    except Exception:
        logging.error('MySQL connection is NOT OK!')
        return jsonify({"mysql": "down"})


@app.route('/help')
@auto.doc()
def documentation():
    return auto.html()


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
