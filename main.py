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
