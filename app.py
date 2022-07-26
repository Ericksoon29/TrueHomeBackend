from flask import Flask, request, jsonify
from flask_pymongo import MongoClient
from bson import ObjectId, errors
import sys
import json
from bson.json_util import dumps

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/') # Have to specify the host & port
db = client.TrueHome
collection = db.User
collectionPeliculas = db.Peliculas

@app.route('/')
def healtCheck():
    return "healtCheck", 200

@app.route('/crearUsuario', methods=['POST'])
def postUsuarios():
    if not request.json:
        return "Por favor ingresa datos en el body", 400

    usuarios = request.json
    id = collection.insert_one(usuarios).inserted_id

    return jsonify(str(id)), 201

@app.route('/obtenerUsuario/<nombre>', methods=['GET'])
def obtenerUsuarioPorNombre(nombre):
    try:
        result = collection.find_one({'nombre': nombre})
    except errors.InvalidId:
        return "Ocurrio un error al tratar de buscar el usuario", 400

    if not result:
        return "Nombre no se encuentra en la base de datos, Intente mas tarde", 404

    return jsonify({'nombre': result['nombre']}), 200


@app.route('/crearPelicula', methods=['POST'])
def postPeliculas():
    if not request.json:
        return "Por favor ingresa datos en el body", 400

    peliculas = request.json
    id = collectionPeliculas.insert_one(peliculas).inserted_id

    return jsonify(str(id)), 201


@app.route('/obtenerPeliculas', methods=['GET'])
def getPeliculas():
    try:
        
        result = collectionPeliculas.find({})
    except errors.InvalidId:
        return "Ocurrio un error al tratar de buscar la pelicula", 400

    if not result:
        return "La pelicula no se encuentra en la base de datos, Intente mas tarde", 404

    return dumps(result), 200


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",  port=3500)