from flask import render_template, request, jsonify, session, redirect, url_for
from app import app

# Usuarios de prueba
USERS = {
    "123": '123'
}

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Usuario o contraseña incorrectos'})
    
    return render_template('login.html')

@app.route('/inicio')
def inicio():
    return render_template('index.html',)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/simple')
def simple():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('simple.html', username=session['username'])

@app.route('/compuesto')
def compuesto():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('compuesto.html', username=session['username'])

@app.route('/interes')
def interes():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('interes.html', username=session['username'])

@app.route('/anualidades')
def anualidades():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('anualidades.html', username=session['username'])

@app.route('/registro', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        username = data.get('cedula')
        password = data.get('password')

        # Validación simple
        if not username or not password:
           return jsonify({'success': False, 'error': 'Todos los campos son obligatorios'})

        if username in USERS:
            return jsonify({'success': False, 'error': 'El usuario ya existe'})

        # Registrar usuario en el diccionario temporal
        USERS[username] = password
        return jsonify({'success': True, 'message': 'Usuario registrado con éxito'})

    return render_template('registro.html')
