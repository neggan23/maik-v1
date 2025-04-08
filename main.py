from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import openai
import datetime
import uuid

from google.cloud import spanner

# CONFIGURACIÓN DE FLASK
app = Flask(__name__)
app.secret_key = '230624Mili'  # Clave de seguridad principal

# CONFIGURACIÓN DE OPENAI
openai.api_key = 'TU_API_KEY'  # Reemplazar con tu clave real

# CONFIGURACIÓN DE SPANNER
INSTANCE_ID = 'maik-instance'
DATABASE_ID = 'maik-db'
spanner_client = spanner.Client()
instance = spanner_client.instance(INSTANCE_ID)
database = instance.database(DATABASE_ID)

# RUTAS DE AUTENTICACIÓN
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

# API PRINCIPAL DE MAIK (INTELIGENCIA)
@app.route('/apiV1', methods=['POST'])
def apiV1():
    if not session.get('autenticado'):
        return jsonify({'error': 'No autorizado'}), 403

    data = request.json
    prompt = data.get('mensaje')
    user_id = session.get('usuario', 'yeis')  # Por defecto "yeis"

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        texto = respuesta.choices[0].message.content

        guardar_interaccion(user_id, prompt, texto)
        return jsonify({'respuesta': texto})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GUARDAR EN SPANNER
def guardar_interaccion(usuario, mensaje, respuesta):
    with database.batch() as batch:
        batch.insert(
            table='Interacciones',
            columns=('id', 'usuario', 'mensaje', 'respuesta', 'timestamp'),
            values=[(
                str(uuid.uuid4()),
                usuario,
                mensaje,
                respuesta,
                spanner.COMMIT_TIMESTAMP
            )]
        )

# EJECUCIÓN
if __name__ == '__main__':
    app.run(debug=True)
