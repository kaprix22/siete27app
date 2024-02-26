# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import pymssql
from datetime import date

app = Flask(__name__)

app.config['MYSQL_HOST'] = '144.22.37.71'
app.config['MYSQL_USER'] = 'alitan2'
app.config['MYSQL_PASSWORD'] = 'alitan2'
app.config['MYSQL_DB'] = 'cuaderno'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    billete_2000 = int(request.form['billete_2000'])
    billete_1000 = int(request.form['billete_1000'])
    billete_500 = int(request.form['billete_500'])
    billete_200 = int(request.form['billete_200'])
    billete_100 = int(request.form['billete_100'])
    cambio = int(request.form['cambio'])
    fajos = int(request.form['fajos'])

    total = (billete_2000 * 2000) + (billete_1000 * 1000) + (billete_500 * 500) + (billete_200 * 200) + (billete_100 * 100) + cambio + fajos

    return render_template('index.html', total=total)

@app.route('/caja')
def caja():
    # Obtener todos los movimientos de la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movimientos")
    movimientos = cur.fetchall()
    cur.close()

    # Formatear los montos de los movimientos
    movimientos_formateados = []
    for movimiento in movimientos:
        monto_formateado = "${:,.2f}".format(movimiento[3]).replace(",", ";").replace(".", ",").replace(";", ".")
        movimientos_formateados.append((movimiento[0], movimiento[1], movimiento[2], monto_formateado, movimiento[4]))

    # Calcular el saldo de la caja
    saldo = 0
    for movimiento in movimientos:
        if movimiento[2] == 'ingreso':
            saldo += movimiento[3]
        else:
            saldo -= movimiento[3]

    # Formatear el saldo
    saldo_formateado = "${:,.2f}".format(saldo).replace(",", ";").replace(".", ",").replace(";", ".")

    # Obtener la fecha actual en el formato "dd-mm-aaaa"
    fecha_actual = date.today().strftime("%Y-%m-%d")

    # Renderizar la plantilla index.html pasando los movimientos, el saldo y la fecha actual como argumentos
    return render_template("caja.html", movimientos=movimientos_formateados, saldo=saldo_formateado,
                           fecha_actual=fecha_actual)

    # Definir la ruta para agregar un nuevo movimiento


@app.route("/agregar", methods=["POST"])
def agregar():
    # Obtener los datos del formulario
    fecha = request.form.get("fecha", date.today().strftime("%Y-%m-%d"))
    tipo = request.form.get("tipo")
    monto = request.form.get("monto")
    motivo = request.form.get("motivo")
    # Insertar el nuevo movimiento en la base de datos
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO movimientos (fecha, tipo, monto, motivo) VALUES (%s, %s, %s, %s)",
                (fecha, tipo, monto, motivo))
    mysql.connection.commit()
    cur.close()
    # Redirigir a la página principal
    return redirect(url_for("caja"))


# Definir la ruta para eliminar un movimiento
@app.route("/eliminar/<id>")
def eliminar(id):
    # Eliminar el movimiento con el id dado de la base de datos
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM movimientos WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    # Redirigir a la página principal
    return redirect(url_for("caja"))

@app.route('/redbus')
def redbus():
    return render_template('redbus.html')

@app.route('/virtual')
def virtual():
    return render_template('virtual.html')

@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    if request.method == 'POST':
        codigo = request.form['codigo']
        conn_dockerlocal = pymssql.connect(server='10.242.182.230', user='sa', password='nomeacuerdo.86', database='Kiosco')
        conn_k1 = pymssql.connect(server='10.242.149.3', user='sa', password='nomeacuerdo.86', database='Kiosco')

        cursor_dockerlocal = conn_dockerlocal.cursor()
        cursor_k1 = conn_k1.cursor()


        cursor_dockerlocal.execute(f"SELECT Descripcion, Precio_Venta FROM Productos WHERE Id_Producto = '{codigo}'")
        results_dockerlocal = cursor_dockerlocal.fetchall()

        cursor_k1.execute(f"SELECT Descripcion, Precio_Venta FROM Productos WHERE Id_Producto = '{codigo}'")
        results_k1 = cursor_k1.fetchall()

        conn_dockerlocal.close()
        conn_k1.close()

        # Crear un diccionario con los nombres asignados a las conexiones
        results_combined = {
            'dockerlocal': results_dockerlocal,
            'K1': results_k1
        }

        return render_template('consulta.html', results=results_combined)
    return render_template('consulta.html', results=None)

if __name__ == '__main__':
    app.run(debug=True, port=5001)