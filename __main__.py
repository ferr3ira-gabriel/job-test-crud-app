#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_selfdoc import Autodoc
from markupsafe import Markup, escape
import logging
import os
import unicodedata

app = Flask(__name__)
auto = Autodoc(app)

app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']
app.config['MYSQL_SSL'] = {'ssl': {'ssl_version': 'PROTOCOL_TLSv1_2'}}

mysql = MySQL(app)

logging.basicConfig(filename='crud-app.log', level=logging.DEBUG, format='%(asctime)s level=%(levelname)s message=%(message)s')


@app.route('/', methods=['GET'])
@auto.doc()
def index():
    return "Crud App: A simple CRUD app to save deploys events! check /help to learn how to use this application"


@app.route('/add', methods=['POST'])
@auto.doc()
def insert():
    """
    POST: Saves an event in the database according to the JSON passed along with the request
    Example: curl --header "Content-Type: application/json" -XPOST -d \
    '{
        "component": "App-Z",
        "id": 3,
        "owner": "Gabriel Ferreira",
        "status": "Updated",
        "version": "1.0"
    }' \
    http://localhost:5000/add
    """
    try:
        jsoninfo = request.get_json()
        jsoninfo['data'] = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO deploy_infos (id, component, version, owner, status, data) VALUES (%(id)s, %(component)s, %(version)s, %(owner)s, %(status)s, %(data)s)", (jsoninfo))
        mysql.connection.commit()
        logging.info('A new deploy info saved.')
        return jsonify({"message": "A new deploy info saved."}), 201
    except Exception as e:
        logging.error(f"MySQL connection error: {e}")

        # Return error message with HTTP status code 500
        return jsonify({"error": "Failed to save deploy info. Please try again later."}), 500

@app.route('/list', methods=['GET'])
@auto.doc()
def list():
    """
    GET: Show all events saved in the database
    Example: curl -X "GET" http://localhost:5000/list
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM deploy_infos")
    data = cur.fetchall()
    datalist = []
    if data is not None:
        for item in data:
            datatempobj = {
                'id': item[0],
                'component': item[1],
                'version': item[2],
                'owner': item[3],
                'status': item[4],
                'data': item[5]
            }
            datalist.append(datatempobj)
        return jsonify(datalist)


@app.route('/list/<id>', methods=['GET'])
@auto.doc()
def list_id(id):
    """
    GET: Searches for an event in the database based on the ID passed in the URI
    Example: curl -X "GET" http://localhost:5000/list/4
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
                    'component': item[1],
                    'version': item[2],
                    'owner': item[3],
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
    DELETE: Removes an event from the database based on the ID passed in the URI
    Example: curl -X "DELETE" http://localhost:5000/delete/
    """
    try:
        unicodedata.numeric(id)
        cur = mysql.connection.cursor()
        query = """DELETE FROM deploy_infos where id=%s"""
        cur.execute(query, (id, ))
        mysql.connection.commit()
        logging.info('The deploy with ID %s was deleted sucessfuly.' % id)
        return ('The deploy with ' + escape(id) + ' was deleted sucessfuly.')  # Escape the user input using Markup.escape()
    except:
        logging.error('The ID number must be int!')
        return ('The ID number must be int!')


@app.route('/status')
@auto.doc()
def healthcheck():
    """
    GET: Returns whether the connection to the components is OK
    Example: curl -XGET http://localhost:5000:port/status
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
