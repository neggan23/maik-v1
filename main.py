from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import openai
import datetime

app = Flask(__name__)
app.secret_key = '230624Mili'  # Clave de seguridad principal

# Reemplazá con tu clave real de OpenAI
openai.api_key = 'TU_API_KEY'

# Ruta de inicio de sesión
@app.route('/')
def login():
    return render_template('inicio de sesión.html')

# Ruta de verificación de clave
@app.route('/acceso', methods=['POST'])
def acceso():
    clave = request.form.get('clave')
    if clave == '230624Mili':
        session['autenticado'] = True
        return redirect(url_for('panel_maik'))
    else:
        return 'Acceso denegado. Clave incorrecta.'

# Panel inteligente de Maik
@app.route('/maik')
def panel_maik():
    if not session.get('autenticado'):
        return redirect(url_for('login'))
    return render_template('maik.html')

# Ruta para cerrar sesión
@app.route('/salir')
def salir():
    session.clear()
    return redirect(url_for('login'))

# API principal de Maik (motor apiV1 con GPT-4 Turbo)
@app.route('/apiV1', methods=['POST'])
def apiV1():
    if not session.get('autenticado'):
        return jsonify({'error': 'No autorizado'}), 403

    data = request.json
    prompt = data.get('mensaje')
    user_id = session.get('usuario', 'yeis')  # default para pruebas

    try:
        # Interacción con el modelo
        respuesta = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        texto = respuesta.choices[0].message.content

        # [FUTURO] Guardar en memoria Spanner
        # guardar_interaccion(user_id, prompt, texto)

        return jsonify({'respuesta': texto})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Punto de entrada principal
if __name__ == '__main__':
    app.run(debug=True)
