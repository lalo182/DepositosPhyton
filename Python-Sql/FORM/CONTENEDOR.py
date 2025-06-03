import flet as ft
import pyodbc
import calendar

from flet import *
from datetime import datetime

class Deposito(): # Diseñado para almacenar informacion para los depositos
        def __init__(self, color, id, fec_ini, fec_fin, nombre):
            self.color = color
            self.iddep = id
            self.fei = fec_ini
            self.fef = fec_fin  
            self.nom = nombre


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

    # servidor = 'ECI-SDMYT-001'
    #servidor = 'DESKTOP-TO7CUU2'
    servidor = 'DESKTOP-SMKHTJB'  # SERVIDOR DE LALO
    basedatos = 'DepositoVehicular_DB'
    
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

    
    tam =70 #tamaño contenedores dias calendario
    sep = 10 #separacion entre cuadros
    semana = ['Dom','Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab']
    meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

    colors=[
        ft.Colors.GREEN_600, 
        ft.Colors.ORANGE_700, 
        ft.Colors.BLUE_800, 
        ft.Colors.BROWN_200, 
        ft.Colors.CYAN_800, 
        ft.Colors.DEEP_PURPLE_700, 
        ft.Colors.PINK_ACCENT_400, 
        ft.Colors.RED_ACCENT_700, 
        ft.Colors.TEAL_700, 
        ft.Colors.WHITE60
    ]

    global mes
    global anio
    mes = int(datetime.now().month) # mes actual
    anio = int (datetime.now().year) # año actual
   
    din, dfi = calendar.monthrange(anio, mes) # obtiene el dia en que inicia el mes y el total de dias que conforman el mes
    rango=[] # almacena el rango seleccionado
    itemsd=[] # almacen de contenedores para dias de mes
    regdep = [] # almacena caracteristicas y roles de los depositos
    # condep=['1 - Deposito 1', '21 - Deposito 2', '136 - Deposito 3', '4 - Deposito 4'] # resultado consulta depositos    


    global status_save
    global region_sel
    seleccion = [] # dias asignados a deposito
    region_sel = ''
    status_save = False
    # global opdep
    # opdep = 0

    def arranque(): # establece valor para dropdowns de mes y año        
        global mes
        global anio
        drop_mes.value = meses[mes-1]
        drop_anio.value = str(anio)
        reg_options()
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

        global mes
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
                ft.TextButton("Si", on_click= lambda _: funcionsi(dlg)),
                ft.TextButton("No", on_click=lambda _: funcion_no(dlg)),
            ]
        )
        page.open(dlg)


    def reg_change(e): # acciones post seleccion de region
        global status_save
        global region_sel
        if len(regdep) > 0 and status_save == False:
            question_alert(
                'Info',
                'Con esta accción se perderán los cambios ¿Desea continuar?',
                limpiar_control,cancelar_sel
            )
        if len(regdep) == 0 or status_save == True:
            region_sel = drop_region.value
            limpiar_control(None)
            ls = (drop_region.value).index('-') 
            idr = int(drop_region.value[:ls]) # extrae id de region
            drop_depositos.options = dep_options(idr)
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
                #on_click=select_listdep,
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
        # condep = depositosRolesDropDownList()
        consultaSql = 'SELECT Id, RazonSocial FROM CatDepositoVehicular WHERE Activo = 1 AND RegionId = ?'
        depositosDb = run_query(consultaSql, (regionId,))
        for dep in depositosDb:
            deps.append(
                ft.DropdownOption(
                    # key=dep,
                    # content=ft.Text(value=dep)
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
                    # key=reg,
                    # content=ft.Text(value=reg)
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
        page.update()


    def rehabilita_dias(color, clickeable):
        for dia in itemsd:
            if dia.bgcolor == color:
                dia.bgcolor = ft.Colors.BLUE_GREY_500
                dia.on_click = clickeable
        page.update


    def consulta_rol(region):
        global mes
        global anio
        
        info_roles = '''SELECT Dep, Nombre, Listadia 
                        FROM
                        (SELECT Id as Dep, RazonSocial as Nombre, RegionId as Regid, T1.Listadia
                        FROM Dbo.CatDepositoVehicular 
                        INNER JOIN (SELECT Dias AS Listadia, DepositoVehicularId as Iddep FROM Dbo.DepositosRoles WHERE Anio = ? AND Mes = ?) AS T1
                        ON Id=iddep WHERE Activo=1) as t2
                        INNER JOIN
                        Dbo.CatRegion
                        ON Id=RegID WHERE id = ?'''
        listdep = run_query(info_roles, (anio, mes, region,))

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
        cad_dia = ''
        for dep in regdep:
            for dia in itemsd:
                if dia.bgcolor == dep.color:
                    valor = (dia.content.value)
                    if cad_dia == '':
                        cad_dia = valor
                    else:
                        cad_dia = cad_dia+','+valor
            query_rol = 'SELECT [DepositoVehicularId] FROM [dbo].[DepositosRoles] WHERE [DepositoVehicularId]=? AND [Mes]=? AND [Anio]=?'
            rolqry = run_query(query_rol, (dep.iddep, mes, anio,))

            if rolqry:
                act_rol ='UPDATE [dbo].[DepositosRoles] set [Dias]=? WHERE [DepositoVehicularId]=? AND [Mes]=? AND [Anio]=?'
                run_query(act_rol,(cad_dia, dep.iddep, mes, anio,))
            else:
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
            drop_depositos.options.append( 
                ft.DropdownOption(
                    key=str(dep.iddep)+'-'+dep.nom,
                    content=ft.Text(value=str(dep.iddep)+'-'+dep.nom)
                )
            )
            colors.append(dep.color)
        regdep.clear()
        status_save = False

        if dlg!=None:
            page.close(dlg)

        if region_sel != '':
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
        label='Deposito:',
        options=[],
        text_align=ft.TextAlign.CENTER,
        width=350,
        on_change=dep_change,        
    )


    drop_region = ft.Dropdown( # lista desplegable regiones
        editable=True,
        label='Region:',
        options=reg_options(),
        text_align=ft.TextAlign.CENTER,
        width=350,
        on_change=reg_change,
    )


    mes_lista = ft.Row ( # fila con listas de mes y año
        width=(tam*7)+(sep*6),
        height=100,
        controls=[drop_mes, drop_anio], alignment=ft.MainAxisAlignment.CENTER
    )


    btn_guardar = ft.CupertinoFilledButton(
        'Guardar',
        width=180,
        height=50,
        opacity_on_click=0.3, 
        border_radius=10, 
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
        municipioSelectRegion.value = ''
        # CONTROLES DEL FORMULARIO DE DEPOSITOS
        Id.value = ''
        RazonSocial.value = ''
        RepresentanteLegal.value = ''
        municipioSelectRegion.value = ''
        DireccionDeposito.value = ''
        NombreCompletoContactos.value = ''
        CorreoElectronicoContacto.value = ''
        Telefonos.value = ''
        Latitud.value = ''
        Longitud.value = ''
        Ubicacion.value = ''
        Activo.value = True
        

    def botonesAgregar():    
        btnAgregarRegistro.disabled =  False
        btnEditarRegistro.disabled = False
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
    # LIST VIEWS
    lv = ft.ListView(expand=1, auto_scroll=True)
    listadep = ft.ListView(spacing=5, auto_scroll=True, width=400)
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
            ft.DataColumn(ft.Text('REGIÓN')),
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
                         ,cr.NombreRegion
                         ,Telefonos
                     FROM CatDepositoVehicular cdv 
               INNER JOIN CatRegion cr ON cdv.RegionId = cr.Id'''
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


    def regionesAdd():
        nuevaRegion = regionNombre.value.upper()
        consultaSql = 'INSERT INTO CatRegion (NombreRegion, Activo) VALUES(?, 1)'
        btnAgregarRegistro.disabled = True
        page.update()
        try:            
            run_query(consultaSql, (nuevaRegion,))                       
            regionesLista()
            limpiarControles()
            botonesAgregar()
            alerta('EXITOSO', 'SE AGREGO CORRECTAMENTE A ' + nuevaRegion)            
        except Exception as ex:
            alerta('WARNING', 'OCURRIO UN ERROR')
        # btnAgregarRegistro.visible = True
        # page.update()    


    def regionesUpdate():
        regid = regionId.value
        nuevaRegion = regionNombre.value.upper()
        estatusRegion = regionActivo.value
        btnEditarRegistro.disabled = True
        page.update()
        consultaSql = 'UPDATE CatRegion SET [NombreRegion] = ? , Activo = ? WHERE Id = ? '        
        try:
            run_query(consultaSql,(nuevaRegion, estatusRegion,regid))            
            regionesLista()          
            limpiarControles()
            botonesAgregar()
            alerta('EXITOSO', 'SE ACTUALIZO CORRECTAMENTE A ' + nuevaRegion)
            btnEditarRegistro.disabled = False            
        except Exception as ex:
            alerta('WARNING', 'OCURRIO UN ERROR')
        # page.update()
        

    def municipioAdd():
            municipio = municipioNombreProp.value
            regionId = regionSeleccionada()
            consultaSql = 'INSERT INTO CatMunicipio (Municipio, RegionId) VALUES (? , ?)'
            try:
                run_query(consultaSql, (municipio, int(regionId),))
                btnAgregarRegistro.disabled = True
                alerta('EXITOSO', 'REGISTRO GUARDADO EXITOSAMENTE')
                btnAgregarRegistro.disabled = False
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
    # MunicipioId = Dropdown(label= 'MUNICIPIO', width=500, enable_filter= True, editable= True) #, on_change=lambda _:regionSeleccionada())
    # SE ACTUALIZO PARA SELECCIONAR LA REGION, OCUPARE EL CONTROL <municipioSelectRegion>
    DireccionDeposito = ft.TextField(label='DIRECCIÓN', width= 700)
    NombreCompletoContactos = ft.TextField(label='NOMBRE DE CONTACTO', width= 450)
    CorreoElectronicoContacto = ft.TextField(label='CORREO ELECTRONICO', width= 400)
    Telefonos = ft.TextField(label='TELEFONO(S)', width= 300)    
    Latitud = ft.TextField(label='LATITUD', width=450)
    Longitud = ft.TextField(label='LONGITUD', width=450)    
    Ubicacion = ft.TextField(label='UBICACION (MAPS)', width=450)
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
                                alignment=ft.Alignment(0.0,0.0),
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
        municipioSelectRegion.options = []
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
        # encabezado = ft.Text('CATÁLOGO DE DEPOSITOS', size= 30)
        # encabezado = ft.Text('COORDENADAS')
        btnAgregarRegistro.on_click = lambda _:depositoAdd()
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
                ], expand=True
            ),
            ft.Row(
                vertical_alignment= ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        controls=[municipioSelectRegion]
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
                vertical_alignment= ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(                        
                        controls=[Ubicacion]
                    )
                ]
            ),
            ft.Row(
                vertical_alignment= ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(                        
                        controls=[ft.Text('COORDENADAS', size= 15, weight= 20)]
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
                        height=250,
                        alignment=ft.alignment.top_center,
                        content = lv
                    )
                ], expand=True              
            )
        )
        depositosLista()
        # municipiosDropDownList()
        regionesDropDownList()
        botonesAgregar()


    def show_RolesDepositos():        
        page.controls.clear()
        texto = ft.Text('ROLES DE DEPOSITOS', size= 30)        
        page.add(texto)
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
        bgcolor= ft.Colors.LIGHT_BLUE_800,
        indicator_color= ft.Colors.GREEN_400,
        overlay_color= ft.Colors.AMBER_400
    )

    page.navigation_bar = barradeNavegacion
    show_CatRegiones()    

ft.app(target= main)