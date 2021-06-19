from re import template
from movements import app
from flask import render_template

@app.route('/')
def listaMovimientos():
    return render_template('movementsList.html', miTexto="Ya veremos si hay lista", texto='hola')

@app.route('/creaalta')
def creaAlta():
    return 'Tengo que devolver una lista de movimientos.'
