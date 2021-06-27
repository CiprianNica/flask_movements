from movements import app
from flask import render_template, request, redirect, url_for
import csv
import sqlite3


@app.route('/')
def listaIngresos():
    conn = sqlite3.connect('movements/data/basededatos.db')
    c = conn.cursor()

    c.execute('SELECT fecha, concepto, cantidad FROM Movimientos;')

    '''
    fIngresos = open("movements/data/basededatos.csv", "r")
    csvReader = csv.reader(fIngresos, delimiter=',', quotechar='"')
    ingresos =list(csvReader)
    '''
    c.execute('SELECT fecha, concepto, cantidad FROM Movimientos;')
    ingresos = c.fetchall()
    conn.close()
    sumador = 0
    for ingreso in ingresos:
        sumador += float(ingreso[2])

    return render_template('movementsList.html', datos=ingresos, total=sumador)

@app.route('/creaalta', methods=['GET','POST'])
def nuevoIngreso():
    if request.method == 'POST':
        conn = sqlite3.connect('movements/data/basededatos.db')
        c = conn.cursor()
        # grabar datos
        c.execute('INSERT INTO Movimientos (cantidad, concepto, fecha) VALUES (?, ?, ?)', 
            (
            float(request.form.get('cantidad')),
            request.form.get('concepto'),
            request.form.get('fecha')
            )
        )
        conn.commit()
        conn.close()
        '''
        fIngresos = open("movements/data/basededatos.csv", "a", newline='')
        csvWriter = csv.writer(fIngresos, delimiter=',', quotechar='"')
        csvWriter.writerow([request.form.get('fecha'), request.form.get('concepto'), request.form.get('cantidad')])
        '''
        return redirect(url_for('listaIngresos'))

    return render_template("alta.html")
