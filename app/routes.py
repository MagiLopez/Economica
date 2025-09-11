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

# Nueva ruta para el login con Google (simplificado)
@app.route('/google-login', methods=['POST'])
def google_login():
    try:
        data = request.json
        user_name = data.get('name')  # Nombre del usuario de Google
        user_email = data.get('email')  # Email del usuario de Google
        
        # Usar el nombre o email como username para la sesión
        username = user_name if user_name else user_email.split('@')[0]
        
        # Simplemente crear la sesión sin validación adicional
        session['username'] = username
        session['google_user'] = True  # Marcar como usuario de Google
        
        return jsonify({'success': True, 'message': 'Login con Google exitoso'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': 'Error al procesar login con Google'})


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
