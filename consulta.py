from flask import render_template, request
import pymssql


def consulta():
    if request.method == 'POST':
        codigo = request.form['codigo']
        connections = {
            'K1': {'server': '10.242.149.3', 'user': 'sa', 'password': 'nomeacuerdo.86', 'database': 'Kiosco'},
            'K2': {'server': '10.242.96.105', 'user': 'sa', 'password': 'nomeacuerdo.86', 'database': 'Kiosco'},
            'K3': {'server': '10.242.190.67', 'user': 'sa', 'password': 'nomeacuerdo.86', 'database': 'Kiosco'},
            'K5': {'server': '10.242.115.59', 'user': 'sa', 'password': 'nomeacuerdo.86', 'database': 'Kiosco'}
        }
        results_combined = {}

        for key, conn_info in connections.items():
            if conn_info['server']:
                conn = pymssql.connect(**conn_info)
                cursor = conn.cursor()
                cursor.execute(f"SELECT Descripcion, Precio_Venta FROM Productos WHERE Id_Producto = '{codigo}'")
                results_combined[key] = cursor.fetchall()
                conn.close()

        return render_template('consulta.html', results=results_combined)
    return render_template('consulta.html', results=None)
