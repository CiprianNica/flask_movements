from movements import app
from flask import render_template, request, redirect, url_for
import csv

@app.route('/')
def listaIngresos():
    fIngresos = open("movements/data/basededatos.csv", "r")
    csvReader = csv.reader(fIngresos, delimiter=',', quotechar='"')
    ingresos =list(csvReader)
    sumador = 0
    for ingreso in ingresos:
        sumador += float(ingreso[2])

    return render_template('movementsList.html', datos=ingresos, total=sumador)

@app.route('/creaalta', methods=['GET','POST'])
def nuevoIngreso():
    if request.method == 'POST':
        # graba datos
        fIngresos = open("movements/data/basededatos.csv", "a", newline='')
        csvWriter = csv.writer(fIngresos, delimiter=',', quotechar='"')
        csvWriter.writerow([request.form.get('fecha'), request.form.get('concepto'), request.form.get('cantidad')])
        return redirect(url_for('listaIngresos'))

    return render_template("alta.html")
