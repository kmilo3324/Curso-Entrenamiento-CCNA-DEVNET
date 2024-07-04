from flask import Flask, request, jsonify
import hashlib
import sqlite3

app = Flask(__name__)

# Función para conectar y crear la base de datos SQLite
def crearbd():
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()

    # Crear tabla si no existe
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (nombre TEXT, apellido TEXT, usuario TEXT, hash_contrasena TEXT)''')

    conn.commit()
    conn.close()

# Función para generar hash de contraseña usando hashlib
def generarhash(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

# Función para registrar un nuevo usuario
@app.route('/registrar', methods=['POST'])
def registrarusuario():
    datos = request.get_json()
    nombre = datos['nombre']
    apellido = datos['apellido']
    usuario = datos['usuario']
    contrasena = datos['contrasena']

    hash_contrasena = generarhash(contrasena)

    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()

    # Insertar usuario en la base de datos
    c.execute("INSERT INTO usuarios (nombre, apellido, usuario, hash_contrasena) VALUES (?, ?, ?, ?)",
              (nombre, apellido, usuario, hash_contrasena))

    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Usuario registrado exitosamente"})

# Función para validar el usuario
@app.route('/validar', methods=['POST'])
def validar_usuario():
    datos = request.get_json()
    nombre = datos['nombre']
    apellido = datos['apellido']

    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()

    # Buscar usuario en la base de datos
    c.execute("SELECT * FROM usuarios WHERE nombre=? AND apellido=?", (nombre, apellido))
    usuario = c.fetchone()

    if usuario:
        return jsonify({"mensaje": f"Bienvenido, {nombre} {apellido}!"})
    else:
        return jsonify({"mensaje": "Usuario no encontrado"})

    conn.close()

if __name__ == '__main__':
    crearbd()
    app.run(port=8500)
