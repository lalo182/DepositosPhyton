import flet as ft
import pyodbc
from flet import *
from datetime import datetime

def main(page: ft.Page):
    servidor = 'ECI-SDMYT-001'
    # servidor = 'DESKTOP-SMKHTJB'
    basedatos = 'DepositoVehicular'
    
    stringConexion = f"DRIVER={{SQL Server}}; SERVER={servidor}; DATABASE={basedatos}; Trusted_Connection=yes"   #  CADENA DE CONEXION

    page.theme_mode = ft.ThemeMode.DARK

    lv = ft.ListView(expand=1, auto_scroll=True, spacing= 25, padding= 15, width= 1300)
    lista_depositos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('ID')),
            ft.DataColumn(ft.Text('RAZÓN SOCIAL')),
            ft.DataColumn(ft.Text('REPRESENTANTE LEGAL')),
            ft.DataColumn(ft.Text('DIRECCIÓN')),
            ft.DataColumn(ft.Text('MUNICIPIO')),
            ft.DataColumn(ft.Text('TELEFONOS'))
        ], rows=[]
    )

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
        except Exception as ex:
            print(ex)
        finally:
            conn.close()


    def alerta(titulo, mensaje):
        dlg = ft.AlertDialog(title= ft.Text(titulo), content= ft.Text(mensaje))
        page.open(dlg)


    def cargarMunicipiosLista():
        consultaSql = 'SELECT Id, UPPER(Municipio) FROM [CatMunicipio] ORDER BY Id'
        municipiosDb = run_query(consultaSql)
        for row in municipiosDb:
            MunicipioId.options.append(
                ft.DropdownOption(
                    key = (str(row[0])+'- '+ row[1]),
                    content= ft.Text(                        
                        str(row[1])
                    )
                )                
            )
        page.update()
        

    def mostrarDepositos():
        consultaSql = ''' SELECT cdv.Id
                         ,RazonSocial
                         ,RepresentanteLegal
                         ,DireccionDeposito
                         ,cm.Municipio
                         ,Telefonos
                     FROM CatDepositoVehicular cdv 
               INNER JOIN CatMunicipio cm ON cdv.MunicipioId = cm.Id'''
        depositosLstDb = run_query(consultaSql)
        lv.controls.clear()
        lv.controls.append(lista_depositos)
        generar_tabla(depositosLstDb)
        page.update()


    def generar_tabla(filas):
        rows = []
        for fila in filas:            
            cells = []
            for col in fila:
                cells.append(ft.DataCell(ft.Text(col)))
            rows.append(ft.DataRow(cells=cells, on_select_changed=selectedrow))
        lista_depositos.rows = rows
        page.update()
   

    def selectedrow(e):
        IdSeleccionado = int(e.control.cells[0].content.value)
        consultaSql = '''SELECT cdv.Id
                               ,RazonSocial
                               ,RepresentanteLegal
                               ,CorreoElectronicoContacto
                               ,NombreCompletoContactos
                               ,Telefonos
                               ,DireccionDeposito
                               ,cdv.MunicipioId
                               ,UPPER(cm.Municipio)
                               ,Latitud
                               ,Longitud
                               ,cdv.Activo
                               ,CreadoPorAdminId
                               ,FechaCreacion
                               ,ActualizadoPorAdminId
                               ,FechaActualizacion
                           FROM CatDepositoVehicular cdv 
                     INNER JOIN CatMunicipio cm ON cdv.MunicipioId = cm.Id
                          WHERE cdv.Id = ? '''
        depositoDB = run_query(consultaSql, (IdSeleccionado,))
        Id.value = str(depositoDB[0][0])
        RazonSocial.value = str(depositoDB[0][1])
        RepresentanteLegal.value = str(depositoDB[0][2])
        CorreoElectronicoContacto.value = str(depositoDB[0][3])
        NombreCompletoContactos.value = str(depositoDB[0][4])
        Telefonos.value = str(depositoDB[0][5])
        DireccionDeposito.value = str(depositoDB[0][6])
        MunicipioId.value = str(depositoDB[0][7])+ '- ' + str(depositoDB[0][8])
        Latitud.value = str(depositoDB[0][9])
        Longitud.value = str(depositoDB[0][10])
        Activo.value = bool(depositoDB[0][11])
        controlesUpdate()
        page.update()


    def MunicipioSeleccionado(): # (e):
        textoSeleccionado = MunicipioId.value
        posicion = textoSeleccionado.find('-')
        if posicion != -1:
            valor = textoSeleccionado[:posicion]
            return valor
        else:
            alerta('ALERTA', 'OCURRIO UN ERROR AL SELECCIONAR EL ELEMENTO')
        page.update()


    def depositoAdd():
        RazonSocialAttr = RazonSocial.value
        RepresentanteLegalAttr = RepresentanteLegal.value
        CorreoElectronicoContactoAttr = CorreoElectronicoContacto.value
        NombreCompletoContactosAttr = NombreCompletoContactos.value
        TelefonosAttr = Telefonos.value
        DireccionDepositoAttr = DireccionDeposito.value
        MunicipioIdAttr = MunicipioSeleccionado()
        LatitudAttr = Latitud.value
        LongitudAttr = Longitud.value
        CreadoPorAdminIdAttr = 1
        ActualizadoPorAdminIdAttr = 1
        # ActivoAttr = True
        consultaSql = '''INSERT INTO CatDepositoVehicular
                        (RazonSocial, RepresentanteLegal, CorreoElectronicoContacto, NombreCompletoContactos
                        ,Telefonos, DireccionDeposito, MunicipioId, Latitud, Longitud
                        ,CreadoPorAdminId, FechaCreacion, ActualizadoPorAdminId, FechaActualizacion, Activo)
                    VALUES(?,?,?,?,?,?,?,?,?,?,GETDATE(),?,GETDATE(),1)'''
        try:
            run_query(consultaSql, (RazonSocialAttr, RepresentanteLegalAttr, CorreoElectronicoContactoAttr, NombreCompletoContactosAttr
                                   ,TelefonosAttr, DireccionDepositoAttr, int(MunicipioIdAttr), LatitudAttr, LongitudAttr
                                   ,int(CreadoPorAdminIdAttr), int(ActualizadoPorAdminIdAttr),))
            alerta('EXITOSO', 'REGISTRO GUARDADO EXITOSAMENTE: ' + RazonSocialAttr)
            mostrarDepositos()
        except:
            alerta('EXCEPCION', 'OCURRIO UNA EXCEPCION AL GUARDAR INFORMACIÓN')
        limpiarControles()
        controlesAdd()
        page.update()


    def depositoUpdate():
        RazonSocialAttr = RazonSocial.value
        RepresentanteLegalAttr = RepresentanteLegal.value
        CorreoElectronicoContactoAttr = CorreoElectronicoContacto.value
        NombreCompletoContactosAttr = NombreCompletoContactos.value
        TelefonosAttr = Telefonos.value
        DireccionDepositoAttr = DireccionDeposito.value
        MunicipioIdAttr = MunicipioSeleccionado()
        LatitudAttr = Latitud.value
        LongitudAttr = Longitud.value
        ActivoAttr = Activo.value
        IdAttr = Id.value
        consultaSql = '''UPDATE CatDepositoVehicular
                             SET RazonSocial = ?
                                ,RepresentanteLegal = ?
                                ,CorreoElectronicoContacto = ?
                                ,NombreCompletoContactos = ?
                                ,Telefonos = ?
                                ,DireccionDeposito = ?
                                ,MunicipioId = ?
                                ,Latitud = ?
                                ,Longitud = ?
                                ,ActualizadoPorAdminId = 1
                                ,FechaActualizacion = GETDATE()
                                ,Activo = ?
                            WHERE Id = ?'''
        try:
            run_query(consultaSql, (RazonSocialAttr, RepresentanteLegalAttr, CorreoElectronicoContactoAttr, NombreCompletoContactosAttr
                                   ,TelefonosAttr, DireccionDepositoAttr, MunicipioIdAttr, LatitudAttr, LongitudAttr, ActivoAttr, IdAttr))
            alerta('EXITOSO', 'REGISTRO ACTUALIZADO EXITOSAMENTE: ' + RazonSocialAttr)
            mostrarDepositos()
        except:
            alerta('ALERTA', 'oOCURRIO UN ERROR AL INTENTAR ACTUALIZAR EL REGISTRO')
        limpiarControles()
        controlesAdd()
        page.update()


    def controlesAdd():
        Activo.visible = False
        btnAgregar.visible = True
        btnEditar.visible = False
        btnCancelarEdicion.visible = False
        page.update()


    def controlesUpdate():
        Activo.visible = True        
        btnAgregar.visible = False
        btnEditar.visible = True
        btnCancelarEdicion.visible = True
        page.update()
        
    
    def cancelAction():        
        limpiarControles()
        controlesAdd()
        page.update()


    def limpiarControles():
        Id.value = ''
        RazonSocial.value = ''
        RepresentanteLegal.value = ''
        MunicipioId.value = ''
        DireccionDeposito.value = ''
        NombreCompletoContactos.value = ''
        CorreoElectronicoContacto.value = ''
        Telefonos.value = ''
        Latitud.value = ''
        Longitud.value = ''
        Activo.value = True
        

    # CONTROLES DEL FORMULARIO
    Id = ft.TextField(label='Id', width= 70, read_only= True)
    RazonSocial = ft.TextField(label='RAZON SOCIAL', width= 565)
    RepresentanteLegal = ft.TextField(label='REPRESENTANTE LEGAL', width= 565)
    MunicipioId = Dropdown(label= 'MUNICIPIO', width=500, enable_filter= True, editable= True) #, on_change=lambda _:regionSeleccionada())
    DireccionDeposito = ft.TextField(label='DIRECCIÓN', width= 700)
    NombreCompletoContactos = ft.TextField(label='NOMBRE DE CONTACTO', width= 450)
    CorreoElectronicoContacto = ft.TextField(label='CORREO ELECTRONICO', width= 400)
    Telefonos = ft.TextField(label='TELEFONO(S)', width= 300)    
    Latitud = ft.TextField(label='LATITUD', width=450)
    Longitud = ft.TextField(label='LONGITUD', width=450)    
    Activo = ft.Switch(label='ACTIVO', label_position=ft.LabelPosition.LEFT, visible= False)

    # BOTONES DEL FORMULARIO
    btnAgregar = ft.CupertinoFilledButton('AGREGAR', width= 120, opacity_on_click=0.3, border_radius=10, on_click=lambda _:depositoAdd())
    btnEditar = ft.CupertinoFilledButton('EDITAR', width= 120, opacity_on_click=0.3, border_radius=10, visible= False, on_click=lambda _:depositoUpdate())
    btnCancelarEdicion = ft.CupertinoFilledButton('CANCELAR', width= 120, opacity_on_click=0.3, border_radius=10, visible= False, on_click=lambda _:cancelAction())


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
                ),
                ft.Column(
                    controls=[Telefonos]
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
            vertical_alignment= ft.CrossAxisAlignment.START,
            controls=[btnAgregar, btnEditar, btnCancelarEdicion]
            # controls=[
            #     ft.Column(
            #         controls=[btnAgregar, btnEditar, btnCancelarEdicion]
            #     )
            # ]            
        ),
        ft.Row(
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=1100,
                    alignment=ft.alignment.top_center,
                    content = lv
                )
            ]
        )
    )

    mostrarDepositos()
    cargarMunicipiosLista()
    controlesAdd()

ft.app(target=main)