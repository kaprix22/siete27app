from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from flask_mysqldb import MySQL

app = Flask(__name__)


mysql = MySQL(app)


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
