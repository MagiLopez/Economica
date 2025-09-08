from flask import render_template, request, jsonify, session, redirect, url_for
from app import app

# Usuarios de prueba
USERS = {
    'admin': 'admin123',
    'user': 'user123',
    'finly': 'finly2024'
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
