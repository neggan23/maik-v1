from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import openai

app = Flask(__name__)
app.secret_key = '230624Mili'  # Clave principal

# Clave de la API (reemplazala con tu clave real de OpenAI)
openai.api_key = 'TU_API_KEY'

# Rutas base
@app.route('/')
def login():
    return render_template('inicio de sesión.html')

@app.route('/acceso', methods=['POST'])
def acceso():
    clave = request.form.get('clave')
    
    if clave == '230624Mili':
        session['autenticado'] = True
        return redirect(url_for('panel_maik'))
    else:
        return 'Acceso denegado. Clave incorrecta.'

@app.route('/maik')
def panel_maik():
    if not session.get('autenticado'):
        return redirect(url_for('login'))
    return render_template('maik.html')

@app.route('/salir')
def salir():
    session.clear()
    return redirect(url_for('login'))

# Motor apiV1 con GPT-4 Turbo
@app.route('/apiV1', methods=['POST'])
def apiV1():
    data = request.json
    prompt = data.get('mensaje')

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        texto = respuesta.choices[0].message.content
        return jsonify({'respuesta': texto})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ejecutar app
if __name__ == '__main__':
    app.run(debug=True)
