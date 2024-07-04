from flask import Flask, request, jsonify
import sqlite3
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

# Crear la base de datos y la tabla de usuarios si no existen
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            registro TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Ruta para registrar un nuevo usuario
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nombre = data['nombre']
    apellido = data['apellido']
    registro = data['registro']
    password = data['password']
    password_hash = pbkdf2_sha256.hash(password)

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (nombre, apellido, registro, password_hash) VALUES (?, ?, ?, ?)', (nombre, apellido, registro, password_hash))
    conn.commit()
    conn.close()

    return jsonify(message='Usuario registrado exitosamente'), 201

# Ruta para validar un usuario
@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    nombre = data['nombre']
    apellido = data['apellido']
    registro = data['registro']
    password = data['password']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE nombre = ? AND apellido = ? AND registro = ?', (nombre, apellido, registro))
    user = cursor.fetchone()
    conn.close()

    if user and pbkdf2_sha256.verify(password, user[0]):
        return jsonify(message='Usuario validado exitosamente'), 200
    else:
        return jsonify(message='Nombre, apellido, registro o contraseña incorrectos'), 401

if __name__ == '__main__':
    init_db()
    app.run(port=8500)
