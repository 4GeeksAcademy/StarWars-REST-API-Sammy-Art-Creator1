"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for  # Importa Flask y herramientas para manejar solicitudes HTTP
from flask_migrate import Migrate  # Permite manejar migraciones de la base de datos
from flask_swagger import swagger  # Genera documentación de API con Swagger
from flask_cors import CORS  # Permite peticiones desde diferentes dominios (Cross-Origin Resource Sharing)
from utils import APIException, generate_sitemap  # Importa manejadores de errores y generación de sitemap
from admin import setup_admin  # Configuración del panel de administración
from models import db, User, Planet, Person, Favorite  # Importa modelos de la base de datos

app = Flask(__name__)  # Crea una instancia de Flask
app.url_map.strict_slashes = False  # Permite que las rutas sean más flexibles con o sin "/"

# Configuración de la base de datos
db_url = os.getenv("DATABASE_URL")  # Obtiene la URL de la base de datos desde las variables de entorno
if db_url is not None:
    # Asegura que el prefijo de PostgreSQL sea correcto
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    # Usa SQLite como base de datos por defecto
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactiva el rastreo de modificaciones para mejorar el rendimiento

# Inicializa la base de datos y migraciones
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)  # Habilita CORS para permitir solicitudes desde cualquier origen
setup_admin(app)  # Configura el panel de administración

# Manejo de errores
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    # Devuelve errores como respuestas JSON
    return jsonify(error.to_dict()), error.status_code

# Genera un sitemap con todas las rutas disponibles
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoint para obtener todos los usuarios
@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all()  # Obtiene todos los usuarios de la base de datos
    return jsonify([user.serialize() for user in users])  # Devuelve los usuarios en formato JSON

# Endpoint para obtener todos los personajes
@app.route('/people', methods=['GET'])
def get_people():
    people = Person.query.all()  # Obtiene todos los personajes
    return jsonify([person.serialize() for person in people])  # Devuelve los personajes en formato JSON

# Endpoint para obtener un personaje por ID
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Person.query.get(people_id)  # Busca el personaje por ID
    return jsonify(person.serialize()) if person else ('', 404)  # Devuelve el personaje si existe, o un error 404

# Endpoint para obtener todos los planetas
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()  # Obtiene todos los planetas
    return jsonify([planet.serialize() for planet in planets])  # Devuelve los planetas en formato JSON

# Endpoint para obtener un planeta por ID
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)  # Busca el planeta por ID
    return jsonify(planet.serialize()) if planet else ('', 404)  # Devuelve el planeta si existe, o un error 404

# Endpoint para obtener los favoritos de un usuario (simulando usuario con ID 1)
@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1  # Se asume que el usuario con ID 1 está autenticado
    favorites = Favorite.query.filter_by(user_id=user_id).all()  # Busca los favoritos del usuario
    return jsonify([favorite.serialize() for favorite in favorites])  # Devuelve los favoritos en formato JSON

# Endpoint para agregar un planeta a los favoritos de un usuario
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1  # Se asume que el usuario con ID 1 está autenticado
    new_favorite = Favorite(user_id=user_id, planet_id=planet_id)  # Crea un nuevo favorito con el planeta
    db.session.add(new_favorite)  # Agrega el favorito a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios
    return jsonify(new_favorite.serialize()), 201  # Devuelve el favorito creado con código 201 (creado)

# Endpoint para agregar un personaje a los favoritos de un usuario
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    user_id = 1  # Se asume que el usuario con ID 1 está autenticado
    new_favorite = Favorite(user_id=user_id, person_id=people_id)  # Crea un nuevo favorito con el personaje
    db.session.add(new_favorite)  # Agrega el favorito a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios
    return jsonify(new_favorite.serialize()), 201  # Devuelve el favorito creado con código 201 (creado)

# Endpoint para eliminar un planeta de los favoritos de un usuario
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1  # Se asume que el usuario con ID 1 está autenticado
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()  # Busca el favorito
    if favorite:
        db.session.delete(favorite)  # Elimina el favorito
        db.session.commit()  # Guarda los cambios
        return '', 204  # Devuelve un código 204 (sin contenido) indicando éxito
    return '', 404  # Devuelve un error 404 si el favorito no existe

# Endpoint para eliminar un personaje de los favoritos de un usuario
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    user_id = 1  # Se asume que el usuario con ID 1 está autenticado
    favorite = Favorite.query.filter_by(user_id=user_id, person_id=people_id).first()  # Busca el favorito
    if favorite:
        db.session.delete(favorite)  # Elimina el favorito
        db.session.commit()  # Guarda los cambios
        return '', 204  # Devuelve un código 204 (sin contenido) indicando éxito
    return '', 404  # Devuelve un error 404 si el favorito no existe

# Ejecuta la aplicación solo si el script se ejecuta directamente
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))  # Obtiene el puerto de la variable de entorno o usa 3000 por defecto
    app.run(host='0.0.0.0', port=PORT, debug=False)  # Inicia el servidor Flask en el puerto especificado
