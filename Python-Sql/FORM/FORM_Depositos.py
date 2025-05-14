import flet as ft
from flet import *
import pyodbc

def main(page: ft.Page):
    servidor = 'DESKTOP-SMKHTJB'
    basedatos = 'DepositoVehicular'
    
    stringConexion = f"DRIVER={{SQL Server}}; SERVER={servidor}; DATABASE={basedatos}; Trusted_Connection=yes"   #  CADENA DE CONEXION

    page.theme_mode = ft.ThemeMode.LIGHT

    def run_query(consulta, parameters = ()):
        try:
            with pyodbc.connect(stringConexion) as conn:                
                query = conn.cursor()
                query.execute(consulta, parameters)
                try: 
                    dato = query.fetchall()
                    conn.commit()
                    return dato
                except:
                    conn.commit()
                    return 0            
        except Exception as ex:
            print(ex)


    def alerta(titulo, mensaje):
        dlg = ft.AlertDialog(title= ft.Text(titulo), content= ft.Text(mensaje))
        page.open(dlg)

    def controlesAdd():
        pass


    def controlesUpdate():
        pass


    def depositoAdd():
        pass


    def depositoUpdate():
        pass


    # CONTROLES DEL FORMULARIO
    Id = ft.TextField(label='Id', width= 70, read_only= True)
    RazonSocial = ft.TextField(label='RAZON SOCIAL', width= 465)
    RepresentanteLegal = ft.TextField(label='REPRESENTANTE LEGAL', width= 465)
    

    MunicipioId = Dropdown(label= 'MUNICIPIO', width=300, enable_filter= True, editable= True) #, on_change=lambda _:regionSeleccionada())
    DireccionDeposito = ft.TextField(label='DIRECCIÓN', width= 500)
    Telefonos = ft.TextField(label='TELEFONO(S)', width= 200)

    NombreCompletoContactos = ft.TextField(label='NOMBRE DE CONTACTO', width= 450)
    CorreoElectronicoContacto = ft.TextField(label='CORREO ELECTRONICO', width= 250)
    
    
    Latitud = ft.TextField(label='LATITUD', width=180)
    Longitud = ft.TextField(label='LONGITUD', width=180)
    
    Activo = ft.Checkbox(label='ACTIVO', visible= False)

    # BOTONES PARA EL FORMULARIO
    btnAgregar = ft.CupertinoFilledButton('AGREGAR', width= 120, opacity_on_click=0.3, border_radius=10, on_click=lambda _:depositoAdd())
    btnEditar = ft.CupertinoFilledButton('EDITAR', width= 120, opacity_on_click=0.3, border_radius=10, visible= False, on_click=lambda _:depositoUpdate())
    btnCancelarEdicion = ft.CupertinoFilledButton('CANCELAR', width= 120, opacity_on_click=0.3, border_radius=10, visible= False, on_click=lambda _:controlesAdd())

    #   ,[CreadoPorAdminId]
    #   ,[FechaCreacion]
    #   ,[ActualizadoPorAdminId]
    #   ,[FechaActualizacion]
    #   ,[Activo]

    page.add(
        ft.Row(
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            controls= [
                ft.Column(
                    controls=[Id]
                ),
                ft.Column(
                    controls=[RazonSocial]
                ),
                ft.Column(
                    controls=[RepresentanteLegal]
                )      
                ]
        ),
        ft.Row(
            controls=[
                ft.Column(
                    controls=[MunicipioId]
                ),
                ft.Column(
                    controls=[DireccionDeposito]                    
                ),
                ft.Column(
                    controls=[Telefonos]
                )             
            ]
        ),
        ft.Row(
            controls=[
                ft.Column(
                    controls=[NombreCompletoContactos]                    
                ),
                ft.Column(
                    controls=[CorreoElectronicoContacto]                    
                )
            ]            
        ),
        ft.Row(
            controls=[
                ft.Column(
                    controls=[Latitud]                    
                ),
                ft.Column(
                    controls=[Longitud]                    
                )
            ]            
        ),
        ft.Row(
            controls=[
                ft.Column(
                    controls=[Activo]                    
                )
            ]            
        ),
        ft.Row(
            controls=[
                ft.Column(
                    controls=[btnAgregar, btnEditar, btnCancelarEdicion]                    
                )
            ]            
        )

    )


ft.app(target=main)