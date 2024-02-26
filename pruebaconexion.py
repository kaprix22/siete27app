from flask_mysqldb import MySQL
import pymssql
conn_prueba = pymssql.connect(server='10.242.182.230', user='sa', password='nomeacuerdo.86', database='prueba')
conn_otra = pymssql.connect(server='10.242.182.230', user='sa', password='nomeacuerdo.86', database='Kiosco')

def codigo():

    codigo = '1'

print(f"Consulta para prueba: SELECT Descripcion, Precio_Venta FROM Productos WHERE Id_Producto = '{codigo}'")
print(f"Consulta para Kiosco: SELECT Descripcion, Precio_Venta FROM Productos WHERE Id_Producto = '{codigo}'")
