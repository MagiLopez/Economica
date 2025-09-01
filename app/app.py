from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import math

app = Flask(__name__)
app.secret_key = 'finly_secret_key_2024'  # Cambia esto por una clave más segura

# Usuarios de prueba (en producción usar base de datos)
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

@app.route('/calculate_simple', methods=['POST'])
def calculate_simple():
    if 'username' not in session:
        return jsonify({'error': 'No autorizado'})
    
    try:
        data = request.json
        
        # Obtener valores del formulario
        P = data.get('capital')  # Capital inicial
        i = data.get('tasa')     # Tasa de interés (%)
        n = data.get('tiempo')   # Tiempo en años
        M = data.get('monto')    # Monto futuro
        
        # Convertir valores a float si existen, sino None
        P = float(P) if P and P != '' else None
        i = float(i) if i and i != '' else None
        n = float(n) if n and n != '' else None
        M = float(M) if M and M != '' else None
        
        # Contar campos llenos
        campos_llenos = sum(x is not None for x in [P, i, n, M])
        
        if campos_llenos < 3:
            return jsonify({'error': 'Debes llenar al menos 3 campos para calcular el cuarto'})
        
        if campos_llenos == 4:
            return jsonify({'error': 'Deja un campo vacío para calcularlo'})
        
        result = {}
        
        # Detectar automáticamente qué calcular
        if P is None:  # Calcular Capital Inicial
            if i and n and M:
                i_decimal = i / 100
                P_calculado = M / (1 + i_decimal * n)
                interes = M - P_calculado
                result = {
                    'valor_calculado': round(P_calculado, 2),
                    'interes_ganado': round(interes, 2),
                    'formula': f'P = M / (1 + i × n) = {M} / (1 + {i}% × {n})',
                    'campo_calculado': 'Capital Inicial (P)'
                }
        
        elif i is None:  # Calcular Tasa de Interés
            if P and M and n and P != 0 and n != 0:
                i_calculado = ((M / P) - 1) / n
                i_porcentaje = i_calculado * 100
                interes = M - P
                result = {
                    'valor_calculado': round(i_porcentaje, 4),
                    'interes_ganado': round(interes, 2),
                    'formula': f'i = ((M/P) - 1) / n = (({M}/{P}) - 1) / {n}',
                    'campo_calculado': 'Tasa de Interés (i%)'
                }
        
        elif n is None:  # Calcular Tiempo
            if P and M and i and P != 0:
                i_decimal = i / 100
                if i_decimal != 0:
                    n_calculado = ((M / P) - 1) / i_decimal
                    interes = M - P
                    result = {
                        'valor_calculado': round(n_calculado, 4),
                        'interes_ganado': round(interes, 2),
                        'formula': f'n = ((M/P) - 1) / i = (({M}/{P}) - 1) / {i}%',
                        'campo_calculado': 'Tiempo (n años)'
                    }
                else:
                    return jsonify({'error': 'La tasa de interés no puede ser 0'})
        
        elif M is None:  # Calcular Monto Futuro
            if P and i and n:
                i_decimal = i / 100
                M_calculado = P * (1 + i_decimal * n)
                interes = M_calculado - P
                result = {
                    'valor_calculado': round(M_calculado, 2),
                    'interes_ganado': round(interes, 2),
                    'formula': f'M = P × (1 + i × n) = {P} × (1 + {i}% × {n})',
                    'campo_calculado': 'Monto Futuro (M)'
                }
        
        if not result:
            return jsonify({'error': 'Error en el cálculo. Verifica los valores ingresados.'})
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Error en el cálculo: {str(e)}'})

@app.route('/calculate_compuesto', methods=['POST'])
def calculate_compuesto():
    if 'username' not in session:
        return jsonify({'error': 'No autorizado'})
    
    try:
        data = request.json
        
        # Obtener valores del formulario
        P = data.get('capital')  # Capital inicial
        i = data.get('tasa')     # Tasa de interés (%)
        n = data.get('tiempo')   # Tiempo en años
        M = data.get('monto')    # Monto futuro
        
        # Convertir valores a float si existen, sino None
        P = float(P) if P and P != '' else None
        i = float(i) if i and i != '' else None
        n = float(n) if n and n != '' else None
        M = float(M) if M and M != '' else None
        
        # Contar campos llenos
        campos_llenos = sum(x is not None for x in [P, i, n, M])
        
        if campos_llenos < 3:
            return jsonify({'error': 'Debes llenar al menos 3 campos para calcular el cuarto'})
        
        if campos_llenos == 4:
            return jsonify({'error': 'Deja un campo vacío para calcularlo'})
        
        result = {}
        
        # Detectar automáticamente qué calcular
        if P is None:  # Calcular Capital Inicial
            if i and n and M:
                i_decimal = i / 100
                P_calculado = M / ((1 + i_decimal) ** n)
                interes = M - P_calculado
                result = {
                    'valor_calculado': round(P_calculado, 2),
                    'interes_ganado': round(interes, 2),
                    'formula': f'P = M / (1 + i)ⁿ = {M} / (1 + {i}%)^{n}',
                    'campo_calculado': 'Capital Inicial (P)'
                }
        
        elif i is None:  # Calcular Tasa de Interés
            if P and M and n and P != 0 and n != 0:
                i_calculado = ((M / P) ** (1/n)) - 1
                i_porcentaje = i_calculado * 100
                interes = M - P
                result = {
                    'valor_calculado': round(i_porcentaje, 4),
                    'interes_ganado': round(interes, 2),
                    'formula': f'i = (M/P)^(1/n) - 1 = ({M}/{P})^(1/{n}) - 1',
                    'campo_calculado': 'Tasa de Interés (i%)'
                }
        
        elif n is None:  # Calcular Tiempo
            if P and M and i and P != 0:
                i_decimal = i / 100
                if (1 + i_decimal) > 0 and M > P:
                    n_calculado = math.log(M / P) / math.log(1 + i_decimal)
                    interes = M - P
                    result = {
                        'valor_calculado': round(n_calculado, 4),
                        'interes_ganado': round(interes, 2),
                        'formula': f'n = ln(M/P) / ln(1 + i) = ln({M}/{P}) / ln(1 + {i}%)',
                        'campo_calculado': 'Tiempo (n años)'
                    }
                else:
                    return jsonify({'error': 'El monto debe ser mayor al capital y la tasa mayor a -100%'})
        
        elif M is None:  # Calcular Monto Futuro
            if P and i and n:
                i_decimal = i / 100
                M_calculado = P * ((1 + i_decimal) ** n)
                interes = M_calculado - P
                result = {
                    'valor_calculado': round(M_calculado, 2),
                    'interes_ganado': round(interes, 2),
                    'formula': f'M = P × (1 + i)ⁿ = {P} × (1 + {i}%)^{n}',
                    'campo_calculado': 'Monto Futuro (M)'
                }
        
        if not result:
            return jsonify({'error': 'Error en el cálculo. Verifica los valores ingresados.'})
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Error en el cálculo: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)