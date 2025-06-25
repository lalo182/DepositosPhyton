import flet as ft
import pyodbc
import calendar
import datetime as dt
import sqlite3
import flet_map as map
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import colorsys


from flet import *
from datetime import datetime

class Deposito(): # Diseñado para almacenar informacion para los depositos
        def __init__(self, color, id, fec_ini, fec_fin, nombre):
            self.color = color
            self.iddep = id
            self.fei = fec_ini
            self.fef = fec_fin  
            self.nom = nombre

class Inasistencia(): # Almacena reportes de inasistencia de depositos
    def __init__(self, deposito, nota):
        self.dep = deposito
        self.nota = nota


class VehiculoIncidente():
    def __init__(self, incidenteId, noVehiculo, tipoVehiculo, tipoGrua, sinPlacas, 
                 origenPlacasId, origenPlacasNombre, noPlacas, noSerie, marcaId, 
                 marca, linea, modelo, color, nombreConductor, apellidosConductor, observaciones):
        self.incidenteId = incidenteId
        self.noVehiculo = noVehiculo
        self.tipoVehiculo = tipoVehiculo
        self.tipoGrua = tipoGrua
        self.sinPlacas = sinPlacas
        self.origenPlacasId = origenPlacasId
        self.origenPlacasNombre = origenPlacasNombre
        self.noPlacas = noPlacas
        self.noSerie = noSerie
        self.marcaId = marcaId
        self.marca = marca
        self.linea = linea
        self.modelo = modelo
        self.color = color
        self.nombreConductor = nombreConductor
        self.apellidosConductor = apellidosConductor        
        self.observaciones = observaciones

    def actualizarDatos(self, tipoVN, tipoGruaN, sinPlacasN, origenPlacasIdN, 
                        origenPlacasNombreN, noPlacasN, noSerieN,
                        marcaIdN, marcaN, lineaN, modeloN, colorN,
                         nombreConductorN, apellidosConductorN, observacionesN,):
        self.tipoVehiculo = tipoVN
        self.tipoGrua = tipoGruaN
        self.sinPlacas = sinPlacasN
        self.origenPlacasId = origenPlacasIdN
        self.origenPlacasNombre = origenPlacasNombreN
        self.noPlacas = noPlacasN
        self.noSerie = noSerieN
        self.marcaId = marcaIdN
        self.marca = marcaN
        self.linea = lineaN
        self.modelo = modeloN
        self.color = colorN
        self.nombreConductor = nombreConductorN
        self.apellidosConductor = apellidosConductorN
        self.observaciones = observacionesN
        

class mapa(): #objeto mapa

    def __init__(self, lat, lon):
        self.marker_layer = ft.Ref[map.MarkerLayer]()
        self.circle_layer = ft.Ref[map.CircleLayer]()
        self.result = map.Map(
            expand=True,
            initial_center=map.MapLatitudeLongitude(lat, lon),
            initial_zoom=15,
            min_zoom=3,
            interaction_configuration=map.MapInteractionConfiguration(
                flags=map.MapInteractiveFlag.ALL
            ),
            layers=[
                map.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    on_image_error=lambda e: print("TileLayer Error"),
                ),
                map.MarkerLayer(
                    ref=self.marker_layer,
                    markers=[
                        map.Marker(
                        content=ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.RED_ACCENT_700),
                        coordinates=map.MapLatitudeLongitude(lat, lon),
                        )
                    ],
                ),
                map.CircleLayer(
                    ref=self.circle_layer,
                    circles=[],
                ),
                
            ],
        )

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(navigation_bar_theme=ft.NavigationBarTheme(bgcolor='#5F1B2D', label_text_style= ft.TextStyle(color=ft.Colors.WHITE)))
    
    ####### BANNER
    action_button_style = ft.ButtonStyle(color=ft.Colors.TRANSPARENT)
    button_style = ft.ButtonStyle(color='#3D9B84', text_style=ft.TextStyle(color=ft.Colors.WHITE))
    button_style2 = ft.ButtonStyle(color='#B33449', text_style=ft.TextStyle(color=ft.Colors.WHITE))
    banner = ft.Banner(
        bgcolor="#5f1b2d", 
        #bgcolor="#11312d",    
        divider_color=ft.Colors.TRANSPARENT,
        content=ft.Container(
            content=ft.Image(src=f'logo_gruas3.png', height=60),
            image=ft.DecorationImage(src=f'Textura.png', alignment=ft.Alignment(-1.0, 0.0)),
            expand=True,
            alignment=ft.Alignment(-1.0, 0.0),
            margin=10
        ),
        actions=[
            ft.TextButton(
                text="", style=action_button_style, disabled=True, width=1
            ),
        ],
    )

    # page.bgcolor = ft.Colors.LIGHT_BLUE_100 # ft.Colors.BLUE_GREY_800
    page.title = 'DEPOSITOS VEHICULARES'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    ancho_win = 1800
    largo_win = 1150
    
    page.window_width=ancho_win
    page.window_height=largo_win

    # page.window.max_width=ancho_win
    # page.window.max_height=largo_win

    # page.window.min_width=ancho_win
    # page.window.min_height=largo_win
    anchocol = 220

    #servidor = '10.27.1.14' # # SERVIDOR PRODUCTIVO
    servidor = 'DESKTOP-TO7CUU2' # SERVIDIOR DE PABLO
    #servidor = 'DESKTOP-SMKHTJB'  # SERVIDOR DE LALO
    basedatos = 'DepositoVehicular_DB'
    usuario = 'sa'
    claveacceso = 'Gruas$mT*$!'

    ### VARIABLES FORMULARIO INCIDENTES
    global diasm
    diasm = []
    inasists = []
    
    #stringConexion = f"DRIVER={{SQL Server}}; SERVER={servidor}; DATABASE={basedatos}; UID={usuario};PWD={claveacceso}"   #  CADENA DE CONEXION

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
        except pyodbc.Error as ex:
            alerta("AVISO", f"Error al conectarse a la base de datos.\nRevise su conexión o repórtelo a soporte técnico")
            print(ex)


    def run_queryLite(query, parameters = ()):
        miconexionLite = 'SqlLite/DepositosVehiculares.db'
        with sqlite3.connect(miconexionLite) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result


    def tipoIncidenteDDL():
        try:
            consultaLite = 'SELECT Descripcion FROM CatTipoIncidente WHERE Activo = 1'
            rows = run_queryLite(consultaLite)
            for row in rows:
                TipoIncidenteDDL.options.append(
                    ft.DropdownOption(
                        key= (str(row[0])),
                        content= ft.Text(str(row[0]))
                    )
                )
            TipoIncidenteDDL.value = "FALTA ADMINISTRATIVA"
        except Exception as er:
            print("Error: ", er)


    def estatusIncidenteDDL():
        try:
            consultaLite = 'SELECT Descripcion FROM CatEstatusIncidente WHERE Activo = 1'
            rows = run_queryLite(consultaLite)
            for row in rows:
                EstatusIncidenteDDL.options.append(
                    ft.DropdownOption(
                        key= (str(row[0])),
                        content= ft.Text(str(row[0]))
                    )
                )
            EstatusIncidenteDDL.value = "EN ARRIBO"
        except Exception as er:
            print("Error: ", er)
    

    def tipoVehiculoDDL():
        try:
            consultaLite = 'SELECT Descripcion FROM CatTipoVehiculo WHERE Activo = 1'
            rows = run_queryLite(consultaLite)
            for row in rows:
                TipoVehiculoDDL.options.append(
                    ft.DropdownOption(
                        key= (str(row[0])),
                        content= ft.Text(str(row[0]))                        
                    )
                )
            TipoVehiculoDDL.value = 'AUTOBUS'
        except Exception as ex:
            alerta("Error:", ex)


    def tipoGruaDDL():
        try:
            consultaLite = 'SELECT Descripcion FROM CatTipoGrua'
            rows = run_queryLite(consultaLite)
            for row in rows:
                TipoGruaDDL.options.append(
                    ft.DropdownOption(
                        key= (str(row[0])),
                        content= ft.Text(str(row[0]))
                    )
                )
            TipoGruaDDL.value = "TIPO A"
        except Exception as er:
            print("Error: ", er)

    def cambiotv():
        if TipoVehiculoDDL.value != None:
            if TipoVehiculoDDL.value == 'AUTOBUS':
                tv = ['TIPO B', 'TIPO C']
            if TipoVehiculoDDL.value == 'BICICLETA' or TipoVehiculoDDL.value == 'MOTOCICLETA':
                tv = ['TIPO A']
            if TipoVehiculoDDL.value == 'CAMIONETA' or TipoVehiculoDDL.value == 'VAN':
                tv = ['TIPO A', 'TIPO B', 'TIPO C']
            if TipoVehiculoDDL.value == 'REMOLQUE' or TipoVehiculoDDL.value == 'SEMIREMOLQUE':
                tv = ['TIPO C', 'TIPO D']
            if TipoVehiculoDDL.value == 'TRACTOCAMION': 
                tv = ['TIPO D']
            if TipoVehiculoDDL.value == 'VEHICULO': 
                tv = ['TIPO A', 'TIPO B']
        return tv


    def tipoGruaDDLv2():
        TipoGruaDDL.options=[]
        TipoGruaDDL.key=[]
        lista = []
        tg = cambiotv()
        lista.extend(tg)
        # consultaLite = 'SELECT Descripcion FROM CatTipoGrua'
        # rows = run_queryLite(consultaLite)
        for row in lista:
            TipoGruaDDL.options.append(
                ft.DropdownOption(
                    key= (row),
                    content= ft.Text(row)
                )
            )
        page.update()

    def alerta(titulo, mensaje):
        dlg = ft.AlertDialog(title= ft.Text(titulo), content= ft.Text(mensaje))
        page.open(dlg)

    
    tam =70 #tamaño contenedores dias calendario
    sep = 10 #separacion entre cuadros
    semana = ['Dom','Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab']
    meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']


    colors=[
        "#912743", 
        '#C79B66',
        '#dd1d3e',
        '#B2B2B1', 
        '#4cb185',
        '#17302D', 
        '#861E34', 
        '#E2BE96',
        '#ECECEC', 
        '#246257', 
        "#B33449", 
        '#FFFDED',
        '#e2af72',
        '#3D9B84', 
        '#484747',
        '#c0234c',
        '#ac875b',
        '#26473a',
        '#ede0b8',
        '#898787'
    ]

    def es_color_oscuro(hex_color, umbral=0.4): #Indica si un color hexadecimal es oscuro
        hex_color = hex_color.lstrip('#')
        r_hex, g_hex, b_hex = hex_color[0:2], hex_color[2:4], hex_color[4:6]
        r, g, b = int(r_hex, 16), int(g_hex, 16), int(b_hex, 16)
        h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
        return l < umbral

    global mes
    global anio
    mes = int(datetime.now().month) # mes actual
    anio = int (datetime.now().year) # año actual
   
    din, dfi = calendar.monthrange(anio, mes) # obtiene el dia en que inicia el mes y el total de dias que conforman el mes
    rango=[] # almacena el rango seleccionado
    itemsd=[] # almacen de contenedores para dias de mes
    regdep = [] # almacena caracteristicas y roles de los depositos
    # # # # # # # # # # # # #
    vehiculosInvolucrados = []  # almacena los datos de los vehiculos involucrados
   
    global status_save
    global region_sel

    region_sel = None
    status_save = False
   

    def arranque(): # establece valor para dropdowns de mes y año        
        global mes
        global anio
        drop_mes.value = meses[mes-1]
        drop_anio.value = str(anio)  
        page.update()


    def select_listdep(e):
        ref = ((((e.control.parent).parent).parent).parent).parent
        idd = int(ref.leading.value)
        
        for dep in regdep:
            if dep.iddep == idd:
                dep.fei = ''
                dep.fef = ''
                move_element = dep

                del regdep[regdep.index(dep)]
            
        regdep.append(move_element)
        alerta('Registro Seleccionado', regdep[-1].nom)


    def delete_item(e):
        ref = ((((e.control.parent).parent).parent).parent).parent
        idd = int(ref.leading.value)

        #global mes
        listadep.controls.remove(ref)
        for dep in regdep:
            if dep.iddep == idd: #identifica deposito seleccionado
                #reintegra registro a lista depositos
                drop_depositos.options.append( 
                    ft.DropdownOption(
                        key=str(dep.iddep)+'-'+dep.nom,
                        content=ft.Text(value=str(dep.iddep)+'-'+dep.nom)
                    )
                )
                rehabilita_dias(dep.color, select_day) #rehabilita contenedores bloqueados de rango
                colors.append(dep.color)
                regdep.remove(dep)
        page.update()


    def editar_vehiculo(e):
        ref = (e.control.parent).parent
        idd = int(ref.leading.value)
        # print(idd)
        if idd > 0:
            for vehiculo in vehiculosInvolucrados:
                # print(vehiculo.noVehiculo)
                if int(vehiculo.noVehiculo) == idd:
                    NoVehiculo.value = vehiculo.noVehiculo
                    TipoVehiculoDDL.value = vehiculo.tipoVehiculo
                    TipoGruaDDL.value = vehiculo.tipoGrua
                    SinPlacas.value = vehiculo.sinPlacas
                    print(str(vehiculo.origenPlacasId) + str(vehiculo.origenPlacasNombre))
                    LugarOrigenPlacasDDL.value = str(vehiculo.origenPlacasId) + str(vehiculo.origenPlacasNombre)            
                    NoPlaca.value = vehiculo.noPlacas
                    NoSerie.value = vehiculo.noSerie
                    print(str(vehiculo.marcaId) + '- '+str(vehiculo.marca))
                    MarcaDDL.value = str(vehiculo.marcaId) + '-'+str(vehiculo.marca)                    
                    Linea.value = vehiculo.linea
                    ModeloVehiculo.value = vehiculo.modelo
                    ColorVehIncidente.value = vehiculo.color
                    NombreConductor.value = vehiculo.nombreConductor
                    ApellidosConductor.value = vehiculo.apellidosConductor
                    ObservacionesdelVehiculo.value = vehiculo.observaciones
                    btnVehiculoInvolucradoUpd.visible = True
                    btnVehiculoInvolucradoAdd.visible = False
        page.update()


    def eliminar_vehiculo(e):
        ref = (e.control.parent).parent
        idd = int(ref.leading.value)
        novAct = 0
        posdel = 0 
        for v in range (0, len(vehiculosInvolucrados)):
            novAct += 1
            if int(vehiculosInvolucrados[v].noVehiculo) == idd:
                novAct -= 1
                posdel = v
            vehiculosInvolucrados[v].noVehiculo = novAct
        vehiculosInvolucrados.remove(vehiculosInvolucrados[posdel])             
        vehiculosIncidenteslv.controls.clear() #.remove(ref)
        mosaicos()
        #print('FIN DLE FOR')
        noVehiculoGet() 
        if len(vehiculosInvolucrados) == 0:
            btnAgregarRegistro.visible = False
        page.update()


    def find_dep(depop): # busca la opcion elegida (deposito)
        for dep in drop_depositos.options:
            if depop == dep.key:
                return dep
        return None


    def question_alert(titulo, mensaje, funcionsi, funcion_no):
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(titulo),
            content=ft.Text(mensaje),
            actions=[
                ft.TextButton("Si", on_click= lambda _: funcionsi(dlg), style=button_style),
                ft.TextButton("No", on_click=lambda _: funcion_no(dlg), style=button_style2),
            ]
        )
        page.open(dlg)


    def reg_change(e): # acciones post seleccion de region
        global status_save
        global region_sel
        try:
            ls = (drop_region.value).index('-') 
            idr = int(drop_region.value[:ls]) # extrae id de region
            drop_depositos.options = dep_options(idr)
        except:
            limpiar_control(None)

        if len(regdep) > 0 and status_save == False:
            question_alert(
                'Info',
                'Con esta accción se perderán los cambios ¿Desea continuar?',
                limpiar_control,cancelar_sel
            )
        if len(regdep) == 0 or status_save == True:
            region_sel = drop_region.value
            limpiar_control(None)
            region_sel = drop_region.value
            
        page.update()


    def dep_change(e): # acciones post seleccion de deposito
        color_act = colors[0]
        ls = (drop_depositos.value).index('-') 
        idd = int(drop_depositos.value[:ls]) # extrae id de deposito
        color = color_act # asigna color para seleccion de rango
        nom = drop_depositos.value[ls+1:] # extrae nombre del deposito        
        #eliminar deposito seleccionado de la lista
        opdep = find_dep(drop_depositos.value)
        if opdep != None:
            drop_depositos.options.remove(opdep)
        #agregar deposito a lista regdep
        regdep.append(
            Deposito(color, idd,'','', nom)
        )
        #gestion de depositos seleccionados
        listadep.controls.clear()
        mosaicos = []
        for dep in regdep:
            elemento = ft.ListTile(
                leading=ft.Text(value=str(dep.iddep), color=ft.Colors.TRANSPARENT),
                title=ft.Text(value=dep.nom),
                trailing=ft.Container(
                    width=60,
                    height=30,
                    content=ft.Row(
                        controls=[
                            ft.Column(controls=[
                                ft.Container(
                                    alignment=ft.Alignment(0.0, 0.0),
                                    width=20,
                                    height=20,
                                    bgcolor=dep.color,
                                    shape=ft.BoxShape.CIRCLE,
                                )],
                            ),
                            ft.Column(controls=[
                                ft.PopupMenuButton(
                                    items=[
                                        ft.PopupMenuItem(text='Seleccionar', on_click= select_listdep),
                                        ft.PopupMenuItem(text='Descartar', on_click= delete_item)
                                    ]
                                )]
                            )
                        ]
                    )
                ),
            )
            mosaicos.append(elemento)
        listadep.controls.extend(mosaicos)
        drop_depositos.visible = False
        colors.remove(color_act)
        page.update()
        if len(regdep) == 1:
            alerta('Info', 'Selecciona rango de fechas')

    
    def moth_options(): # desplegable de meses
        options = []
        for m in meses: # consulta a arreglo de meses y los convierte en opcion del desplegable
            options.append(
                ft.DropdownOption(
                    key=m,
                    content=ft.Text(value=m)
                ),
            )
        return options


    def anio_options(): # desplegable de años
        global anio
        anios =[]
        for a in range(anio-5,anio+5): # muestra rango de 10 años
            anios.append(
                ft.DropdownOption(
                    key=a,
                    content=ft.Text(value=(str(a)))
                ),
            )
        return anios


    def dep_options(regionId): # deplegable de depositos
        deps = []
        consultaSql = 'SELECT Id, RazonSocial FROM CatDepositoVehicular WHERE Activo = 1 AND RegionId = ?'
        depositosDb = run_query(consultaSql, (regionId,))
        for dep in depositosDb:
            deps.append(
                ft.DropdownOption(
                    key = (str(dep[0])+'-'+dep[1]),
                    content= ft.Text(str(dep[0])+'-'+dep[1])
                ),
            )
        return deps
    

    def reg_options(): # deplegable de regiones
        regs = []
        consultaSql = 'SELECT Id, NombreRegion FROM CatRegion WHERE Activo = 1'
        regionesDb = run_query(consultaSql)
        for reg in regionesDb:
            regs.append(
                ft.DropdownOption(
                    key = (str(reg[0])+'- '+ reg[1]),
                    content= ft.Text(str(reg[1]))
                ),
            )
        return regs
    

    def select_day(e): # seleccion rango de dias
        global mes
        global anio
        if len(regdep) > 0: # validacion seleccion de deposito
            if regdep[-1].fef == '': # validacion de termino de registro deposito
                if len(rango)<2: # se encarga de identificar rango de dias y lo almacena en una arreglo
                    diasel = e.control.content.value
                    e.control.bgcolor=ft.Colors.GREEN_ACCENT_400
                    e.control.update()
                    rango.append(int(diasel))
                if len(rango)==2: # acciones posteriores a idenrificar el rango
                    if rango[0]<rango[1]: # ordena el rango para identificar inferior y superior
                        inf=rango[0]
                        sup=rango[1]
                    else:
                        inf=rango[1]
                        sup=rango[0]
                    recorrer_hoja(inf,sup,regdep[-1].color, False)
                    regdep[-1].fei = str(inf)+'/'+str(mes)+'/'+str(anio)
                    regdep[-1].fef = str(sup)+'/'+str(mes)+'/'+str(anio)
                    drop_depositos.visible = True
                    rango.clear()
                    page.update()
        else:
            alerta('Info','Debes seleccionar un deposito')


    def on_hover(e): # animacion al colocar cursor sobre contenedores
        if e.control.bgcolor == ft.Colors.BLUE_GREY_500 or e.control.bgcolor == ft.Colors.BLUE_GREY_400:
            e.control.bgcolor = ft.Colors.BLUE_GREY_400 if e.data == 'true' else ft.Colors.BLUE_GREY_500
        e.control.update()


    def recorrer_hoja(din,dfi,color, clickeable): # marca el rango seleccionado
        for dia in itemsd: # recorrido al arreglo de contenedores
            if dia.bgcolor != ft.Colors.TRANSPARENT: # discrimina contenedores vacios
                pos = (int(dia.content.value))
                if pos>=din and pos<=dfi and dia.bgcolor==ft.Colors.BLUE_GREY_500 or dia.bgcolor==ft.Colors.GREEN_ACCENT_400: # marca rango seleccionado
                    dia.bgcolor = color
                    dia.on_click = clickeable
                    if es_color_oscuro(color):
                        (dia.content).color = ft.Colors.WHITE
        page.update()


    def rehabilita_dias(color, clickeable):
        for dia in itemsd:
            if dia.bgcolor == color:
                dia.bgcolor = ft.Colors.BLUE_GREY_500
                dia.on_click = clickeable
        page.update()


    def consulta_rol(region):
        global mes
        global anio
        
        query_rol = 'SELECT * FROM [dbo].[Reg_Roles] WHERE ANIO=? AND MES=? AND regid=? AND act=1'
        listdep = run_query(query_rol, (anio, mes, region,))

        if listdep != None:
            for d in listdep:
                color_act = colors[0]
                
                #eliminar deposito seleccionado de la lista
                opdep = find_dep((str(d[0])+'-'+d[1]))
                if opdep != None:
                    drop_depositos.options.remove(opdep)
                regdep.append(
                    Deposito(color_act, d[0],'Null','Null', d[1])
                )
                
                days = d[2].split(',')
                for dia in itemsd: # recorrido al arreglo de contenedores
                    if dia.bgcolor != ft.Colors.TRANSPARENT: # discrimina contenedores vacios
                        pos = (dia.content.value)
                        if pos in days: # marca rango seleccionado
                            dia.bgcolor = color_act
                            if es_color_oscuro(color_act):
                                (dia.content).color = ft.Colors.WHITE
                        
                colors.remove(color_act)

            ###################################################################
            #gestion de depositos almacenados
            listadep.controls.clear()
            mosaicos = []
            for dep in regdep:
                elemento = ft.ListTile(
                    leading=ft.Text(value=str(dep.iddep), color=ft.Colors.TRANSPARENT),
                    title=ft.Text(value=dep.nom),
                    trailing=ft.Container(
                        width=60,
                        height=30,
                        content=ft.Row(
                            controls=[
                                ft.Column(controls=[
                                    ft.Container(
                                        alignment=ft.Alignment(0.0, 0.0),
                                        width=20,
                                        height=20,
                                        bgcolor=dep.color,
                                        shape=ft.BoxShape.CIRCLE,
                                    )],
                                ),
                                ft.Column(controls=[
                                    ft.PopupMenuButton(
                                        items=[
                                            ft.PopupMenuItem(text='Seleccionar', on_click= select_listdep),
                                            ft.PopupMenuItem(text='Descartar', on_click= delete_item)
                                        ]
                                    )]
                                )
                            ]
                        )
                    ),
                )
                mosaicos.append(elemento)
            listadep.controls.extend(mosaicos)
        
        page.update()
        

    def guardar_rol():
        global status_save
        global anio
        global mes
        global region_sel
        ls = (drop_region.value).index('-') 
        idr = int(drop_region.value[:ls])

        cad_dia = ''
        btn_guardar.disabled=True
        drop_anio.disabled=True
        drop_mes.disabled=True
        drop_region.disabled=True
        drop_depositos.disabled=True
        page.update()
        query_rol = 'SELECT * FROM [DepositoVehicular_DB].[dbo].[Reg_Roles] WHERE ANIO=? AND MES=? AND regid=? AND act=1'
        rolqry = run_query(query_rol, (anio, mes, idr,))

        if rolqry != None:
            for d in rolqry:
                act_rol ='UPDATE [dbo].[DepositosRoles] set [Activo]=0 WHERE [DepositoVehicularId]=? AND [Mes]=? AND [Anio]=?'
                run_query(act_rol,(d[0],mes,anio))
            
        for dep in regdep:
            for dia in itemsd:
                if dia.bgcolor == dep.color:
                    valor = (dia.content.value)
                    if cad_dia == '':
                        cad_dia = valor
                    else:
                        cad_dia = cad_dia+','+valor
            
            insert_rol = '''INSERT INTO [dbo].[DepositosRoles]
                            ([DepositoVehicularId]
                            ,[Anio]
                            ,[Mes]
                            ,[Dias]
                            ,[CreadoPor]
                            ,[FechaCreacion]
                            ,[ActualizadoPor]
                            ,[FechaActualizacion]
                            ,[Activo])
                        VALUES(?,?,?,?,1,getdate(),1,getdate(),1)'''
            run_query(insert_rol,(dep.iddep, anio, mes, cad_dia))
            cad_dia=''
            
        status_save=True
        btn_guardar.disabled=False
        drop_anio.disabled=False
        drop_mes.disabled=False
        drop_region.disabled=False
        drop_depositos.disabled=False
        page.update()
        alerta('AVISO', 'REGISTRO GUARDADO CORRECTAMENTE')


    def head(sem): # encabezado nombre dias
        days = []
        for dia in sem:
            days.append(
                ft.Container(
                    content=ft.Text(value=dia),
                    alignment=ft.Alignment(0.0, 0.0),
                    width=tam,
                    height=2*sep,
                    bgcolor=ft.Colors.BLUE_GREY_300,
                    border_radius=ft.BorderRadius(5,5,5,5),
                )
            )
        return days


    def items(count,di,df): # dibuja los contenedores que muestran los dias del calendario        
        diaini = di+1
        for i in range(1, count + 1): # recorrido para el dibujo de n contenedores (42)
            if di==6: # En caso de que mes inicie en domingo establece el recorrido en la promera posicion
                diaini = 0
                if i>=diaini and (i-(diaini))<=df: # rango dias de mes
                    itemsd.append(
                        ft.Container(
                            content=ft.Text(value=str(i-(diaini))),
                            alignment=ft.Alignment(0.0, 0.0),
                            width=tam,
                            height=tam,
                            bgcolor=ft.Colors.BLUE_GREY_500,
                            border_radius=ft.BorderRadius(5,5,5,5),
                            on_click=select_day,
                            on_hover=on_hover,
                        )
                    )           
            if i<=diaini: # dibuja el contenedor pero no le da valor
                itemsd.append(
                    ft.Container(
                        alignment=ft.Alignment(0.0, 0.0),
                        width=tam,
                        height=tam,
                        bgcolor=ft.Colors.TRANSPARENT,
                    )
                )
            if i>=diaini and (i-(diaini-1))<=df and diaini>0: # se encarga del dibujo de contenedores en caso de no iniciar el mes en domingo
                itemsd.append(
                    ft.Container(
                        content=ft.Text(value=str(i-(diaini-1))),
                        alignment=ft.Alignment(0.0, 0.0),
                        width=tam,
                        height=tam,
                        bgcolor=ft.Colors.BLUE_GREY_500,
                        border_radius=ft.BorderRadius(5,5,5,5),
                        on_click=select_day,
                        on_hover=on_hover,
                    )
                )
        return itemsd #almacena el grupo de contenedores en un arreglo


    dias_sem = ft.Row( # encabezado (dias de la semana) en fila
        wrap=True,
        width=(tam*7)+(sep*6),
        height=(sep+5),
        spacing=sep,
        controls=head(semana)
    )


    hoja = ft.Row( # fila de contenedores (dias del mes)
        wrap=True,
        width=(tam*7)+(sep*6),
        height=600,
        spacing=sep,
        controls=items(42,din,dfi)
    )


    def limpiar_control(dlg): #limpia la lista de depositos y habilita la hoja del calendario
        #seccion calendario
        global mes
        global anio
        global status_save
        mes = (meses.index(drop_mes.value)+1)
        anio = int(drop_anio.value)
        din, dfi = calendar.monthrange(anio, mes)
        itemsd.clear()
        hoja.controls = items(42, din, dfi)
        
        #seccion depositos
        listadep.controls.clear()
        for dep in regdep:       
            colors.append(dep.color)
        regdep.clear()
        status_save = False

        if dlg!=None:
            page.close(dlg)

        if region_sel != None:
            ls = (drop_region.value).index('-') 
            idr = int(drop_region.value[:ls]) # extrae id de region
            consulta_rol(idr)

        page.update()


    def cancelar_sel(dlg):
        global region_sel
        page.close(dlg)
        drop_mes.value = meses[mes-1]
        drop_anio.value = anio
        drop_region.value = region_sel
        page.update()


    dias_sem = ft.Row( # encabezado (dias de la semana) en fila
        wrap=True,
        width=(tam*7)+(sep*6),
        height=(sep+5),
        spacing=sep,
        controls=head(semana)
    )


    drop_mes = ft.Dropdown( # lista deplegable meses
        editable=True,
        options=moth_options(),
        text_align = ft.TextAlign.CENTER,
        on_change=reg_change,
    )


    drop_anio = ft.Dropdown( # listadesplegable años
        editable=True,
        options=anio_options(),
        text_align=ft.TextAlign.CENTER,
        on_change=reg_change,
    )


    drop_depositos = ft.Dropdown( # lista desplegable depositos
        editable=True,
        label='DEPÓSITO:',
        options=[],
        text_align=ft.TextAlign.CENTER,
        width=350,
        on_change=dep_change,        
    )


    drop_region = ft.Dropdown( # lista desplegable regiones
        editable=True,
        label='REGIÓN:',
        # options=reg_options(),
        text_align=ft.TextAlign.CENTER,
        width=350,
        on_change=reg_change,
    )


    mes_lista = ft.Row ( # fila con listas de mes y año
        width=(tam*7)+(sep*6),
        height=100,
        controls=[drop_mes, drop_anio], alignment=ft.MainAxisAlignment.CENTER
    )


    btn_guardar = ft.CupertinoButton(
        content=ft.Text(value='GUARDAR', color=ft.Colors.WHITE, size=15), 
        width=180,
        height=50,
        opacity_on_click=0.3, 
        border_radius=10,
        bgcolor='#3D9B84',
        on_click=lambda _:guardar_rol()
    )


    def limpiarControles():
        # CONTROLES DEL FORMULARIO DE REGION
        regionId.value = ''
        regionNombre.value = ''
        regionActivo.value = False
        # CONTROLES DEL FORMULARIO DE MUNICIPIO
        municipioIdProp.value = ''
        municipioNombreProp.value = ''
        municipioSelectRegion.value = None

        # CONTROLES DEL FORMULARIO DE DEPOSITOS
        Id.value = ''
        RazonSocial.value = ''
        RepresentanteLegal.value = ''
        municipioSelectRegion.value = None
        DireccionDeposito.value = ''
        NombreCompletoContactos.value = ''
        CorreoElectronicoContacto.value = ''
        Telefonos.value = ''
        Latitud.value = ''
        Longitud.value = ''
        Ubicacion.value = ''
        Activo.value = True
        

    def limpiarControlesIncidentes():
        Vialidad.value = ''
        Colonia.value = ''
        UbicacionIncidente.value = ''
        CambioDDL.visible = False
        Referencia.value = ''
        DepositoDDL.options = []
        DepositoDDL.key = []
        # DepositoDDL.options = depositosIncidentesDropDownList()
        RegionTxt.value = False
        RespondienteNombreCompleto.value = ''
        RespondienteIdentificacion.value = ''
        NotaRespondiente.value = ''
        Folio911.value = ''
        page.update()


    def limpiarControlesVehiculosInci():
        NoVehiculo.value = ''
        SinPlacas.value = False        
        NoPlaca.value = ''
        Linea.value = ''
        NoSerie.value = ''
        ColorVehIncidente.value = ''
        NombreConductor.value = ''
        ApellidosConductor.value = ''
        ModeloVehiculo.value = ''
        ObservacionesdelVehiculo.value = ''
        MarcaDDL.options = []
        marcasVehiculosDropDownList()
        noVehiculoGet()        
        page.update()


    def botonesAgregar():        
        btnAgregarRegistro.disabled =  False
        btnEditarRegistro.disabled = False
        btnAgregarRegistro.visible =  True
        btnEditarRegistro.visible = False
        btnCancelarAccionForm.visible = False
        regionActivo.visible = False
        Activo.visible = False  
        FolioIncidente.visible = False
        page.update()


    def botonesEditar():
        btnAgregarRegistro.visible = False
        btnEditarRegistro.visible = True
        btnCancelarAccionForm.visible = True
        regionActivo.visible = True
        FolioIncidente.visible = True
        page.update()    
    

    def botonesCancelarAccionForm():
        limpiarControles()
        botonesAgregar()
        page.update()


    def validarDatosIncidente():
        tipoIncidenteValor = TipoIncidenteDDL.value
        estatusIncidenteValor = EstatusIncidenteDDL.value
        municipioDLLValor = municipioIncidenteSeleccionado()
        depositoDLLValor = depositoIncidenteSeleccionado()
        respondienteNombreValor = RespondienteNombreCompleto.value.strip()
        respondienteIdentificacionValor = RespondienteIdentificacion.value.strip()
        
        if(tipoIncidenteValor.strip() != '' and 
           Vialidad.value.strip() != '' and 
           Colonia.value.strip() != '' and 
           UbicacionIncidente.value.strip() != '' and 
           int(municipioDLLValor) > 0 and 
           int(depositoDLLValor) > 0 and
           len(respondienteNombreValor) > 10 and
           len(respondienteIdentificacionValor) > 3 and
           estatusIncidenteValor != ''):
            noVehiculoGet()
            agregarVehiculoMostrarControles()
        else:
            alerta('AVISO', 'FALTAN CAMPOS POR LLENAR')
    

    def incidenteMostrarControles():
        IdIncidente.visible = True
        TipoIncidenteDDL.visible = True        
        FechaIncidente.visible = True
        HoraIncidente.visible = True
        Vialidad.visible = True
        Colonia.visible = True
        Referencia.visible = True
        MunicipioDDL.visible = True
        CambioDDL.visible = True
        btn_buscaub.visible = True
        RegionTxt.visible = True
        DepositoDDL.visible = True
        Latitud.visible = True
        Longitud.visible = True
        UbicacionIncidente.visible = True
        RespondienteNombreCompleto.visible = True
        RespondienteIdentificacion.visible = True
        NotaRespondiente.visible = True
        Folio911.visible = True
        EstatusIncidenteDDL.visible = True
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        IdVehiculoIncidente.visible = False
        FolioIncidente.visible = False
        NoVehiculo.visible = False        
        TipoVehiculoDDL.visible = False
        TipoGruaDDL.visible = False
        SinPlacas.visible = False
        LugarOrigenPlacasDDL.visible = False
        NoPlaca.visible = False
        NoSerie.visible = False
        ColorVehIncidente.visible = False
        MarcaDDL.visible = False
        Linea.visible = False
        ModeloVehiculo.visible = False
        NombreConductor.visible = False
        ApellidosConductor.visible = False
        ObservacionesdelVehiculo.visible = False
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        btnAgregarVehiculoIncidente.visible = True
        btnDatosIncidente.visible = False
        btnVehiculoInvolucradoAdd.visible = False
        btnAgregarRegistro.visible = False
        page.update()


    def agregarVehiculoMostrarControles():
        IdIncidente.visible = False
        TipoIncidenteDDL.visible = False        
        FechaIncidente.visible = False
        HoraIncidente.visible = False
        Vialidad.visible = False
        Colonia.visible = False
        Referencia.visible = False
        MunicipioDDL.visible = False
        RegionTxt.visible = False
        CambioDDL.visible = False
        btn_buscaub.visible = False
        DepositoDDL.visible = False
        Latitud.visible = False
        Longitud.visible = False
        UbicacionIncidente.visible = False
        RespondienteNombreCompleto.visible = False
        RespondienteIdentificacion.visible = False
        NotaRespondiente.visible = False
        Folio911.visible = False
        EstatusIncidenteDDL.visible = False
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        IdVehiculoIncidente.visible = True
        FolioIncidente.visible = False # # # SOLO SERA VISIBLE AL EDITAR
        NoVehiculo.visible = True
        TipoVehiculoDDL.visible = True
        TipoGruaDDL.visible = True
        SinPlacas.visible = True 
        LugarOrigenPlacasDDL.visible = True       
        NoPlaca.visible = True
        NoSerie.visible = True
        ColorVehIncidente.visible = True
        MarcaDDL.visible = True
        Linea.visible = True
        ModeloVehiculo.visible = True
        NombreConductor.visible = True
        ApellidosConductor.visible = True
        ObservacionesdelVehiculo.visible = True
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        btnAgregarVehiculoIncidente.visible = False # PARA MOSTRAR ESTOS CONTROLES
        btnDatosIncidente.visible = True  # PARA CAMBIAR A LOS CONTROLES DEL FORMULARIO DE INCIDENE
        btnVehiculoInvolucradoAdd.visible = True  # PARA AGREGAR A LA LISTA
        btnAgregarRegistro.visible = False
        if len(vehiculosInvolucrados) > 0:
            btnAgregarRegistro.visible = True
        page.update()


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # LIST VIEW PARA MOSTRAR LAS REGIONES
    lv = ft.ListView(spacing=5, auto_scroll=True, expand=1)
    listadep = ft.ListView(spacing=5, auto_scroll=True, width=400)
    incidenteslv = ft.ListView(spacing=10, auto_scroll= True, width=750)
    EstatusIncidenteslv = ft.ListView(spacing=10, auto_scroll= True, width=750)
    incidentesreplv = ft.ListView(spacing=20, auto_scroll= True, width=1900)
    vehiculosIncidenteslv = ft.ListView(spacing=5, auto_scroll= True, width=550)


    lista_regiones = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('ID')),
            ft.DataColumn(ft.Text('REGIÓN')),
            ft.DataColumn(ft.Text('DISPONIBLE'))
        ], rows=[],
    )


    lista_municipios = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('ID')),
            ft.DataColumn(ft.Text('MUNICIPIO')),
            ft.DataColumn(ft.Text('REGIÓN'))
        ], rows=[]
    ) 


    lista_depositos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('ID')),
            ft.DataColumn(ft.Text('RAZÓN SOCIAL')),
            ft.DataColumn(ft.Text('REPRESENTANTE LEGAL')),
            ft.DataColumn(ft.Text('DIRECCIÓN')),
            ft.DataColumn(ft.Text('REGIÓN')),
            ft.DataColumn(ft.Text('TELEFONOS'))
        ], rows=[]
    )


    lista_incidentes = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('ID')),
            ft.DataColumn(ft.Text('TIPO DE INCIDENTE')),
            ft.DataColumn(ft.Text('FOLIO')),
            ft.DataColumn(ft.Text('FECHA')),
            ft.DataColumn(ft.Text('VIALIDAD')),
            ft.DataColumn(ft.Text('COLONIA')),
            ft.DataColumn(ft.Text('UBICACIÓN (LINK MAPS)')),
            ft.DataColumn(ft.Text('ESTATUS')),
            ft.DataColumn(ft.Text('MUNICIPIO')),
            ft.DataColumn(ft.Text('RAZÓN SOCIAL')),
            ft.DataColumn(ft.Text('INVOLUCRADOS'))
        ], rows=[]
    )

    lista_incidentesrep = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('FOLIO')),
            ft.DataColumn(ft.Text('TIPO DE INCIDENTE')),
            ft.DataColumn(ft.Text('FECHA')),
            ft.DataColumn(ft.Text('VIALIDAD')),
            ft.DataColumn(ft.Text('COLONIA')),
            ft.DataColumn(ft.Text('REFERENCIA')),
            ft.DataColumn(ft.Text('UBICACIÓN (LINK MAPS)')),
            ft.DataColumn(ft.Text('RESPONDIENTE')),
            ft.DataColumn(ft.Text('ESTATUS')),
            ft.DataColumn(ft.Text('MUNICIPIO')),
            ft.DataColumn(ft.Text('REGIÓN')),
            ft.DataColumn(ft.Text('DEPÓSITO'))
        ], rows=[]
    )

    lista_estatusIncidentes = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('ID')),
            ft.DataColumn(ft.Text('FOLIO')),
            ft.DataColumn(ft.Text('TIPO DE INCIDENTE')),
            ft.DataColumn(ft.Text('ESTATUS')),
            ft.DataColumn(ft.Text('FECHA Y HORA')),
            ft.DataColumn(ft.Text('VIALIDAD')),
            ft.DataColumn(ft.Text('COLONIA')),
            ft.DataColumn(ft.Text('MUNICIPIO')),
            ft.DataColumn(ft.Text('DEPÓSITO')),
            ft.DataColumn(ft.Text('RESPONDIENTE'))
        ]
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
            consultaSql = 'SELECT cmun.[Id],UPPER([Municipio]),creg.NombreRegion FROM [CatMunicipio] cmun INNER JOIN CatRegion creg ON cmun.RegionId = creg.Id ORDER BY creg.NombreRegion'
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
                         ,cr.NombreRegion
                         ,Telefonos
                     FROM CatDepositoVehicular cdv 
               INNER JOIN CatRegion cr ON cdv.RegionId = cr.Id ORDER BY cr.NombreRegion'''
        depositosDb = run_query(consultaSql)
        lv.controls.clear()
        lv.controls.append(lista_depositos)
        generar_tabla_depositos(depositosDb)
        page.update()

    def depositosBuscaLista():# busqueda en lista de municipios
        if municipioSelectRegion.value == None and len(RazonSocial.value) == 0 and len(RepresentanteLegal.value)==0:
            alerta('AVISO', 'No hay criterios de busqueda')
        else:
            if RazonSocial.value == '' and RepresentanteLegal.value=='':
                consultaSql = '''SELECT cdv.Id
                                        ,RazonSocial
                                        ,RepresentanteLegal
                                        ,DireccionDeposito
                                        ,cr.NombreRegion
                                        ,Telefonos
                                    FROM CatDepositoVehicular cdv 
                                INNER JOIN CatRegion cr ON cdv.RegionId = cr.Id
                                WHERE  RegionId = ?'''
                ls = (municipioSelectRegion.value).find('-')
                idr = int(municipioSelectRegion.value[:ls])
                depositosDb = run_query(consultaSql,(int(idr),))
                lv.controls.clear()
                lv.controls.append(lista_depositos)
                generar_tabla_depositos(depositosDb)
            else:
                consultaSql = '''SELECT cdv.Id
                                        ,RazonSocial
                                        ,RepresentanteLegal
                                        ,DireccionDeposito
                                        ,cr.NombreRegion
                                        ,Telefonos
                                    FROM CatDepositoVehicular cdv 
                                INNER JOIN CatRegion cr ON cdv.RegionId = cr.Id
                                WHERE RazonSocial LIKE '%'''+RazonSocial.value+'''%' OR RepresentanteLegal LIKE '%'''+RepresentanteLegal.value+'''%' OR RegionId = ?'''
                ls = (municipioSelectRegion.value).find('-')
                idr = int(municipioSelectRegion.value[:ls])
                depositosDb = run_query(consultaSql,(int(idr),))
                lv.controls.clear()
                lv.controls.append(lista_depositos)
                generar_tabla_depositos(depositosDb)

            page.update()

    def depositosBuscaListaReg():# busqueda en lista de muni
        if municipioSelectRegion.value == None:
            alerta('AVISO', 'No hay criterios de busqueda')
        else:
            consultaSql = 'SELECT cmun.[Id],UPPER([Municipio]),creg.NombreRegion FROM [CatMunicipio] cmun INNER JOIN CatRegion creg ON cmun.RegionId = creg.Id WHERE RegionId=?'
            ls = (municipioSelectRegion.value).find('-')
            idr = int(municipioSelectRegion.value[:ls])
            depositosDb = run_query(consultaSql,(int(idr),))
            lv.controls.clear()
            lv.controls.append(lista_municipios)
            generar_tabla_municipios(depositosDb)
            page.update()


    def incidentesLista(anio):
        consutaSql = ''' SELECT inc.Id,
                                TipoIncidente
                                ,RIGHT('000'+CAST(FolioIncidente AS VARCHAR(3)),3) AS FolioInciden
                                ,CONVERT(varchar(20), FechaIncidente, 120) as FechaIncidente
                                ,UPPER(VialidadIncidente) AS VialidadIncidente
                                ,upper(ColoniaIncidente) AS ColoniaIncidente
                                ,UbicacionIncidente
                                ,EstatusIncidente
                                ,cmu.Municipio
                                ,cdep.RazonSocial 
                                ,CONVERT(NVARCHAR(10) , [dbo].[uf_CantVehiculosIncidentes](inc.Id)) + ' UNIDAD(ES) INVOLUCRADA(S) ' as Cant
                            FROM Incidentes inc
                    INNER JOIN CatMunicipio cmu ON inc.MunicipioId = cmu.Id
                    INNER JOIN CatDepositoVehicular cdep ON inc.DepositoVehicularId = cdep.Id
                        WHERE YEAR(inc.FechaIncidente) = ?'''
        incidentesDb = run_query(consutaSql, (anio,))
        incidenteslv.controls.clear()
        incidenteslv.controls.append(lista_incidentes)
        generar_tabla_incidentes(incidentesDb)
        page.update()

    def incidentesRepLista(dato, idfiltro):
        if idfiltro == 1:
            consultaSql = 'SELECT FolioIncidente, TipoIncidente, FechaIncidente, VialidadIncidente, ColoniaIncidente, ReferenciaUbicacionIncidente, UbicacionIncidente, RespondienteNombreCompleto, EstatusIncidente, Municipio, NombreRegion, RazonSocial FROM Incidentes, CatMunicipio, CatRegion, CatDepositoVehicular WHERE MunicipioId=CatMunicipio.Id AND Incidentes.RegionId = CatRegion.Id AND DepositoVehicularId = CatDepositoVehicular.Id AND EstatusIncidente = ?'
        if idfiltro == 2:
            ls = (FiltroIncidentesDepDDL.value).find('-')
            iddep = int(FiltroIncidentesDepDDL.value[:ls])
            dato = iddep
            consultaSql = 'SELECT FolioIncidente, TipoIncidente, FechaIncidente, VialidadIncidente, ColoniaIncidente, ReferenciaUbicacionIncidente, UbicacionIncidente, RespondienteNombreCompleto, EstatusIncidente, Municipio, NombreRegion, RazonSocial FROM Incidentes, CatMunicipio, CatRegion, CatDepositoVehicular WHERE MunicipioId=CatMunicipio.Id AND Incidentes.RegionId = CatRegion.Id AND DepositoVehicularId = CatDepositoVehicular.Id AND DepositoVehicularId = ?'
        if idfiltro == 3:
            ls = dato.find('-')
            idreg = int(dato[:ls])
            dato = idreg
            consultaSql = 'SELECT FolioIncidente, TipoIncidente, FechaIncidente, VialidadIncidente, ColoniaIncidente, ReferenciaUbicacionIncidente, UbicacionIncidente, RespondienteNombreCompleto, EstatusIncidente, Municipio, NombreRegion, RazonSocial FROM Incidentes, CatMunicipio, CatRegion, CatDepositoVehicular WHERE MunicipioId=CatMunicipio.Id AND Incidentes.RegionId = CatRegion.Id AND DepositoVehicularId = CatDepositoVehicular.Id AND Incidentes.RegionId = ?'
        if idfiltro == 4:
            consultaSql = 'SELECT FolioIncidente, TipoIncidente, FechaIncidente, VialidadIncidente, ColoniaIncidente, ReferenciaUbicacionIncidente, UbicacionIncidente, RespondienteNombreCompleto, EstatusIncidente, Municipio, NombreRegion, RazonSocial FROM Incidentes, CatMunicipio, CatRegion, CatDepositoVehicular WHERE MunicipioId=CatMunicipio.Id AND Incidentes.RegionId = CatRegion.Id AND DepositoVehicularId = CatDepositoVehicular.Id AND TipoIncidente = ?'
        incidentesDb = run_query(consultaSql, (dato,))
        incidentesreplv.controls.clear()
        incidentesreplv.controls.append(lista_incidentesrep)
        generar_tabla_incidentesrep(incidentesDb)
        page.update()

    def estatusIncidenteLista(anio):
        #consultaSql = 'SELECT FolioIncidente, TipoIncidente, FechaIncidente, VialidadIncidente, ColoniaIncidente, ReferenciaUbicacionIncidente, UbicacionIncidente, RespondienteNombreCompleto, RespondienteIdentificacion, RespondienteNotas, Municipio, NombreRegion, RazonSocial, MunicipioId, Incidentes.RegionId, DepositoVehicularId FROM Incidentes, CatMunicipio, CatRegion, CatDepositoVehicular WHERE MunicipioId=CatMunicipio.Id AND Incidentes.RegionId = CatRegion.Id AND DepositoVehicularId = CatDepositoVehicular.Id AND EstatusIncidente = ?'
        consultaSql = ''' SELECT inc.Id
                                ,RIGHT('000'+CAST(FolioIncidente AS VARCHAR(3)),3) AS FolioInciden		  
                                ,TipoIncidente
                                ,inc.EstatusIncidente
                                ,UPPER(CONVERT(VARCHAR(16), FechaIncidente, 120)) AS FechaIncidente
                                ,UPPER(VialidadIncidente) AS VialidadIncidente
                                ,UPPER(ColoniaIncidente) AS ColoniaIncidente 
                                ,UPPER(cmu.Municipio) AS Municipio
                                ,cdv.RazonSocial
                                ,inc.RespondienteNombreCompleto
                            FROM Incidentes inc
                        INNER JOIN CatMunicipio cmu ON inc.MunicipioId = cmu.Id
                        INNER JOIN CatDepositoVehicular cdv ON inc.DepositoVehicularId = cdv.Id 
                            WHERE YEAR(FechaIncidente) = ?'''
        incidentesEstatus = run_query(consultaSql, (int(anio),))
        EstatusIncidenteslv.controls.clear()
        EstatusIncidenteslv.controls.append(lista_estatusIncidentes)
        generar_Tabla_EstatusIncidente(incidentesEstatus)
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
                                ,cr.Id
                                ,UPPER(cr.NombreRegion)
                                ,Latitud
                                ,Longitud
                                ,Ubicacion
                                ,cdv.Activo
                                ,CreadoPorAdminId
                                ,FechaCreacion
                                ,ActualizadoPorAdminId
                                ,FechaActualizacion
                            FROM CatDepositoVehicular cdv 
                      INNER JOIN CatRegion cr ON cdv.RegionId = cr.Id
                            WHERE cdv.Id = ?'''
        depositoDB = run_query(consultaSql, (IdSeleccionado,))
        Id.value = str(depositoDB[0][0])
        RazonSocial.value = str(depositoDB[0][1])
        RepresentanteLegal.value = str(depositoDB[0][2])
        CorreoElectronicoContacto.value = str(depositoDB[0][3])
        NombreCompletoContactos.value = str(depositoDB[0][4])
        Telefonos.value = str(depositoDB[0][5])
        DireccionDeposito.value = str(depositoDB[0][6])
        municipioSelectRegion.value = str(depositoDB[0][7])+ '- ' + str(depositoDB[0][8])
        Latitud.value = str(depositoDB[0][9])
        Longitud.value = str(depositoDB[0][10])
        Ubicacion.value = str(depositoDB[0][11])
        Activo.value = bool(depositoDB[0][12])
        botonesEditar()
        page.update()


    def selectedrowEstatusIncidentes(e):
        IdSeleccionado = int(e.control.cells[0].content.value)
        print(IdSeleccionado)
        pass


    def generar_tabla(filas):
        rows = []
        for fila in filas:
            cells = [] 
            for col in fila:
                if (col == True or col == False) and len(cells)>0:
                    cells.append(ft.DataCell(content=ft.Checkbox(value=col, disabled=True)))
                else:
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


    def generar_tabla_incidentes(filas):
        rows = []
        for fila in filas:
            cells = []
            for col in fila:
                cells.append(ft.DataCell(ft.Text(col)))
            rows.append(ft.DataRow(cells=cells, )) # on_select_changed=selectedrowDepositos
        lista_incidentes.rows = rows
        page.update()

    def generar_tabla_incidentesrep(filas):
        rows = []
        for fila in filas:
            cells = []
            for col in fila:
                cells.append(ft.DataCell(ft.Text(col)))
            rows.append(ft.DataRow(cells=cells, )) # on_select_changed=selectedrowDepositos
        lista_incidentesrep.rows = rows
        page.update()

    
    def generar_Tabla_EstatusIncidente(filas):
        rows = []
        for fila in filas:
            cells = []
            for col in fila:
                cells.append(ft.DataCell(ft.Text(col)))
            rows.append(ft.DataRow(cells=cells, on_select_changed=selectedrowEstatusIncidentes)) # on_select_changed=selectedrowDepositos
        lista_estatusIncidentes.rows = rows
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


    def regionIncidenteSeleccionado():
        try:
            textoSeleccionado = RegionTxt.value
            posicion = textoSeleccionado.find('-')
            if posicion != -1:
                valor = textoSeleccionado[:posicion]
                return valor
            else:
                return 0
        except:
            return 0


    def municipioIncidenteSeleccionado():
        try:
            textoSeleccionado = MunicipioDDL.value
            posicion = textoSeleccionado.find('-')
            if posicion != -1:
                valor = textoSeleccionado[:posicion]
                regionDescripcion(valor)
                return valor
            else:
                return 0
        except:
            return 0
        

    def anioGetSeleccionado():
        try:
            # print(FechaIncidente.value)
            textoSeleccionado = FechaIncidente.value
            posicion = textoSeleccionado.find('-')
            # print(posicion)
            if posicion != -1:
                valor = textoSeleccionado[:posicion]
                print('anioGetSeleccionado')
                print(valor)
                return valor
            else:
                return 0
        except:
            return 0

    
    def depositoIncidenteSeleccionado():
        try:
            textoSeleccionado = DepositoDDL.value
            posicion = textoSeleccionado.find('-')
            if posicion != -1:
                valor = textoSeleccionado[:posicion]
                return valor
            else:
                return 0
        except:
            return 0


    def tipoVehiculoSeleccionado():
        tipoGruaDDLv2() #validacion tipo de grua
        try:
            textoSeleccionado = TipoVehiculoDDL.value
            if(textoSeleccionado == "BICICLETA"):
                    #TipoGruaDDL.value = 'N/A'
                    SinPlacas.disabled = True
                    SinPlacas.value = True
                    # LugarOrigenPlacasDDL.options = []
                    # LugarOrigenPlacasDDL.key = []                    
                    LugarOrigenPlacasDDL.value = '33- N/A'
                    LugarOrigenPlacasDDL.disabled = True
                    NoPlaca.value = 'NO APLICA'
                    NoPlaca.disabled = True
                    NoSerie.value = 'NO APLICA'
                    NoSerie.disabled = True
                    MarcaDDL.options = []
                    MarcaDDL.key = []
                    MarcaDDL.disabled = True
                    Linea.value = 'NO APLICA'
                    Linea.disabled = True
                    ModeloVehiculo.value = 'NO APLICA'
                    ModeloVehiculo.disabled = True
                    NombreConductor.value = 'NO APLICA'
                    # NombreConductor.disabled = True
                    ApellidosConductor.value = 'NO APLICA'
                    # ApellidosConductor.disabled = True
                    page.update()
            if(textoSeleccionado != "BICICLETA"):
                    SinPlacas.disabled = False                    
                    LugarOrigenPlacasDDL.disabled = False
                    LugarOrigenPlacasDDL.options= []
                    lugarOrigenPlacasDropDownList()
                    NoPlaca.disabled = False
                    NoSerie.disabled = False
                    MarcaDDL.disabled = False
                    MarcaDDL.options = []
                    marcasVehiculosDropDownList()
                    Linea.disabled = False
                    ModeloVehiculo.disabled = False
                    NombreConductor.disabled = False
                    ApellidosConductor.disabled = False
                    page.update()
        except:
            return 0
    

    def marcaIdSeleccionado():
        try:
            textoSelect = MarcaDDL.value
            posicion = textoSelect.find('-')
            if posicion != -1:
                valor = textoSelect[:posicion]
                return valor
            else:
                return 0
        except:
            return 0


    def origenPlacasSeleccionado():
        try:
            textoSelect = LugarOrigenPlacasDDL.value
            posicion = textoSelect.find('-')
            if posicion != -1:
                valor = textoSelect[:posicion]
                return valor
            else:
                return 0
        except:
            return 0


    def origenPlacasNombreSeleccionado():
        try:
            textoSelect = LugarOrigenPlacasDDL.value
            posicion = textoSelect.find('-')
            if posicion != -1:
                valor = textoSelect[posicion:]
                return valor
            else:
                return ''
        except:
            return ''


    def regionDescripcion(municipioId):
        dia = str((datetime.now()).day)
        querydeps = 'SELECT Id, RazonSocial FROM CatDepositoVehicular WHERE RegionId=?'
        consultaSql = "SELECT RegionId FROM CatMunicipio WHERE Id = ?"
        regionId = run_query(consultaSql, (municipioId,))
        consultaSql = "SELECT CONVERT(NVARCHAR(120), [Id]) + '-' +  [NombreRegion], Id FROM [CatRegion] WHERE Id = ?"
        nombreRegion = run_query(consultaSql, (regionId[0][0],))  
        RegionTxt.value = nombreRegion[0][0]
        DepositoDDL.options=[]
        querydepturno = "SELECT Dep, Nombre FROM Reg_Roles WHERE act=1 AND mes=MONTH(GETDATE()) AND anio=YEAR(GETDATE()) AND regid=? and SUBSTRING(Listadia, 1,3) LIKE '%"+dia+",%' OR act=1 AND mes=MONTH(GETDATE()) AND anio=YEAR(GETDATE()) AND regid=? and Listadia LIKE '%,"+dia+",%' OR act=1 AND mes=MONTH(GETDATE()) AND anio=YEAR(GETDATE()) AND regid=? and Listadia LIKE '%,"+dia+"%'"
        depturno = run_query(querydepturno, (str(nombreRegion[0][1]), str(nombreRegion[0][1]), str(nombreRegion[0][1])))
        if depturno:
            depositosIncidentesDropDownList(querydeps,nombreRegion[0][1])
            DepositoDDL.value = str(depturno[0][0])+'-'+depturno[0][1]
            CambioDDL.visible = True
        else:
            DepositoDDL.key=[]
            depositosIncidentesDropDownList(querydeps,nombreRegion[0][1])
            CambioDDL.visible = False
        page.update()


    def filtroIncideneAnioSeleccionado():
        try:
            textoSelect = FiltroIncidentesAnioDDL.value
            incidentesLista(int(textoSelect))
        except:
            return 0
        
    
    def filtroEstatusIncideneAnioSeleccionado():
        try:
            textoSelect = FiltroEstatusIncidentesAnioDDL.value
            estatusIncidenteLista(textoSelect)
        except:
            return 0
    
    def filtroStatusIncideneAnioSeleccionado(filtro, idfiltro):
        try:
            textoSelect = filtro.value
            incidentesRepLista(textoSelect, idfiltro)
        except:
            return 0
        

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
    

    def municipiosIncidentesDropDownList():
        consultaSql = 'SELECT Id, Municipio  FROM CatMunicipio ORDER BY Municipio'
        regionesLst = run_query(consultaSql)        
        for row in regionesLst:
            MunicipioDDL.options.append(
                ft.DropdownOption(
                    key = (str(row[0])+'- '+row[1]),
                    content= ft.Text(                        
                        str(row[1])
                    )
                )                
            )
        page.update()


    def depositosIncidentesDropDownList(consultaSql, idreg):
        depositosLst = run_query(consultaSql,(idreg,))
        for row in depositosLst:
            DepositoDDL.options.append(
                ft.DropdownOption(
                    key= (str(row[0])+ '-' + row[1]),
                    content= ft.Text(
                        str(row[1])
                    )
                )
            )
        page.update()
        

    def marcasVehiculosDropDownList():
        consultaSql = 'SELECT Id, Marca FROM CatMarcasVehiculos WHERE Activo = 1 ORDER BY Marca'
        marcasVeh = run_query(consultaSql)
        for row in marcasVeh:
            MarcaDDL.options.append(
                ft.DropdownOption(
                    key= (str(row[0])+ '- ' + row[1]),
                    content= ft.Text(
                        str(row[1])
                    )
                )
            )


    def lugarOrigenPlacasDropDownList():
        consultaSql = 'SELECT Id, UPPER(Estado) FROM Estados'
        estados = run_query(consultaSql)
        for row in estados:
            LugarOrigenPlacasDDL.options.append(
                ft.DropdownOption(
                    key= (str(row[0])+ '- ' + row[1]),
                    content= ft.Text(
                        str(row[1])
                    )                    
                )
            )
        LugarOrigenPlacasDDL.value = "21- PUEBLA"


    def filtroIncidenteAniosDropDownList():
        consultaSql = 'SELECT DISTINCT(YEAR(FechaIncidente)) AS ANIOS FROM Incidentes WHERE Activo = 1'
        anios = run_query(consultaSql)
        for row in anios:
            FiltroIncidentesAnioDDL.options.append(
                ft.DropdownOption(
                    key= (str(row[0])),
                    content= ft.Text(str(row[0]))
                )
            )
    ################# drops reportes
    def filtroIncidenteStatusDropDownList():
        # consultaSql = 'SELECT DISTINCT(YEAR(FechaIncidente)) AS ANIOS FROM Incidentes WHERE Activo = 1'
        # anios = run_query(consultaSql)
        status = ['EN ARRIBO','MANIOBRA','CUSTODIA','TRASLADO','DEPÓSITO','LIBERADO']
        for row in status:
            FiltroIncidentesStatusDDL.options.append(
                ft.DropdownOption(
                    key= row,
                    content= ft.Text(row)
                )
            )

    def filtroIncidenteDepDropDownList():
        consultaSql = 'SELECT Id, RazonSocial FROM CatDepositoVehicular'
        anios = run_query(consultaSql)
        for row in anios:
            FiltroIncidentesDepDDL.options.append(
                ft.DropdownOption(
                    key= (str(row[0])+'-'+row[1]),
                    content= ft.Text(str(row[0])+'-'+row[1])
                )
            )

    def filtroIncidenteRegDropDownList():
        consultaSql = 'SELECT Id, NombreRegion FROM CatRegion'
        anios = run_query(consultaSql)
        for row in anios:
            FiltroIncidentesRegDDL.options.append(
                ft.DropdownOption(
                    key= (str(row[0])+'-'+row[1]),
                    content= ft.Text(str(row[0])+'-'+row[1])
                )
            )
    
    def filtroIncidenteTIDropDownList():
        Tipo_Inc = ['FALTA ADMINISTRATIVA', 'HECHO DELICTIVO', 'INCIDENTE DE TRANSITO']
        for row in Tipo_Inc:
            FiltroIncidentesTIDDL.options.append(
                ft.DropdownOption(
                    key= (row),
                    content= ft.Text(row)
                )
            )
    
    def filtroEstatusIncidenteAniosDropDownList():
        consultaSql = 'SELECT DISTINCT(YEAR(FechaIncidente)) AS ANIOS FROM Incidentes WHERE Activo = 1'
        anios = run_query(consultaSql)
        for row in anios:
            FiltroEstatusIncidentesAnioDDL.options.append(
                ft.DropdownOption(
                    key= (str(row[0])),
                    content= ft.Text(str(row[0]))
                )
            )


    def noVehiculoGet():
        NoVehiculoSig = len(vehiculosInvolucrados)
        NoVehiculo.value = str(NoVehiculoSig + 1).zfill(3)
        page.update()


    def marcaVehiculoGet():
        try:
            textoSeleccionado = MarcaDDL.value
            posicion = textoSeleccionado.find('-')
            if posicion != -1:
                valor = textoSeleccionado[posicion+1:]
                return valor
            else:
                return 0
        except:
            return ''


    def vehiculoSinPlacasCheck(e):
        if e.data == 'true':
            LugarOrigenPlacasDDL.value = "33- N/A"
            LugarOrigenPlacasDDL.disabled = True
            NoPlaca.value = 'NO APLICA'
            NoPlaca.disabled = True            
        if e.data == 'false':
            LugarOrigenPlacasDDL.disabled = False            
            lugarOrigenPlacasDropDownList()
            NoPlaca.disabled = False
            NoPlaca.value = ''
        page.update()  


    def recdelete(elemento, lista): #elimina todos los elementos indicados
        if elemento in lista:  
            lista.remove(elemento) #elimina el primer resultado del elemento en la lista
            recdelete(elemento, lista) #Elimina hasta que ya no exista el elemento indicado
        return lista #devuelve la lista limpia
    

    def valid_lon(e, objeto):
        if len(e.control.value) > 7:
            objeto.disabled=False
        else:
            objeto.disabled=True
        objeto.update()


    def cmbdep_No(dlg): #opcion cancelar cambio deposito
        CambioDDL.value=True
        page.close(dlg)
        page.update()


    def cmbdep_Si(dlg, dep): #asigna siguiente deposito en rol
        global diasm
        if len(diasm) == 0:
            diasm = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
            queryddep = 'SELECT Dep, Listadia FROM Reg_Roles WHERE act=1 AND mes=MONTH(GETDATE()) AND anio=YEAR(GETDATE()) AND regid=?'
            ls = (RegionTxt.value).find('-')
            reg = RegionTxt.value[:ls]
            listdias = run_query(queryddep,(reg))
            for elemento in listdias:
                dias = elemento[1].split(',')
                for dia in dias:
                    diasm[int(dia)-1] = elemento[0]
            dia = (datetime.now()).day
            diasm = recdelete('',diasm)[dia-1:]
            diasm = recdelete(dep,diasm)
        else:
            diasm = recdelete(dep,diasm)
        
        try:
            query_depsup = 'SELECT Id, RazonSocial FROM CatDepositoVehicular WHERE Id = ?'
            inasists.insert(0,Inasistencia(dep, notaCambio.value))
            notaCambio.value=''
            depsup = run_query(query_depsup,(diasm[0]))
            DepositoDDL.value = str(depsup[0][0])+'-'+depsup[0][1]
            CambioDDL.value=True
        except:
            alerta('AVISO', 'No hay mas depositos disponibles')
        page.close(dlg)
        page.update()


    def cambioDep(e):
        ls = (DepositoDDL.value).find('-')
        iddep = int(DepositoDDL.value[:ls])
        btnAceptcmb.on_click=lambda _:cmbdep_Si(dlg, iddep)
        if e.data == 'false':
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text('AVISO'),
                content=ft.Row(
                    width=400,
                    wrap=True,
                    controls=[
                        ft.Text('Justifique el cambio de deposito'),
                        notaCambio,
                        ]
                    ),
                actions=[
                    btnAceptcmb,
                    ft.TextButton("Cancelar", on_click= lambda _:cmbdep_No(dlg)),
                ]
            )
            page.open(dlg)


    def busca_infoub():
        try:
            if UbicacionIncidente.value != '':
                url = UbicacionIncidente.value
                coord = get_coor(url)
                geolocator = Nominatim(user_agent="App_mapa_prueba")
                location = geolocator.reverse(str(coord[0])+','+str(coord[1]))
                try:
                    municipio = (location.raw['address'])['county']
                    if municipio == 'Municipio de Puebla':
                        municipio = 'Puebla'
                except KeyError:
                    municipio = (location.raw['address'])['town']

                try:
                    calle = (location.raw['address'])['road']
                except KeyError:
                    calle = ''

                querymun = "SELECT Id, Municipio FROM CatMunicipio WHERE Municipio LIKE '%"+municipio+"%'"
                mun = run_query(querymun)
                if len(mun)!=0:
                    MunicipioDDL.value = str(mun[0][0])+'- '+mun[0][1]
                    municipioIncidenteSeleccionado()
                    Vialidad.value = calle
                    page.update()
                else:
                    alerta('AVISO', 'Sin informacion del sitio')
        except:
            alerta('AVISO', 'Revisa tu conexion a internet o intenta con otro enlace')


    def mosaicos():
        # vehiculosIncidenteslv.controls.clear()  # limpiamos el listView para volverlo a llenar
        veh_temp = []
        for vi in vehiculosInvolucrados:
            tituloMostrar = str(vi.marca + ' ' + vi.linea + ' ' + str(vi.modelo) + ' ' + vi.noPlacas)
            if vi.tipoVehiculo == "BICICLETA":
                tituloMostrar = vi.tipoVehiculo + ' ' + vi.color + ' '
                print(tituloMostrar)
            elemento = ft.ListTile(
                leading= ft.Text(value=str(vi.noVehiculo).zfill(3), color= ft.Colors.BLACK),
                title= ft.Text(value=tituloMostrar),
                trailing= ft.PopupMenuButton(
                    icon=ft.Icons.MORE_VERT,
                    items=[
                        ft.PopupMenuItem(text="EDITAR", on_click= editar_vehiculo),
                        ft.PopupMenuItem(text="ELIMINAR", on_click= eliminar_vehiculo)
                    ],
                )
            )
            veh_temp.append(elemento)
            # for vt in veh_temp:
            #     print(vt.title)
        vehiculosIncidenteslv.controls.extend(veh_temp)
        if len(veh_temp) > 0:            
            btnAgregarRegistro.visible = True        
        page.update()


    def agregarVehiculoLista():
        btnVehiculoInvolucradoAdd.disabled = True
        page.update()
        tipoVehiculoVal = TipoVehiculoDDL.value
        tipoGruaVal = TipoGruaDDL.value
        noPlacasVal = NoPlaca.value.strip()
        lineaVal = Linea.value.strip()
        # modeloVal = ModeloVehiculo.value.strip()
        colorVal = ColorVehIncidente.value.strip()
        observacionesVehiculoVal = True
        marcaSelected = marcaVehiculoGet()
        marcaId = marcaIdSeleccionado()

        if tipoVehiculoVal == "BICICLETA":
                observacionesVehiculoVal = False
                marcaSelected = ""
                marcaId = 0
                parametro = len(ObservacionesdelVehiculo.value.strip())
                if parametro > 10:
                    observacionesVehiculoVal = True

        if (tipoVehiculoVal != None  and tipoGruaVal != None and len(noPlacasVal) > 0 and
           len(lineaVal) > 0 and len(colorVal) > 0 and observacionesVehiculoVal):
            
            origenPlacasId = origenPlacasSeleccionado()
            origenPlacasNombre = origenPlacasNombreSeleccionado()
                
            vehiculosInvolucrados.append(
            VehiculoIncidente(1, NoVehiculo.value, TipoVehiculoDDL.value, TipoGruaDDL.value,  SinPlacas.value, origenPlacasId, origenPlacasNombre,
                            NoPlaca.value, NoSerie.value, marcaId, marcaSelected, Linea.value, ModeloVehiculo.value, ColorVehIncidente.value,
                            NombreConductor.value, ApellidosConductor.value, ObservacionesdelVehiculo.value)
                    )
            vehiculosIncidenteslv.controls.clear()  # limpiamos el listView para volverlo a llenar
            limpiarControlesVehiculosInci()  # limpiamos los controles de registro
            mosaicos()
            btnVehiculoInvolucradoAdd.disabled = False
            page.update()
        else:
            alerta('AVISO', 'FALTAN CAMPOS POR LLENAR')
            btnVehiculoInvolucradoAdd.disabled = False
            page.update()
        

    def vehiculoDatosUpdate():
        for vt in vehiculosInvolucrados:
            if int(vt.noVehiculo) == int(NoVehiculo.value):
                origenPlacasId = origenPlacasSeleccionado()
                origenPlacasNombre = origenPlacasNombreSeleccionado()
                marcaId = marcaIdSeleccionado()
                marcaSelected = marcaVehiculoGet()

                vt.actualizarDatos(TipoVehiculoDDL.value, TipoGruaDDL.value, SinPlacas.value,
                                   origenPlacasId, origenPlacasNombre, NoPlaca.value, NoSerie.value,
                                   marcaId, marcaSelected, Linea.value, ModeloVehiculo.value,
                                   ColorVehIncidente.value, NombreConductor.value, ApellidosConductor.value, ObservacionesdelVehiculo.value)
                
        limpiarControlesVehiculosInci()
        btnVehiculoInvolucradoAdd.visible = True
        btnVehiculoInvolucradoUpd.visible = False
        vehiculosIncidenteslv.controls.clear()
        mosaicos()
        noVehiculoGet()

        page.update()


    def estatusIncidenteUpdate():
        try:
            consultaLite = 'SELECT Descripcion FROM CatEstatusIncidente WHERE Activo = 1'
            rows = run_queryLite(consultaLite)
            for row in rows:
                EstatusAdministracionDDL.options.append(
                    ft.DropdownOption(
                        key= (str(row[0])),
                        content= ft.Text(str(row[0]))
                    )
                )
            EstatusAdministracionDDL.value = "EN ARRIBO"
        except Exception as er:
            print("Error: ", er)


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
        # MunicipioIdAttr = municipioSeleccionado()
        RegionIdAttr = regionSeleccionada()
        LatitudAttr = Latitud.value
        LongitudAttr = Longitud.value
        UbicacionAttr = Ubicacion.value
        CreadoPorAdminIdAttr = 1
        ActualizadoPorAdminIdAttr = 1
        btnAgregarRegistro.disabled = True
        btnAgregarRegistro.text = "GUARDANDO..."
        page.update()
        consultaSql = '''INSERT INTO CatDepositoVehicular
                        (RazonSocial, RepresentanteLegal, CorreoElectronicoContacto, NombreCompletoContactos
                        ,Telefonos, DireccionDeposito, RegionId, Latitud, Longitud, Ubicacion
                        ,CreadoPorAdminId, FechaCreacion, ActualizadoPorAdminId, FechaActualizacion, Activo)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,GETDATE(),?,GETDATE(),1)'''
        try:
            run_query(consultaSql, (RazonSocialAttr, RepresentanteLegalAttr, CorreoElectronicoContactoAttr, NombreCompletoContactosAttr
                                   ,TelefonosAttr, DireccionDepositoAttr, int(RegionIdAttr), LatitudAttr, LongitudAttr, UbicacionAttr
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
        # MunicipioIdAttr = municipioSeleccionado()
        RegionIdAttr = regionSeleccionada()
        LatitudAttr = Latitud.value
        LongitudAttr = Longitud.value
        UbicacionAttr = Ubicacion.value
        ActivoAttr = Activo.value
        IdAttr = Id.value
        btnEditarRegistro.disabled = True
        btnEditarRegistro.text = "ACTUALIZANDO..."
        page.update()
        consultaSql = '''UPDATE CatDepositoVehicular
                             SET RazonSocial = ?
                                ,RepresentanteLegal = ?
                                ,CorreoElectronicoContacto = ?
                                ,NombreCompletoContactos = ?
                                ,Telefonos = ?
                                ,DireccionDeposito = ?
                                ,RegionId = ?
                                ,Latitud = ?
                                ,Longitud = ?
                                ,Ubicacion = ?
                                ,ActualizadoPorAdminId = 1
                                ,FechaActualizacion = GETDATE()
                                ,Activo = ?
                            WHERE Id = ?'''
        try:
            run_query(consultaSql, (RazonSocialAttr, RepresentanteLegalAttr, CorreoElectronicoContactoAttr, NombreCompletoContactosAttr
                                   ,TelefonosAttr, DireccionDepositoAttr, RegionIdAttr, LatitudAttr, LongitudAttr, UbicacionAttr, ActivoAttr, IdAttr))
            alerta('EXITOSO', 'REGISTRO ACTUALIZADO EXITOSAMENTE: ' + RazonSocialAttr)
            depositosLista()
        except:
            alerta('ALERTA', 'oOCURRIO UN ERROR AL INTENTAR ACTUALIZAR EL REGISTRO')
        limpiarControles()
        botonesAgregar()
        page.update()


    def get_coor(url):#extraccion coordenadas de enlace google maps
        
        coordenadas = [0,0]
        pagina = requests.get(url) # extrae datos de url enviado

        if pagina.status_code == 200: # en caso de conexion exitosa 
            soup = BeautifulSoup(pagina.content, 'html.parser') # convierte la informacion en html
            infopag = soup.find_all('meta') # extrae la informacion de etiquetas meta
            marker = (infopag[3].get('content')).split('&') # en la 4ta etiqueta se encuentran las coordenadas almacenadas en la propiedad markers
            
            for dato in marker: # se extrae en especifico la informacion de markers
                if dato[:4] == 'mark':
                    coordenadas.clear()
                    li = dato.index('%')
                    lati = float(dato[8:li])
                    coordenadas.append(lati)
                    ls = dato.index('C')+1
                    long = float(dato[ls:])
                    coordenadas.append(long)
        
        return coordenadas


    def abrir_mapa():
        url = Ubicacion.value
        if url!='':
            coord = get_coor(url)
            #mapa
            if coord[0] == 0 and coord[1]==0:
                alerta('AVISO', 'Error al intentar abrir ubicacion, actualice el enlace')
            else:
                ubmap = mapa(coord[0], coord[1])
                visor_map.content = ubmap.result
                page.open(bs)
            
            page.update()
        else:
            alerta('AVISO', 'No hay ubicacion disponible')


    def incidentesAdd():
        if len(vehiculosInvolucrados) > 0:
            anio = anioGetSeleccionado()        
            ConsultaQuery = 'SELECT ISNULL(MAX([FolioIncidente]), 0) FROM [Incidentes] WHERE YEAR(FechaIncidente) = ?'
            fechaCompleta = FechaIncidente.value + ' '+ HoraIncidente.value
            print(fechaCompleta)
            folioIncidenteSigQuery = run_query(ConsultaQuery, (int(anio),))
            folioSig = int(folioIncidenteSigQuery[0][0]) + 1
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #        
            tipoIncideneVal = TipoIncidenteDDL.value
            folioIncidenteVal = str(folioSig)
            vialidadVal = Vialidad.value
            coloniaVal = Colonia.value
            referenciaUbicacionVal = Referencia.value       
            ubicacionIncidenteVal = UbicacionIncidente.value
            municipioIdVal = municipioIncidenteSeleccionado()
            regionIdVal = regionIncidenteSeleccionado()
            depositoVal = depositoIncidenteSeleccionado()
            respondienteNombreVal = RespondienteNombreCompleto.value
            respondienteIdentificacionVal = RespondienteIdentificacion.value
            respondienteNotasVal = NotaRespondiente.value
            folio911Val = str(Folio911.value)
            estatusIncidenteVal = EstatusIncidenteDDL.value
            consultaSql = '''INSERT INTO [dbo].[Incidentes]
                            ([TipoIncidente],[FechaIncidente], [FolioIncidente]
                            ,[VialidadIncidente],[ColoniaIncidente],[ReferenciaUbicacionIncidente],[UbicacionIncidente]
                            ,[MunicipioId],[RegionId],[DepositoVehicularId]
                            ,[RespondienteNombreCompleto],[RespondienteIdentificacion],[RespondienteNotas]
                            ,[Folio911],[EstatusIncidente],[CreadoPor],[FechaCreacion],[Activo])
                    VALUES(?, CONVERT(datetime, ?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1 , GETDATE(), 1)'''
            try:
                run_query(consultaSql, 
                        (tipoIncideneVal, fechaCompleta, folioIncidenteVal, 
                        vialidadVal, coloniaVal, referenciaUbicacionVal, ubicacionIncidenteVal,
                        municipioIdVal, regionIdVal, depositoVal,
                        respondienteNombreVal, respondienteIdentificacionVal, respondienteNotasVal,
                        folio911Val, estatusIncidenteVal,))            
                consultaSqlIdInciedente = 'SELECT MAX(Id) AS Id FROM Incidentes'
                res = run_query(consultaSqlIdInciedente)
                IdIncidente = res[0][0]
                guardados = 0
                if (int(IdIncidente) > 0):
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    registrarEstatus = '''INSERT INTO [EstatusIncidentes]
                                            ([IncidenteId],[DepositoVehicularId],[EstatusId]
                                            ,[FechaMovimiento],[CreadoPor],[Activo])
                                        VALUES(?, ?, 1, GETDATE(), 1, 1)'''
                    run_query(registrarEstatus, (int(IdIncidente), int(depositoVal),))
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    alerta('AVISO', 'INCIDENTE GUARDADO CORRECTAMENTE')
                    for vi in vehiculosInvolucrados:
                        insertVehiculosInvolucradosQuery = '''
                        INSERT INTO [dbo].[IncidenteVehiculos]
                                ([IncidenteId],[NumeroVehiculo],[TipoVehiculo],[TipoGrua]
                                ,[SinPlacas],[LugarOrigenPlacas],[NumeroPlaca]
                                ,[NumeroSerie],[MarcaId],[LineaVehiculo]
                                ,[ModeloVehiculo],[Color],[NombresConductor]
                                ,[ApellidosConductor],[ObservacionesVehiculo]
                                ,[CreadoPor],[FechaCreacion],[Activo])
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, 1, GETDATE(), 1)'''
                        run_query(insertVehiculosInvolucradosQuery,
                                (IdIncidente, vi.noVehiculo, vi.tipoVehiculo, vi.tipoGrua,
                                vi.sinPlacas, vi.origenPlacasId, vi.noPlacas,
                                vi.noSerie, vi.marcaId, vi.linea,
                                vi.modelo, vi.color, vi.nombreConductor,
                                vi.apellidosConductor, vi.observaciones))
                        guardados += 1
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    vehiculosCount = int(len(vehiculosInvolucrados))
                    if guardados == vehiculosCount:
                        alerta('AVISO', 'SE REGISTRARON ' + str(guardados) + ' VEHICULO(S) CORRECTAMENTE')
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    if (len(inasists) > 0):
                        for ina in inasists:
                            consultaSql = '''INSERT INTO 
                                        [Inasistencias] ([IdDeposito],[IdIncidente],[Anotacion]) 
                            VALUES (?, ?, ?)'''
                            run_query(consultaSql, (int(ina.dep), int(IdIncidente), ina.nota))
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    vehiculosIncidenteslv.controls.clear()
                    vehiculosInvolucrados.clear()
                    limpiarControlesIncidentes()
                    limpiarControlesVehiculosInci()
                    incidenteMostrarControles()
                    botonesAgregar()
                    # RECORRER PARA GUARDAR LOS ELEMENTOS DE LA LISTA DE VEHICULOS INVOLUCRADOS
                else:
                    alerta('ALERTA', 'OCURRIO UN ERROR AL GUARDAR EL INCIDENTE, INFORME AL RESPONSABLE DEL SISTEMA')            
            except Exception as ex:
                alerta('ADVERTENCIA', 'OCURRIO UN ERROR')
                print(f"{ex}")
        else:
            alerta('AVISO', 'REGISTRE AL MENOS UN VEHICULO')


    def incidentesUpdate():
        alerta('PRUEBA', 'CLICK EN BOTON ACTUALIZAR INCIDENTE')


    # CONTROLES PARA EL FORMULARIO DE REGIONES
    regionId = ft.TextField(label='Id', width=70, read_only=True, height= 35, text_size=12)
    regionNombre = ft.TextField(label='REGIÓN', width=280, height= 35, text_size=12)
    regionActivo = ft.Checkbox(label='DISPONIBLE', visible= False) 
    
    # CONTROLES PARA EL FORMULARIO DE MUNICIPIOS
    municipioIdProp = ft.TextField(label='Id', width= 70, height= 35, text_size=12, read_only= True)
    municipioNombreProp = ft.TextField(label='MUNICIPIO', width= 720, height= 35, text_size=12)
    municipioSelectRegion = Dropdown(label= 'REGIÓN', width=350, enable_filter= True, editable= True, on_change=lambda _:regionSeleccionada())
    
    # CONTROLES PARA EL FORMULARIO DE DEPOSITOS
    Id = ft.TextField(label='Id', width= 70, height= 35, text_size=12, read_only= True)
    RazonSocial = ft.TextField(label='RAZÓN SOCIAL', width= 700, height= 35, text_size=12)
    RepresentanteLegal = ft.TextField(label='REPRESENTANTE LEGAL', width= 405, height= 35, text_size=12)
    NombreCompletoContactos = ft.TextField(label='NOMBRE DE CONTACTO', width= 405, height= 35, text_size=12)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    CorreoElectronicoContacto = ft.TextField(label='CORREO ELECTRÓNICO', width= 300, height= 35, text_size=12)
    Telefonos = ft.TextField(label='TELÉFONO(S)', width= 500, height= 35, text_size=12)
    Ubicacion = ft.TextField(label='UBICACIÓN (MAPS)', width=500)    
    Latitud = ft.TextField(label='LATITUD', width=250)
    Longitud = ft.TextField(label='LONGITUD', width=250)     
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    DireccionDeposito = ft.TextField(label='DIRECCIÓN', width= 1400, height= 35, text_size=12)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    Activo = ft.Switch(label='ACTIVO', label_position=ft.LabelPosition.LEFT, visible= False)
    
    # CONTROLES PARA EL FORMULARIO DE INCIDENTES
    IdIncidente = ft.TextField(label='Id', width= 70, read_only= True)
    TipoIncidenteDDL = Dropdown(label= 'TIPO DE INCIDENTE', width=350, enable_filter= True, editable= True)
    FechaIncidente = ft.TextField(label='FECHA', value= dt.datetime.now().strftime("%Y-%m-%d"), width=150)
    HoraIncidente = ft.TextField(label='HORA', value= dt.datetime.now().strftime("%H:%M"), width=100)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    Vialidad = ft.TextField(label='VIALIDAD *', width=350) 
    Colonia = ft.TextField(label='COLONIA *', width=250)
    Referencia = ft.TextField(label='REFERENCIA', width=400)
    UbicacionIncidente = ft.TextField(label='UBICACIÓN (MAPS) *', width=420)
    btn_buscaub = ft.ElevatedButton(content=ft.Text(value='Buscar Info', color=ft.Colors.WHITE, size=13), on_click= lambda _:busca_infoub(), bgcolor='#E2BE96')
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    MunicipioDDL = Dropdown(label= 'MUNICIPIO *', width=400, enable_filter= True, editable= True, on_change=lambda _:municipioIncidenteSeleccionado())
    RegionTxt = ft.TextField(label='REGIÓN', width=450, read_only=True)
    DepositoDDL = Dropdown(label= 'DEPÓSITO', width=650, enable_filter= True, editable= True)
    CambioDDL = ft.Checkbox(label='Atendido', visible= False, on_change=cambioDep, value=True)
    notaCambio = ft.TextField(label='Nota', width=400, on_change= lambda e:valid_lon(e,btnAceptcmb))
    btnAceptcmb = ft.TextButton("Aceptar", disabled=True)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    RespondienteNombreCompleto = ft.TextField(label='NOMBRE COMPLETO DE RESPONDIENTE *', width= 700)
    RespondienteIdentificacion = ft.TextField(label='IDENTIFICACIÓN DE RESPONDIENTE *', width= 300)
    NotaRespondiente = ft.TextField(label='NOTA DE RESPONDIENTE', width= 1010)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    Folio911 = ft.TextField(label='FOLIO DE 911', width=200)
    EstatusIncidenteDDL = Dropdown(label= 'ESTATUS INCIDENTE *', width=350, enable_filter= True, editable= True, visible= False) 

    # CONTROLES PARA EL FORMULARIO DE VEHICULOS DE INCIDENTES
    IdVehiculoIncidente = ft.TextField(label='Id', width= 70, read_only= True, visible= False)
    FolioIncidente = ft.TextField(label='No. FOLIO', width=200, read_only= True, visible= False)
    NoVehiculo = ft.TextField(label='No. DE VEHÍCULO', width=140, read_only= True, visible=False)
    TipoVehiculoDDL = Dropdown(label= 'TIPO DE VEHICULO', width=500, enable_filter= True, editable= True, visible= False, on_change=lambda _: tipoVehiculoSeleccionado())
    TipoGruaDDL = Dropdown(label= 'TIPO DE GRUA', width=200, enable_filter= True, editable= True, visible= False)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    SinPlacas = ft.Checkbox(label='NO TIENE PLACAS', visible= False, on_change=vehiculoSinPlacasCheck)
    LugarOrigenPlacasDDL = Dropdown(label= 'ORIGEN DE LAS PLACAS *', width=300, enable_filter= True, editable= True, visible= False)
    NoPlaca = ft.TextField(label='PLACA *', width=200, visible=False)
    NoSerie = ft.TextField(label='No. DE SERIE', width=400, visible= False)
    ColorVehIncidente = ft.TextField(label='COLOR *', width=200, visible= False)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    MarcaDDL = Dropdown(label= 'MARCA *', width=250, enable_filter= True, editable= True, visible=False)
    Linea = ft.TextField(label='LINEA *', width=400, visible= False)
    ModeloVehiculo = ft.TextField(label='MODELO', width=200, visible=False)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    NombreConductor = ft.TextField(label='NOMBRE(S) DEL CONDUCTOR', width=300, visible= False)
    ApellidosConductor = ft.TextField(label='APELIDOS DEL CONDUCTOR', width=300, visible= False)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    ObservacionesdelVehiculo = ft.TextField(label='OBSERVACIONES', width=900, visible= False)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #########################FILTROS REPORTES #############################################################
    FiltroIncidentesAnioDDL = Dropdown(label= 'AÑO', width=250, enable_filter= True, editable= True, on_change=lambda _:filtroIncideneAnioSeleccionado())
    FiltroIncidentesStatusDDL = Dropdown(label= 'ESTATUS', width=250, enable_filter= True, editable= True, on_change=lambda _:filtroStatusIncideneAnioSeleccionado(FiltroIncidentesStatusDDL,1))
    FiltroIncidentesDepDDL = Dropdown(label= 'DEPÓSITO', width=450, enable_filter= True, editable= True, on_change=lambda _:filtroStatusIncideneAnioSeleccionado(FiltroIncidentesDepDDL,2))
    FiltroIncidentesRegDDL = Dropdown(label= 'REGIÓN', width=250, enable_filter= True, editable= True, on_change=lambda _:filtroStatusIncideneAnioSeleccionado(FiltroIncidentesRegDDL,3))
    FiltroIncidentesTIDDL = Dropdown(label= 'TIPO DE INCIDENTE', width=250, enable_filter= True, editable= True, on_change=lambda _:filtroStatusIncideneAnioSeleccionado(FiltroIncidentesTIDDL,4))
    FiltroEstatusIncidentesAnioDDL = Dropdown(label= 'AÑO', width=250, enable_filter= True, editable= True, on_change=lambda _:filtroEstatusIncideneAnioSeleccionado())    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    DatosIncidentesTxt = ft.TextField(label='Datos del incidente', width=600, visible= True, read_only= False)
    EstatusAdministracionDDL = Dropdown(label= 'Estatus *', width=250, enable_filter= True, editable= True)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #textosControles
    textoGuardar = ft.Text(value='GUARDAR', size=13, color=ft.Colors.WHITE)
    textoBuscar = ft.Text(value='BUSCAR', size=13, color=ft.Colors.WHITE)
    textoEditar = ft.Text(value='EDITAR', size=13, color=ft.Colors.WHITE)
    textoCancelar = ft.Text(value='CANCELAR', size=13, color=ft.Colors.WHITE)
    textoAgregarVehiculoIncidente = ft.Text(value='VER VEHÍCULOS INVOLUCRADOS', size=13, color=ft.Colors.WHITE)
    textoDatosIncidente = ft.Text(value='DATOS DEL INCIDENTE', size=13, color=ft.Colors.WHITE)
    textoVehiculosAdd = ft.Text(value='AGREGAR A LA LISTA', size=13, color=ft.Colors.WHITE)
    textoVehiculosUpd = ft.Text(value='EDITAR INFORMACIÓN', size=13, color=ft.Colors.WHITE)
    textoActualizarEstatus = ft.Text(value='ACTUALIZAR ESTATUS', size=13, color=ft.Colors.WHITE)

    # Controles mapa
    visor_map = ft.InteractiveViewer(
                    width=900,
                    height=900,
                    min_scale=0.1,
                    boundary_margin=ft.Margin(10,10,10,10),
                    content=ft.Text('')
                )


    bs = ft.BottomSheet(
        ft.Container(
                    width=900,
                    height=900,
                    content=visor_map
                ),
        open=False,
    )


    btn_map = ft.ElevatedButton("Ver ubicación", on_click= lambda _:abrir_mapa())


    # BOTONES
    btnAgregarRegistro = ft.CupertinoButton(content=textoGuardar, width=180, height=55, opacity_on_click=0.3, border_radius=10, visible = True, bgcolor='#3D9B84') # , on_click=lambda _:regionesAdd()
    btnEditarRegistro = ft.CupertinoButton(content=textoEditar, width=180, height=55, opacity_on_click=0.3, border_radius=10, visible = False, bgcolor='#B2B2B1') # , on_click=lambda _:regionesUpdate()    
    btnCancelarAccionForm = ft.CupertinoButton(content=textoCancelar, width=180, height=55, opacity_on_click=0.3, border_radius=10, visible = False, bgcolor='#B33449') # , on_click=lambda _:regionesAdd()
    btnBuscarRegistro = ft.CupertinoButton(content=textoBuscar, width=180, height=55, opacity_on_click=0.3, border_radius=10, visible = True, bgcolor='#E2BE96', on_click=lambda _:depositosBuscaLista())
    btnBuscarRegistroMun = ft.CupertinoButton(content=textoBuscar, width=180, height=55, opacity_on_click=0.3, border_radius=10, visible = True, bgcolor='#E2BE96', on_click=lambda _:depositosBuscaListaReg())
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    btnAgregarVehiculoIncidente = ft.CupertinoButton(content=textoAgregarVehiculoIncidente, width=180, height=50, opacity_on_click=0.3, border_radius=10, visible = True, bgcolor='#3D9B84')
    btnDatosIncidente = ft.CupertinoButton(content=textoDatosIncidente, width=180, height=50, opacity_on_click=0.3, border_radius=10, visible = False, bgcolor='#E2BE96')
    btnVehiculoInvolucradoAdd = ft.CupertinoButton(content=textoVehiculosAdd, width=180, height=50, opacity_on_click=0.3, border_radius=10, visible= False, bgcolor='#3D9B84')
    btnVehiculoInvolucradoUpd = ft.CupertinoButton(content=textoVehiculosUpd, width=180, height=50, opacity_on_click=0.3, border_radius=10, visible= False, on_click= lambda _:vehiculoDatosUpdate(), bgcolor='#E2BE96')
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    btnActualizarEstatus = ft.CupertinoButton(content=textoActualizarEstatus, width=180, height=50, opacity_on_click=0.3, border_radius=10, visible= False, on_click= lambda _:estatusIncidenteUpdate(), bgcolor='#B2B2B1')
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


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
        # if selected_index == 4:
        #     show_SancionesDepositos()
        if selected_index == 4:
            show_Incidentes()
        if selected_index == 5:
            show_IncidenteRegistros()
        if selected_index == 6:
            show_AdministracionEstatusIncdente()
        page.update()


    def show_CatRegiones():
        page.controls.clear()
        encabezado = ft.Text('CATÁLOGO DE REGIONES', size= 30)
        btnAgregarRegistro.visible=True
        btnAgregarRegistro.on_click = lambda _:regionesAdd()
        btnEditarRegistro.on_click = lambda _:regionesUpdate()
        btnCancelarAccionForm.on_click = lambda _:botonesCancelarAccionForm()
        page.add(encabezado)
        page.add(
            ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        controls=[
                            ft.Container(
                                width=450,
                                height=480,
                                padding=20,
                                alignment=ft.Alignment(0.0, 0.0),
                                content=ft.Column(controls=[
                                        ft.Row(controls=[regionId]),
                                        ft.Row(controls=[regionNombre]),
                                        ft.Row(controls=[regionActivo]),
                                        ft.Row(controls = [btnAgregarRegistro, btnEditarRegistro, btnCancelarAccionForm])
                                ])
                            )
                        ], 
                    ),
                    ft.Column(
                        controls=[
                            ft.Row(controls=[
                                ft.Container(                                    
                                    width=650,
                                    height=500,
                                    alignment=ft.Alignment(0.0, 0.0),
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
        encabezado = ft.Text('CATÁLOGO DE MUNICIPIOS', size= 30)
        municipioSelectRegion.options = []
        btnAgregarRegistro.visible=True
        btnAgregarRegistro.on_click = lambda _:municipioAdd()
        btnEditarRegistro.on_click = lambda _:municipioUpdate()
        btnCancelarAccionForm.on_click = lambda _:botonesCancelarAccionForm()
        regionesDropDownList()
        municipiosLista()
        page.add(encabezado)
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
                controls=[btnAgregarRegistro, btnEditarRegistro, btnCancelarAccionForm, btnBuscarRegistroMun]
            ),
            ft.Row(
                vertical_alignment= ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        ft.Container(
                            width=800,
                            height=450,
                            alignment=ft.Alignment(0.0, 0.0),
                            content= lv
                        )
                    )
                ]
            )
        )


    def show_Depositos():
        page.controls.clear()
        encabezado = ft.Text('CATÁLOGO DE DEPÓSITOS', size= 30)
        municipioSelectRegion.options = []
        btnAgregarRegistro.on_click = lambda _:depositoAdd()
        btnEditarRegistro.on_click = lambda _:depositoUpdate()
        btnCancelarAccionForm.on_click = lambda _:botonesCancelarAccionForm()
        page.add(encabezado)
        page.add(
            ft.Row(
                # vertical_alignment= ft.CrossAxisAlignment.START,                
                width=1750,
                wrap=True,
                controls= [
                    ft.Column(
                        controls=[Id]
                    ),
                    ft.Column(
                        controls=[RazonSocial]
                    ),
                    ft.Column(
                        controls=[RepresentanteLegal]
                    ),
                    ft.Column(
                        controls= [NombreCompletoContactos]
                    )
                ]
            ),
            ft.Row(
                # vertical_alignment= ft.CrossAxisAlignment.START,                
                width=1750,
                wrap=True,
                controls=[                    
                    ft.Column(
                        controls=[CorreoElectronicoContacto]
                    ),
                    ft.Column(
                        controls=[Telefonos]
                    ),
                    ft.Column(                        
                        controls=[Ubicacion]
                    ),
                    ft.Column(
                        controls= [Latitud]
                    ),
                    ft.Column(
                        controls= [Longitud]
                    ),
                    ft.Column(
                        controls= [btn_map]
                    )
                ]
            ),
            ft.Row(
                # vertical_alignment= ft.CrossAxisAlignment.START,                
                width=1750,
                wrap=True,
                controls=[
                    ft.Column(
                        controls=[DireccionDeposito]
                    )
                ]
            ),
            ft.Row(
                # vertical_alignment= ft.CrossAxisAlignment.START,                
                width=1750,
                wrap=True,
                controls=[                    
                    ft.Column(
                        controls=[municipioSelectRegion]
                    )                    
                ]                                
            ),
            ft.Row(
                width=1750,
                wrap=True,
                controls=[
                    ft.Column(
                        controls=[Activo]
                    )
                ]
            ),
            ft.Row(
                # vertical_alignment= ft.CrossAxisAlignment.START,
                controls= [btnAgregarRegistro, btnEditarRegistro, btnCancelarAccionForm, btnBuscarRegistro]
            ),
            ft.Row(
                # vertical_alignment= ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=1750,
                        height=300,
                        alignment=ft.Alignment(0.0, 0.0),
                        content = lv
                    )
                ]                
            )
        )
        depositosLista()
        # municipiosDropDownList()
        regionesDropDownList()
        botonesAgregar()


    def show_RolesDepositos():
        page.controls.clear()
        encabezado = ft.Text('ROLES DE DEPÓSITOS', size= 30)
        drop_region.options = []
        drop_region.options = reg_options()
        page.add(encabezado)
        page.add(
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Container(
                                width=(tam*7)+(sep*6),
                                height=600,
                                alignment= ft.Alignment(0.0, 0.0),
                                content= ft.Column(
                                    controls=[
                                        mes_lista,
                                        dias_sem,
                                        hoja
                                    ]
                                )                                                                    
                            )
                        ], expand=True, horizontal_alignment= ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Column(
                        controls=[
                            ft.Container(
                                width= 500,
                                height= 600,
                                alignment= ft.Alignment(-1.0, 0.0),
                                content= ft.Column(
                                    controls=[
                                        ft.Row(controls=[drop_region], alignment=ft.Alignment(-1.0, 0.0)),
                                        ft.Row(controls=[drop_depositos], alignment=ft.Alignment(-1.0, 0.0)),
                                        ft.Row(controls=[listadep], alignment=ft.Alignment(-1.0, 0.0), height=350, width=500),
                                        ft.Row(controls=[btn_guardar], alignment=ft.MainAxisAlignment.CENTER, width=300),
                                    ]
                                )                                
                            )
                        ], horizontal_alignment= ft.Alignment(0.0, 0.0)
                    )
                ]
            )
        )        
        arranque()        
        

    def show_SancionesDepositos():
        page.controls.clear()
        encabezado = ft.Text('SANCIONES A DEPOSITOS', size= 30)
        page.add(encabezado)


    def show_Incidentes():
        page.controls.clear()
        encabezado = ft.Text('REGISTRO DE INCIDENTES', size= 30)
        btnAgregarRegistro.on_click = lambda _:incidentesAdd()  
        btnAgregarRegistro.visible = False      
        btnEditarRegistro.on_click = lambda _:incidentesUpdate()
        btnCancelarAccionForm.on_click = lambda _:botonesCancelarAccionForm()
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        btnAgregarVehiculoIncidente.on_click = lambda _:validarDatosIncidente()
        btnDatosIncidente.on_click = lambda _:incidenteMostrarControles()
        btnVehiculoInvolucradoAdd.on_click = lambda _:agregarVehiculoLista()
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #        
        TipoIncidenteDDL.options = []
        tipoIncidenteDDL()
        EstatusIncidenteDDL.options =[]
        estatusIncidenteDDL()
        MunicipioDDL.options = []
        municipiosIncidentesDropDownList()
        DepositoDDL.options = []
        TipoVehiculoDDL.options = []
        tipoVehiculoDDL()
        # TipoGruaDDL.options = []
        tipoGruaDDLv2()
        MarcaDDL.options = []
        marcasVehiculosDropDownList()
        LugarOrigenPlacasDDL.options = []
        lugarOrigenPlacasDropDownList()       

        page.add(encabezado)
        page.add(
            ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Row(controls=[IdIncidente, TipoIncidenteDDL, FechaIncidente, HoraIncidente]),
                                    ft.Row(controls=[Vialidad, Colonia, UbicacionIncidente, btn_buscaub, Referencia],wrap=True, width=1280),
                                    ft.Row(controls=[MunicipioDDL, RegionTxt, DepositoDDL, CambioDDL], wrap=True, width=1280),                                    
                                    ft.Row(controls=[RespondienteNombreCompleto, RespondienteIdentificacion]),
                                    ft.Row(controls=[NotaRespondiente]),
                                    ft.Row(controls=[Folio911, EstatusIncidenteDDL]),
                                    ft.Row(controls=[btnAgregarVehiculoIncidente, btnDatosIncidente])                                                                        
                                ]
                            )
                        ]
                    )                    
                ]
            ),
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Row(controls=[IdVehiculoIncidente, FolioIncidente, NoVehiculo, TipoVehiculoDDL, TipoGruaDDL]),
                            ft.Row(controls=[SinPlacas,LugarOrigenPlacasDDL,NoPlaca, NoSerie]),
                            ft.Row(controls=[MarcaDDL, Linea, ModeloVehiculo, ColorVehIncidente]),
                            ft.Row(controls=[NombreConductor, ApellidosConductor]),
                            ft.Row(controls=[ObservacionesdelVehiculo])
                        ]
                    ),
                    ft.Column(
                        controls=[
                            ft.Container(
                                content= ft.Column(
                                    controls=[ft.Row(controls=[vehiculosIncidenteslv])]
                                )
                            )
                        ]
                    )
                ]  
            ),
            ft.Row(
                controls=[btnVehiculoInvolucradoAdd, btnVehiculoInvolucradoUpd]
            ),
            ft.Row(
                controls=[
                    ft.Row(
                        controls=[btnAgregarRegistro, btnEditarRegistro, btnCancelarAccionForm]
                    )
                ]
            )            
        )        
        page.update()


    def show_IncidenteRegistros():
        page.controls.clear()
        encabezado = ft.Text('INCIDENTES REGISTRADOS', size= 30)
        page.add(encabezado)

        # FiltroIncidentesAnioDDL.options = []
        # FiltroIncidentesAnioDDL.key = []
        # filtroIncidenteAniosDropDownList()

        # fecha_actual = dt.date.today() # datetime.date.today()
        # anio_actual = fecha_actual.year
        # FiltroIncidentesAnioDDL.value = anio_actual

        FiltroIncidentesStatusDDL.options = []
        FiltroIncidentesStatusDDL.key = []

        FiltroIncidentesTIDDL.options = []
        FiltroIncidentesTIDDL.key = []

        filtroIncidenteStatusDropDownList()
        filtroIncidenteDepDropDownList()
        filtroIncidenteRegDropDownList()
        filtroIncidenteTIDropDownList()

        page.add(
            ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Row(controls=[FiltroIncidentesStatusDDL, FiltroIncidentesDepDDL, FiltroIncidentesRegDDL, FiltroIncidentesTIDDL])                                                                                                       
                                ]
                            )
                        ]
                    )                    
                ]
            ),
            ft.Row(
                vertical_alignment= ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        ft.Container(
                            width=1900,
                            height=650,
                            alignment=ft.Alignment(0.0, 0.0),
                            content= incidentesreplv
                        )
                    )
                ]
            )
        )
        page.update()


    def show_AdministracionEstatusIncdente():
        page.controls.clear()
        encabezado = ft.Text('ACTUALIZAR ESTATUS DE INCIDENTE', size= 30)

        FiltroEstatusIncidentesAnioDDL.options = []
        FiltroEstatusIncidentesAnioDDL.key = []
        filtroEstatusIncidenteAniosDropDownList()
        
        fecha_actual = dt.date.today() # datetime.date.today()
        anio_actual = fecha_actual.year
        FiltroEstatusIncidentesAnioDDL.value = anio_actual
                
        estatusIncidenteLista(anio_actual)

        page.add(encabezado)
        page.add(
            ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Row(controls=[DatosIncidentesTxt, EstatusAdministracionDDL, btnActualizarEstatus ])                                                                                                           
                                ]
                            )
                        ]
                    )                    
                ]
            ),
            ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Row(controls=[FiltroEstatusIncidentesAnioDDL])                                                                                                       
                                ]
                            )
                        ]
                    )                    
                ]
            ),
            ft.Row(
                vertical_alignment= ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        ft.Container(
                            width=800,
                            height=650,
                            alignment=ft.Alignment(0.0, 0.0),
                            content= EstatusIncidenteslv
                        )
                    )
                ]
            )
        )
        page.update()
    


    barradeNavegacion = ft.NavigationBar(
        selected_index= 0,
        on_change= on_navigation_change,
        destinations= [
            ft.NavigationBarDestination(icon= ft.Icon(name=ft.Icons.APP_REGISTRATION, color=ft.Colors.WHITE), label='Catálogo de Regiones'),
            ft.NavigationBarDestination(icon= ft.Icon(name=ft.Icons.ACCOUNT_TREE, color=ft.Colors.WHITE), label= 'Catálogo de Municipios', bgcolor = ft.Colors.BLACK),
            ft.NavigationBarDestination(icon= ft.Icon(name=ft.Icons.ADD_BUSINESS, color=ft.Colors.WHITE), label= 'Catálogo de Depósitos', bgcolor = ft.Colors.GREEN_400),
            ft.NavigationBarDestination(icon= ft.Icon(name=ft.Icons.ACCESS_TIME_FILLED_ROUNDED, color=ft.Colors.WHITE), label= 'Roles de Depósitos'),
            # ft.NavigationBarDestination(icon= ft.Icon(name=ft.Icons.INFO_SHARP, color=ft.Colors.WHITE), label= 'Sanciones Depositos', visible= False),  # ACCOUNT_BOX, label= 'Sanciones Depositos')  # ADD_CARD_OUTLINED   # ADD_COMMENT
            ft.NavigationBarDestination(icon= ft.Icon(name=ft.Icons.COMMUTE, color=ft.Colors.WHITE), label= 'Formulario de Incidentes'),
            ft.NavigationBarDestination(icon= ft.Icon(name=ft.Icons.TABLE_CHART_OUTLINED, color=ft.Colors.WHITE), label= 'Tabla de Incidentes'),
            #ft.NavigationBarDestination(icon= ft.Icon(name=ft.Icons.ADD_MODERATOR_OUTLINED, color=ft.Colors.WHITE), label= 'Estatus de Incidente')
        ],
        bgcolor= '#5F1B2D', 
        indicator_color= '#c4436f',
        animation_duration=1
    )

    page.navigation_bar = barradeNavegacion
    show_CatRegiones()
    page.open(banner)

ft.app(target= main, )  # # # view= ft.WEB_BROWSER