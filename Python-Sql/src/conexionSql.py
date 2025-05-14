import pyodbc

# Definicion de los parametros de conexion
servidor = 'ECI-SDMYT-001'
# basedatos = 'InformaticaAdmin'
basedatos = 'DepositoVehicular'
# usuario = 'InformaticaAPI'
# contrasenia = 'Adm1nAP1!'

# DEFINIMOS LA CADENA DE CONEXION
# stringConexion = f"DRIVER={{SQL Server}}; SERVER={servidor}; DATABASE={basedatos}; UID={usuario}; PWD={contrasenia}"
stringConexion = f"DRIVER={{SQL Server}}; SERVER={servidor}; DATABASE={basedatos}; Trusted_Connection=yes"

# # FUNCION PARA OBTENER LA CONEXION A LA BASE DE DATOS
# def get_conexion():
#     try:
#         cnxSql = pyodbc.connect(stringConexion)
#         print("conexion exitosa")
#         return cnxSql
#     except pyodbc.Error as e:
#         print("Error al conectar a SQL Server: ", e)
#         return None
#     finally
#         cnxSql.close()

# get_conexion()

def conn (query_data):
    try:
        # conexion = pyodbc.connect('DRIVER={SQL Server}; SERVER=ECI-SDMYT-001; DATABASE=InformaticaAdmin; UID=InformaticaAPI;PWD=Adm1nAP1!;Encrypt=False')
        conexion = pyodbc.connect(stringConexion)
        print("CONEXION EXITOSA")

        query = conexion.cursor()
        # query.execute("SELECT @@version;")
        # row = query.fetchone()
        # print(row)
        query.execute(query_data)
        resultado = query.fetchall()
        for item in resultado:
            print(item)
    except Exception as ex:
        print(ex)
    finally:
        conexion.close()
        print("CONEXION CERRADA")

conn('SELECT * FROM CatMunicipio')