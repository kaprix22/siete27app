from flask import Flask, render_template
from flask_mysqldb import MySQL
from consulta import consulta
from caja import caja

app = Flask(__name__)

app.config['MYSQL_HOST'] = '144.22.37.71'
app.config['MYSQL_USER'] = 'alitan2'
app.config['MYSQL_PASSWORD'] = 'alitan2'
app.config['MYSQL_DB'] = 'cuaderno'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculadora')
def calculadora():
    return render_template('calculadora.html')


@app.route('/caja')
def caja_route():
    return caja()


@app.route('/consulta', methods=['GET', 'POST'])
def consulta_route():
    return consulta()


@app.route('/redbus')
def redbus():
    return render_template('redbus.html')


@app.route('/virtual')
def virtual():
    return render_template('virtual.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
