from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = '230624Mili'  # Clave principal de seguridad

# Ruta principal: pantalla de inicio de sesión
@app.route('/')
def login():
    return render_template('inicio de sesión.html')

# Ruta POST del login
@app.route('/acceso', methods=['POST'])
def acceso():
    clave = request.form.get('clave')
    
    if clave == '230624Mili':
        session['autenticado'] = True
        return redirect(url_for('panel_maik'))
    else:
        return 'Acceso denegado. Clave incorrecta.'

# Ruta del panel principal de Maik
@app.route('/maik')
def panel_maik():
    if not session.get('autenticado'):
        return redirect(url_for('login'))
    return render_template('maik.html')

# Logout
@app.route('/salir')
def salir():
    session.clear()
    return redirect(url_for('login'))

# Ejecución local
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import openai  # Asegurate de tenerlo en tu requirements.txt

app = Flask(__name__)

# Clave secreta de OpenAI (mejor usar variable de entorno en producción)
openai.api_key = "sk-tu_clave_aqui"

@app.route('/')
def home():
    return "Maik está activo y esperando órdenes, Yeis."

@app.route('/maik', methods=['POST'])
def chat_with_maik():
    data = request.get_json()
    user_input = data.get("mensaje")

    if not user_input:
        return jsonify({"error": "Mensaje no recibido"}), 400

    try:
        # Llamada a OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # o "gpt-4" si tenés acceso
            messages=[
                {"role": "system", "content": "Sos Maik, el asistente leal y poderoso de Yeis."},
                {"role": "user", "content": user_input}
            ]
        )
        respuesta = response.choices[0].message.content
        return jsonify({"respuesta": respuesta})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
