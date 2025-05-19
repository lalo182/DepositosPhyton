import flet as ft
from flet import *
import pyodbc


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.bgcolor = ft.Colors.LIGHT_BLUE_100 # ft.Colors.BLUE_GREY_800
    page.title = 'DEPOSITOS VEHICULARES'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    ancho_win = 1100
    largo_win = 950
    
    page.window_width=ancho_win
    page.window_height=largo_win

    # page.window.max_width=ancho_win
    # page.window.max_height=largo_win

    # page.window.min_width=ancho_win
    # page.window.min_height=largo_win



    anchocol = 220

    servidor = 'ECI-SDMYT-001'
    # servidor = 'DESKTOP-SMKHTJB'
    basedatos = 'DepositoVehicular'
    
    stringConexion = f"DRIVER={{SQL Server}}; SERVER={servidor}; DATABASE={basedatos}; Trusted_Connection=yes"   #  CADENA DE CONEXION

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #     
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
    

    def limpiarControles():
        # CONTROLES DEL FORMULARIO DE REGION
        regionId.value = ''
        regionNombre.value = ''
        regionActivo.value = False
        # CONTROLES DEL FORMULARIO DE MUNICIPIO
        municipioIdProp.value = ''
        municipioNombreProp.value = ''
        municipioSelectRegion.value = ''
        # CONTROLES DEL FORMULARIO DE DEPOSITOS
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
        

    def botonesAgregar():        
        btnAgregarRegistro.visible =  True
        btnEditarRegistro.visible = False
        btnCancelarAccionForm.visible = False
        regionActivo.visible = False
        page.update()


    def botonesEditar():
        btnAgregarRegistro.visible = False
        btnEditarRegistro.visible = True
        btnCancelarAccionForm.visible = True
        regionActivo.visible = True
        page.update()    
    

    def botonesCancelarAccionForm():
        limpiarControles()
        botonesAgregar()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # LIST VIEW PARA MOSTRAR LAS REGIONES
    lv = ft.ListView(expand=1, auto_scroll=True)
    lista_regiones = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('ID')),
            ft.DataColumn(ft.Text('REGIÓN')),
            ft.DataColumn(ft.Text('ESTATUS'))
        ], rows=[],
    )

    lista_municipios = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('ID')),
            ft.DataColumn(ft.Text('MUNICIPIO')),
            ft.DataColumn(ft.Text('REGION'))
        ], rows=[]
    )
    
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
    
    # LIST VIEW PARA MOSTRAR LAS REGIONES

    # ELEMENTOS PARA LA PLANTILLA DEL FORMULARIO DE REGIONES
    def regionesLista():
        consultaSql = 'SELECT Id, NombreRegion, Activo FROM CatRegion'
        regionesdb = run_query(consultaSql)
        lv.controls.clear()
        lv.controls.append(lista_regiones)
        generar_tabla(regionesdb)
        page.update()


    def municipiosLista():
            consultaSql = 'SELECT cmun.[Id],UPPER([Municipio]),creg.NombreRegion FROM [CatMunicipio] cmun INNER JOIN CatRegion creg ON cmun.RegionId = creg.Id ORDER BY cmun.Id'
            municipiosDb = run_query(consultaSql)
            lv.controls.clear()
            lv.controls.append(lista_municipios)
            generar_tabla_municipios(municipiosDb)
            page.update()


    def depositosLista():
        consultaSql = '''SELECT cdv.Id
                         ,RazonSocial
                         ,RepresentanteLegal
                         ,DireccionDeposito
                         ,cm.Municipio
                         ,Telefonos
                     FROM CatDepositoVehicular cdv 
               INNER JOIN CatMunicipio cm ON cdv.MunicipioId = cm.Id'''
        depositosDb = run_query(consultaSql)
        lv.controls.clear()
        lv.controls.append(lista_depositos)
        generar_tabla_depositos(depositosDb)
        page.update()


    def selectedrow(e):    
        if e.control.selected:
            e.control.selected=False
        else:
            e.control.selected=True
            regionId.value = int(e.control.cells[0].content.value)
            regionNombre.value = str(e.control.cells[1].content.value)
            regionActivo.value = bool(e.control.cells[2].content.value)
            botonesEditar()
            page.update()


    def selectedrowMunicipios(e):
        municipioIdSelected = str(e.control.cells[0].content.value)
        print(municipioIdSelected)
        consultaSql = 'SELECT cm.Id, UPPER(Municipio), RegionId, cre.NombreRegion [region] FROM CatMunicipio cm INNER JOIN CatRegion cre ON cm.RegionId = cre.Id WHERE cm.Id = ?'        
        municipioDb = run_query(consultaSql,(municipioIdSelected,))
        municipioIdProp.value = str(municipioDb[0][0])
        municipioNombreProp.value = str(municipioDb[0][1])
        municipioSelectRegion.value = str(municipioDb[0][2]) + '- ' + str(municipioDb[0][3])
        # controlesEditar()
        botonesEditar()
        page.update()


    def selectedrowDepositos(e):
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
        botonesEditar()
        page.update()


    def generar_tabla(filas):
        rows = []
        for fila in filas:
            cells = [] 
            for col in fila:
                cells.append(ft.DataCell(ft.Text(col)))
            rows.append(ft.DataRow(cells=cells, on_select_changed=selectedrow))
        lista_regiones.rows = rows
        page.update()


    def generar_tabla_municipios(filas):
        rows = []
        for fila in filas:
            cells = [] 
            for col in fila:
                cells.append(ft.DataCell(ft.Text(col)))
            rows.append(ft.DataRow(cells=cells, on_select_changed=selectedrowMunicipios))
        lista_municipios.rows = rows
        page.update()


    def generar_tabla_depositos(filas):
        rows = []
        for fila in filas:            
            cells = []
            for col in fila:
                cells.append(ft.DataCell(ft.Text(col)))
            rows.append(ft.DataRow(cells=cells, on_select_changed=selectedrowDepositos))
        lista_depositos.rows = rows
        page.update()


    def regionSeleccionada():
        textoSeleccionado = municipioSelectRegion.value
        posicion = textoSeleccionado.find('-')
        if posicion != -1:
            valor = textoSeleccionado[:posicion]
            return valor
        else:
            alerta('AVISO', 'OCURRIO UN ERROR AL SELECCIONAR EL ELEMENTO')
        page.update()


    def municipioSeleccionado():
        textoSeleccionado = MunicipioId.value
        posicion = textoSeleccionado.find('-')
        if posicion != -1:
            valor = textoSeleccionado[:posicion]
            return valor
        else:
            alerta('ALERTA', 'OCURRIO UN ERROR AL SELECCIONAR EL ELEMENTO')
        page.update()


    def regionesDropDownList():
        consultaSql = 'SELECT Id, NombreRegion  FROM CatRegion WHERE Activo = 1 ORDER BY NombreRegion'
        regionesLst = run_query(consultaSql)        
        for row in regionesLst:
            municipioSelectRegion.options.append(
                ft.DropdownOption(
                    key = (str(row[0])+'- '+row[1]),
                    content= ft.Text(                        
                        str(row[1])
                    )
                )                
            )
        page.update()


    def municipiosDropDownList():
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


    def regionesAdd():
        nuevaRegion = regionNombre.value.upper()
        consultaSql = 'INSERT INTO CatRegion (NombreRegion, Activo) VALUES(?, 1)'
        try:
            run_query(consultaSql, (nuevaRegion,))                       
            regionesLista()
            limpiarControles()
            botonesAgregar()
            alerta('EXITOSO', 'SE AGREGO CORRECTAMENTE A ' + nuevaRegion) 
        except Exception as ex:
            alerta('WARNING', 'OCURRIO UN ERROR')        


    def regionesUpdate():
        regid = regionId.value
        nuevaRegion = regionNombre.value.upper()
        estatusRegion = regionActivo.value
        consultaSql = 'UPDATE CatRegion SET [NombreRegion] = ? , Activo = ? WHERE Id = ? '        
        try:
            run_query(consultaSql,(nuevaRegion, estatusRegion,regid))            
            regionesLista()          
            limpiarControles()
            botonesAgregar()
            alerta('EXITOSO', 'SE ACTUALIZO CORRECTAMENTE A ' + nuevaRegion)
        except Exception as ex:
            alerta('WARNING', 'OCURRIO UN ERROR')
        

    def municipioAdd():
            municipio = municipioNombreProp.value
            regionId = regionSeleccionada()
            consultaSql = 'INSERT INTO CatMunicipio (Municipio, RegionId) VALUES (? , ?)'
            try:
                run_query(consultaSql, (municipio, int(regionId),))
                alerta('EXITOSO', 'REGISTRO GUARDADO EXITOSAMENTE')
                municipiosLista()
                limpiarControles()            
            except Exception as ex:
                print('Error al guardar')
            page.update()


    def municipioUpdate():
        id = municipioIdProp.value
        municipio = municipioNombreProp.value
        regionId = regionSeleccionada()
        consultaSql = 'UPDATE CatMunicipio SET Municipio = ?, RegionId =? WHERE Id = ?'
        try:
            run_query(consultaSql, (municipio, regionId, id))            
            alerta('EXITOSO', 'REGISTRO ACTUALIZADO EXITOSAMENTE')
            municipiosLista()
            limpiarControles()
        except Exception as ex:
            print('ERROR AL ACRTUALIZAR')


    def depositoAdd():
        RazonSocialAttr = RazonSocial.value
        RepresentanteLegalAttr = RepresentanteLegal.value
        CorreoElectronicoContactoAttr = CorreoElectronicoContacto.value
        NombreCompletoContactosAttr = NombreCompletoContactos.value
        TelefonosAttr = Telefonos.value
        DireccionDepositoAttr = DireccionDeposito.value
        MunicipioIdAttr = municipioSeleccionado()
        LatitudAttr = Latitud.value
        LongitudAttr = Longitud.value
        CreadoPorAdminIdAttr = 1
        ActualizadoPorAdminIdAttr = 1
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
            depositosLista()
        except:
            alerta('EXCEPCION', 'OCURRIO UNA EXCEPCION AL GUARDAR INFORMACIÓN')
        limpiarControles()
        botonesAgregar()
        page.update()


    def depositoUpdate():
        RazonSocialAttr = RazonSocial.value
        RepresentanteLegalAttr = RepresentanteLegal.value
        CorreoElectronicoContactoAttr = CorreoElectronicoContacto.value
        NombreCompletoContactosAttr = NombreCompletoContactos.value
        TelefonosAttr = Telefonos.value
        DireccionDepositoAttr = DireccionDeposito.value
        MunicipioIdAttr = municipioSeleccionado()
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
            depositosLista()
        except:
            alerta('ALERTA', 'oOCURRIO UN ERROR AL INTENTAR ACTUALIZAR EL REGISTRO')
        limpiarControles()
        botonesAgregar()
        page.update()


    # CONTROLES PARA EL FORMULARIO DE REGIONES
    regionId = ft.TextField(label='Id', width=anchocol, read_only=True)
    regionNombre = ft.TextField(label='Region', width=anchocol)
    regionActivo = ft.Checkbox(label='Disponible', visible= False)    
    # CONTROLES PARA EL FORMULARIO DE MUNICIPIOS
    municipioIdProp = ft.TextField(label='Id', width= 80, read_only= True)
    municipioNombreProp = ft.TextField(label='MUNICIPIO', width= 720)
    municipioSelectRegion = Dropdown(label= 'REGIÓN', width=350, enable_filter= True, editable= True, on_change=lambda _:regionSeleccionada())
    # CONTROLES PARA EL FORMULARIO DE DEPOSITOS
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


    # BOTONES
    btnEditarRegistro = ft.CupertinoFilledButton('EDITAR', width=120, opacity_on_click=0.3, border_radius=10, visible = False) # , on_click=lambda _:regionesUpdate()
    btnAgregarRegistro = ft.CupertinoFilledButton('AGREGAR', width=120, opacity_on_click=0.3, border_radius=10, visible = True) # , on_click=lambda _:regionesAdd()
    btnCancelarAccionForm = ft.CupertinoFilledButton('CANCELAR', width=120, opacity_on_click=0.3, border_radius=10, visible = False) # , on_click=lambda _:regionesAdd()



    def on_navigation_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            show_CatRegiones()            
        if selected_index == 1:
            show_CatMunicipios()
        if selected_index == 2:
            show_Depositos()
        if selected_index == 3:
            show_RolesDepositos()
        if selected_index == 4:
            show_SancionesDepositos()
        page.update()


    def show_CatRegiones():
        page.controls.clear()
        texto = ft.Text('CATÁLOGO DE REGIONES', size= 30)
        btnAgregarRegistro.on_click = lambda _:regionesAdd()
        btnEditarRegistro.on_click = lambda _:regionesUpdate()
        btnCancelarAccionForm.on_click = lambda _:botonesCancelarAccionForm()
        page.add(texto)
        page.add(
            ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        controls=[
                            ft.Container(
                                width=300,
                                height=480,
                                padding=20,
                                alignment=ft.alignment.center,
                                content=ft.Column(controls=[
                                        ft.Row(controls=[regionId]),
                                        ft.Row(controls=[regionNombre]),
                                        ft.Row(controls=[regionActivo]),
                                        # ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                                        ft.Row(controls = [btnAgregarRegistro, btnEditarRegistro, btnCancelarAccionForm])
                                ])
                            )
                        ], 
                    ),
                    ft.Column(
                        controls=[
                            ft.Row(controls=[
                                ft.Container(                                    
                                    width=600,
                                    height=500,
                                    alignment=ft.alignment.top_center,
                                    content=lv                                    
                                )
                            ],
                            height=600,
                        )
                    ])
                ]
            )
        )
        regionesLista()


    def show_CatMunicipios():
        page.controls.clear()
        texto = ft.Text('CATÁLOGO DE MUNICIPIOS', size= 30)        
        btnAgregarRegistro.on_click = lambda _:municipioAdd()
        btnEditarRegistro.on_click = lambda _:municipioUpdate()
        btnCancelarAccionForm.on_click = lambda _:botonesCancelarAccionForm()
        regionesDropDownList()
        municipiosLista()

        page.add(texto)
        page.add(
            ft.Row(
                vertical_alignment= ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        controls=[municipioIdProp]
                    ),
                    ft.Column(
                        controls=[municipioNombreProp]
                    ),
                    ft.Column(
                        controls=[municipioSelectRegion]
                    )
                ]
            ),
            ft.Row(
                vertical_alignment= ft.CrossAxisAlignment.START,
                controls=[btnAgregarRegistro, btnEditarRegistro, btnCancelarAccionForm]
            ),
            ft.Row(
                vertical_alignment= ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        ft.Container(
                            width=800,
                            height=450,
                            alignment= ft.alignment.top_center,
                            content= lv
                        )
                    )
                ]
            )
        )


    def show_Depositos():
        page.controls.clear()
        texto = ft.Text('CATÁLOGO DE DEPOSITOS', size= 30)
        btnAgregarRegistro.on_click = lambda _:depositoAdd()()
        btnEditarRegistro.on_click = lambda _:depositoUpdate()
        btnCancelarAccionForm.on_click = lambda _:botonesCancelarAccionForm()
        page.add(texto)
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
                vertical_alignment= ft.CrossAxisAlignment.CENTER,
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
                        controls= [NombreCompletoContactos]
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
                controls= [
                    ft.Column(
                        controls= [Latitud]
                    ),
                    ft.Column(
                        controls= [Longitud]
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
                controls= [btnAgregarRegistro, btnEditarRegistro, btnCancelarAccionForm]
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
        depositosLista()
        municipiosDropDownList()
        botonesAgregar()


    def show_RolesDepositos():
        page.controls.clear()
        texto = ft.Text('ROLES DE DEPOSITOS', size= 30)
        page.add(texto)
        

    def show_SancionesDepositos():
        page.controls.clear()
        texto = ft.Text('SANCIONES A DEPOSITOS', size= 30)
        page.add(texto)


    barradeNavegacion = ft.NavigationBar(
        selected_index= 0,
        on_change= on_navigation_change,
        destinations= [
            ft.NavigationBarDestination(icon= ft.Icons.APP_REGISTRATION, label= 'Catálogo de Regiones'),
            ft.NavigationBarDestination(icon= ft.Icons.ACCOUNT_TREE, label= 'Catálogo de Municipios'),
            ft.NavigationBarDestination(icon= ft.Icons.ADD_BUSINESS, label= 'Catálogo de Depositos'),
            ft.NavigationBarDestination(icon= ft.Icons.ACCESS_TIME_FILLED_ROUNDED, label= 'Roles de Depositos'),
            ft.NavigationBarDestination(icon= ft.Icons.INFO_SHARP, label= 'Sanciones Depositos')  # ACCOUNT_BOX, label= 'Sanciones Depositos')  # ADD_CARD_OUTLINED   # ADD_COMMENT
        ],
        bgcolor= ft.colors.LIGHT_BLUE_800,
        indicator_color= ft.Colors.GREEN_400,
        overlay_color= ft.Colors.AMBER_400
    )

    page.navigation_bar = barradeNavegacion
    show_CatRegiones()    

ft.app(target= main)