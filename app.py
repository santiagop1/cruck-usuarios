from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
db = sqlite3.connect('data.db', check_same_thread=False)

# Rutas
@app.route('/', methods=['GET']) # / significa la ruta raiz
def index():
    return render_template('index.html')

@app.route('/saludo/<nombre>/<int:edad>') # Nombre
def saludar(nombre, edad):
    numeros = [1,2,3,4,5,6,7,8,9]
    return render_template('saludo.html', name=nombre, age=edad, numbers=numeros)

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    #Obteniendo formulario de contacto
    if request.method == 'GET':
        return render_template('contacto.html')
    
    #Guardando la información de contacto
    nombres = request.form.get('nombres')
    email = request.form.get('email')
    celular = request.form.get('celular')
    observacion = request.form.get('observacion')

    

    return 'Guardando información ' + observacion
    
@app.route('/sumar')
def sumar():
    resultado = 2+2
    return 'la suma de 2+2=' + str(resultado)

@app.route('/usuarios')
def usuarios():
    usuarios = db.execute('select * from usuarios')

    usuarios = usuarios.fetchall()

    return render_template('usuarios/listar.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['GET', 'POST'])
def crear_usuarios():
    if request.method == 'GET':
        return render_template('usuarios/crear.html')
    
    nombres = request.form.get('nombres')
    apellidos = request.form.get('apellidos')
    email = request.form.get('email')
    password = request.form.get('password')

    cursor = db.cursor()
    cursor.execute("""insert into usuarios(
            nombres,
            apellidos,
            email,
            password
        )values (?,?,?,?)
    """, (nombres, apellidos, email, password))

    db.commit()

    return redirect(url_for('usuarios'))

@app.route('/usuarios/actualizar', methods=['GET', 'POST'])
def actualizar_usuarios():
    if request.method == 'GET':
        return render_template('usuarios/actualizar.html')
    
    identificacion = request.form.get('id')


    usuarios = db.execute('select * from usuarios where id = ? ', identificacion)

    usuarios = usuarios.fetchone()

    if(usuarios != None):
        print('s')

    nombres = request.form.get('nombres')
    apellidos = request.form.get('apellidos')
    email = request.form.get('email')
    password = request.form.get('password')

    usuario = list(usuarios)

    if(nombres != ''):
        usuario[1] = nombres
    
    if(apellidos != ''):
        usuario[2] = apellidos

    if(email != ''):
        usuario[3] = email
    if(password != ''):
        usuario[4] = password

    cursor = db.cursor()
    cursor.execute("""update usuarios SET
            nombres = ?,
            apellidos = ?,
            email = ?,
            password = ?
            where id = ?
    """, (usuario[1], usuario[2], usuario[3], usuario[4],usuario[0]))
    db.commit()
    return redirect(url_for('usuarios'))

@app.route('/usuarios', methods=['GET', 'POST'])
def eliminar_usuario():

    identificacion = request.form.get('id')

    cursor = db.cursor()
    cursor.execute("""delete from usuarios
            where id = ?
    """,(identificacion))

    db.commit()

    return redirect(url_for('usuarios'))

app.run(debug=True)