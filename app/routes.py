from flask import render_template, request, jsonify, session, redirect, url_for
import requests  # Para hacer peticiones a FastAPI
from app import app

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        cedula = data.get('username')
        password = data.get('password')
        
        try:
            # Hacer petición a FastAPI para validar login
            fastapi_response = requests.post(
                "http://127.0.0.1:5000/validar_login",
                json={"cedula": cedula, "password": password},
                timeout=5
            )
            
            if fastapi_response.status_code == 200:
                result = fastapi_response.json()
                if result.get('success'):
                    # Buscar el usuario en la API para obtener su nombre
                    usuarios_response = requests.get("http://127.0.0.1:5000/usuarios")
                    if usuarios_response.status_code == 200:
                        usuarios_data = usuarios_response.json()
                        usuarios = usuarios_data.get('usuarios', [])
                        
                        # Buscar el usuario específico
                        usuario_encontrado = None
                        for usuario in usuarios:
                            if usuario.get('cedula') == cedula:
                                usuario_encontrado = usuario
                                break
                        
                        if usuario_encontrado:
                            session['username'] = usuario_encontrado.get('nombre', f'Usuario {cedula}')
                            return jsonify({'success': True, 'message': f"Bienvenido {session['username']}"})
                    
                    # Si no se encuentra el nombre, usar cédula
                    session['username'] = f'Usuario {cedula}'
                    return jsonify({'success': True, 'message': f"Bienvenido {session['username']}"})
            
            # Si FastAPI devuelve error
            if fastapi_response.status_code == 404:
                return jsonify({'success': False, 'error': 'Usuario no encontrado'})
            else:
                return jsonify({'success': False, 'error': 'Credenciales inválidas'})
                
        except requests.RequestException as e:
            print(f"Error conectando con FastAPI: {e}")
            return jsonify({'success': False, 'error': 'Error de conexión con el servidor'})
    
    return render_template('login.html')

# Ruta auxiliar para crear sesión (si usas la Opción 1)
@app.route('/create-session', methods=['POST'])
def create_session():
    try:
        data = request.json
        cedula = data.get('cedula')
        
        # Obtener información del usuario desde FastAPI
        usuarios_response = requests.get("http://127.0.0.1:5000/usuarios")
        if usuarios_response.status_code == 200:
            usuarios_data = usuarios_response.json()
            usuarios = usuarios_data.get('usuarios', [])
            
            for usuario in usuarios:
                if usuario.get('cedula') == cedula:
                    session['username'] = usuario.get('nombre', f'Usuario {cedula}')
                    return jsonify({'success': True})
        
        session['username'] = f'Usuario {cedula}'
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/google-login', methods=['POST'])
def google_login():
    try:
        data = request.json
        user_name = data.get('name')
        user_email = data.get('email')
        
        username = user_name if user_name else user_email.split('@')[0]
        session['username'] = username
        session['google_user'] = True
        
        return jsonify({'success': True, 'message': 'Login con Google exitoso'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': 'Error al procesar login con Google'})

@app.route('/inicio')
def inicio():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('google_user', None)
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

@app.route('/registro')
def register():
    return render_template('registro.html')

@app.route('/gradiente')
def gradiente():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('gradiente.html', username=session['username'])

@app.route("/amortizacion")
def amortizacion():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("amortizacion.html")


@app.route("/retorno")
def retorno():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("retorno.html")
@app.route("/capitalizacion")
def capitalizacion():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("capitalizacion.html")
