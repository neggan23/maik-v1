from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import requests

app = Flask(__name__)
app.secret_key = '230624Mili'  # Clave principal de seguridad

# ======= CONFIGURACIÓN APIv1 MAIK ========
API_V1_URL = "http://localhost:8000/maikv1/preguntar"  # Cambialo si lo hosteás en otro lado

# ======= PANTALLA DE INICIO DE SESIÓN ========
@app.route('/')
def login():
    return render_template('inicio de sesión.html')

# ======= PROCESO DE ACCESO ========
@app.route('/acceso', methods=['POST'])
def acceso():
    clave = request.form.get('clave')
    
    if clave == '230624Mili':
        session['autenticado'] = True
        return redirect(url_for('panel_maik'))
    else:
        return 'Acceso denegado. Clave incorrecta.'

# ======= PANEL PRINCIPAL DE MAIK ========
@app.route('/maik')
def panel_maik():
    if not session.get('autenticado'):
        return redirect(url_for('login'))
    return render_template('maik.html')

# ======= CERRAR SESIÓN ========
@app.route('/salir')
def salir():
    session.clear()
    return redirect(url_for('login'))

# ======= INTEGRACIÓN CON MOTOR apiV1 DE MAIK ========
@app.route('/preguntar', methods=['POST'])
def preguntar():
    data = request.json
    prompt = data.get('mensaje')

    try:
        respuesta_api = requests.post(API_V1_URL, json={"mensaje": prompt})
        respuesta_api.raise_for_status()
        contenido = respuesta_api.json()
        return jsonify({'respuesta': contenido.get("respuesta", "Sin respuesta desde el motor apiV1")})
    except Exception as e:
        return jsonify({'respuesta': f'Error al consultar motor Maik: {str(e)}'})

# ======= INICIAR FLASK ========
if __name__ == '__main__':
    app.run(debug=True)
