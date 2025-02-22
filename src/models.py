from flask_sqlalchemy import SQLAlchemy

# Inicializa la base de datos con SQLAlchemy
db = SQLAlchemy()

# Modelo de Usuario
class User(db.Model):
    # Define las columnas de la tabla 'user'
    id = db.Column(db.Integer, primary_key=True)  # Identificador único (clave primaria)
    username = db.Column(db.String, unique=True, nullable=False)  # Nombre de usuario, único y obligatorio
    email = db.Column(db.String, unique=True, nullable=False)  # Email, único y obligatorio
    password = db.Column(db.String, unique=False, nullable=False)  # Contraseña, obligatoria
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)  # Indica si el usuario está activo

    # Relación con la tabla 'Favorite' (un usuario puede tener muchos favoritos)
    favorites = db.relationship("Favorite", backref="user", lazy=True)

    def __repr__(self):
        # Representación del objeto cuando se imprime
        return '<User %r>' % self.username

    def serialize(self):
        # Devuelve un diccionario con los datos serializados del usuario (sin la contraseña por seguridad)
        return {
            "id": self.id,
            "username": self.username,
        }

# Modelo de Planeta
class Planet(db.Model):
    # Define las columnas de la tabla 'planet'
    id = db.Column(db.Integer, primary_key=True)  # Identificador único (clave primaria)
    name = db.Column(db.String, nullable=False)  # Nombre del planeta, obligatorio
    climate = db.Column(db.String, nullable=False)  # Clima del planeta, obligatorio
    diameter = db.Column(db.String, nullable=False)  # Diámetro del planeta, obligatorio
    population = db.Column(db.String, nullable=False)  # Población del planeta, obligatorio

    # Relación con la tabla 'Favorite' (un planeta puede estar en varios favoritos)
    favorites = db.relationship('Favorite', backref='planet', lazy=True)

    def __repr__(self):
        # Representación del objeto cuando se imprime
        return '<Planet %r>' % self.name

    def serialize(self):
        # Devuelve un diccionario con los datos serializados del planeta
        return {
            "id": self.id,
            "name": self.name,
            "Climate": self.climate,
            "Diamater": self.diameter,
            "Population": self.population
        }

# Modelo de Personaje
class Person(db.Model):
    # Define las columnas de la tabla 'person'
    id = db.Column(db.Integer, primary_key=True)  # Identificador único (clave primaria)
    name = db.Column(db.String, nullable=False)  # Nombre del personaje, obligatorio
    height = db.Column(db.String, nullable=False)  # Altura del personaje, obligatoria
    mass = db.Column(db.String, nullable=False)  # Peso del personaje, obligatorio
    hair_color = db.Column(db.String, nullable=False)  # Color de cabello del personaje, obligatorio

    # Relación con la tabla 'Favorite' (un personaje puede estar en varios favoritos)
    favorites = db.relationship('Favorite', backref='person', lazy=True)

    def __repr__(self):
        # Representación del objeto cuando se imprime
        return '<Person %r>' % self.name

    def serialize(self):
        # Devuelve un diccionario con los datos serializados del personaje
        return {
            "id": self.id,
            "name": self.name,
            "Height": self.height,
            "Mass": self.mass,
            "Hair Color": self.hair_color
        }

# Modelo de Favoritos
class Favorite(db.Model):
    # Define las columnas de la tabla 'favorite'
    id = db.Column(db.Integer, primary_key=True)  # Identificador único (clave primaria)

    # Llaves foráneas para relacionar favoritos con usuario, planeta o personaje
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Relación con User (obligatoria)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)  # Relación con Planet (opcional)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)  # Relación con Person (opcional)

    def __repr__(self):
        # Representación del objeto cuando se imprime
        return '<Favorite %r>' % self.id

    def serialize(self):
        # Devuelve un diccionario con los datos serializados del favorito
        return {
            "id": self.id,
            "user_id": self.user_id,
            "person_id": self.person_id,
            "planet_id": self.planet_id
        }
