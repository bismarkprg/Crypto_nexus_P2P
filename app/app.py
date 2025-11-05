from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cryptonexus'

mysql = MySQL(app)

@app.route('/')
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form.get('repeat_password')

        # Validación de contraseñas
        if password != repeat_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('register'))

        if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            flash('La contraseña debe tener al menos 8 caracteres, incluir letras y números.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO usuarios (nombre, email, password)
                VALUES (%s, %s, %s)
            """, (username, email, hashed_password))
            mysql.connection.commit()
            session['user_id'] = cur.lastrowid
            cur.close()
            return redirect(url_for('register_form'))
        except Exception as e:
            flash(f'Error al registrar: {str(e)}', 'danger')
            return render_template('register.html', error_message=f'Error al registrar: {str(e)}')

    return render_template('register.html')


@app.route('/register_form', methods=['GET', 'POST'])
def register_form():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('register'))

        # Obtener datos del formulario
        nombre_completo = request.form['nombre_completo']
        fecha_nacimiento = request.form['fecha_nacimiento']
        pais_residencia = request.form['pais_residencia']
        ciudad_residencia = request.form['ciudad_residencia']
        nacionalidad = request.form['nacionalidad']
        tipo_documento = request.form['tipo_documento']
        documento_identidad = request.form['documento_identidad']
        numero_telefono = request.form['numero_telefono']

        # Actualizar el usuario
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE usuarios SET
                nombre_completo=%s,
                fecha_nacimiento=%s,
                pais_residencia=%s,
                ciudad_residencia=%s,
                nacionalidad=%s,
                tipo_documento=%s,
                documento_identidad=%s,
                numero_telefono=%s
            WHERE id_usuario=%s
        """, (nombre_completo, fecha_nacimiento, pais_residencia, ciudad_residencia,
              nacionalidad, tipo_documento, documento_identidad, numero_telefono, user_id))
        mysql.connection.commit()
        # Obtener el campo 'nombre' del usuario
        cur.execute("SELECT nombre FROM usuarios WHERE id_usuario = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        return redirect(url_for('login', nombre=user[0]))

    # Obtener datos del usuario para mostrar el nombre
    user_id = session.get('user_id')
    cur = mysql.connection.cursor()
    cur.execute("SELECT nombre FROM usuarios WHERE id_usuario = %s", (user_id,))
    user = cur.fetchone()
    cur.close()

    return render_template('register_form.html', current_user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_usuario, nombre, password FROM usuarios WHERE nombre = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            return redirect(url_for("dashboard"))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    nombre = session["user_id"]
    return render_template('dashboard.html', nombre=nombre)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("/"))

if __name__ == '__main__':
    app.run(debug=True)

