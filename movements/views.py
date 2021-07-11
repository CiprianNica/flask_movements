from movements.forms import MovementsForm
from sqlite3.dbapi2 import connect
from flask_wtf import form
from movements import app
from flask import render_template, request, redirect, url_for
import csv
import sqlite3

DBFILE = app.config['DBFILE']

def DBconsulta(query, params=()):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()

    '''
    SELECT * FROM TABLA  --> [(), (), (),]
    SELECT * FROM TABLA VACIA -> []
    INSERT....->[]
    UPDATE....->[]
    DELETE....->[]
    '''
    c.execute(query, params)
    conn.commit()
    filas = c.fetchall()
    conn.close()

    if len(filas) == 0:
        return filas

    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0])

    listaDeDiccionarios = []
    

    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames):
            d[columnName] = fila[ix]
        listaDeDiccionarios.append(d)

    return listaDeDiccionarios

@app.route('/')
def listaIngresos():
    
    ingresos = DBconsulta('SELECT fecha, concepto, cantidad, id FROM Movimientos;')

    sumador = 0
    for ingreso in ingresos:
        sumador += float(ingreso['cantidad'])

    return render_template('movementsList.html', datos=ingresos, total=sumador)

@app.route('/creaalta', methods=['GET','POST'])
def nuevoIngreso():
    form = MovementsForm()

    if request.method == 'POST':
        # grabar datos
        DBconsulta('INSERT INTO Movimientos (cantidad, concepto, fecha) VALUES (?, ?, ?)', 
            (
            float(request.form.get('cantidad')),
            request.form.get('concepto'),
            request.form.get('fecha')
            )
        )
        return redirect(url_for('listaIngresos'))

    return render_template("alta.html", form=form)

@app.route('/modifica/<identificador>', methods=['GET','POST'])
def modificaIngresos(identificador): 
    if request.method == 'GET':
        datos = DBconsulta('SELECT fecha, concepto, cantidad, id FROM Movimientos WHERE id=?', (identificador,))
        return render_template("modifica.html", registro = datos[0])
    else:
        cantidad = float(request.form.get('cantidad'))
        concepto = request.form.get('concepto')
        fecha= request.form.get('fecha')
        DBconsulta('UPDATE Movimientos SET fecha=?, concepto=?, cantidad=? WHERE id=?', (fecha, concepto, cantidad, identificador))
        return redirect(url_for('listaIngresos'))

@app.route('/delete/<identificador>', methods=['GET', 'POST'])
def deleteRegistro(identificador):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()        
    if request.method == 'GET':
        c.execute('SELECT fecha, concepto, cantidad, id FROM Movimientos WHERE id=?', (identificador,))
        datos = c.fetchone()
        conn.close()
        return render_template('delete.html', registro = datos)
    else:
        c.execute('DELETE Movimientos WHERE id=?',identificador)
        conn.commit()
        conn.close()
        return redirect(url_for('listaIngresos'))