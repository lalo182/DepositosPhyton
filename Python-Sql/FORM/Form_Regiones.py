import flet as ft
import pyodbc

def main(page:ft.Page):
    servidor = 'ECI-SDMYT-001'
    # servidor = 'DESKTOP-SMKHTJB'
    basedatos = 'DepositoVehicular'
    
    stringConexion = f"DRIVER={{SQL Server}}; SERVER={servidor}; DATABASE={basedatos}; Trusted_Connection=yes"   #  CADENA DE CONEXION

    page.theme_mode = ft.ThemeMode.DARK
    ancho_win = 750
    largo_win = 850
    page.window_height=largo_win
    page.window_width=ancho_win
    page.window.max_height=largo_win
    page.window.max_width=ancho_win
    page.window.min_height=largo_win
    page.window.min_width=ancho_win

    anchocol = 220
    
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

    # ELEMENTOS PARA LA PLANTILLA
    regionId = ft.TextField(label='Id', width=anchocol, read_only=True)
    regionNombre = ft.TextField(label='Region', width=anchocol)
    regionActivo = ft.Checkbox(label='Disponible', visible= False)

    # BOTONES
    btnEditarRegistro = ft.CupertinoFilledButton('EDITAR', width=120, opacity_on_click=0.3, border_radius=10, visible = False, on_click=lambda _:regionesUpdate())
    btnAgregarRegistro = ft.CupertinoFilledButton('AGREGAR', width=120, opacity_on_click=0.3, border_radius=10, visible = True, on_click=lambda _:regionesAdd())       

    lv = ft.ListView(expand=1, auto_scroll=True)
    lista_regiones = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('ID')),
            ft.DataColumn(ft.Text('REGIÓN')),
            ft.DataColumn(ft.Text('ESTATUS'))
        ], rows=[],
    )
    
    # METODO PARA OBTENER LA LISTA DE REGIONES
    def regionesLista():   # EN EL EJEMPLO, ES LA FUNCION [def listadiaria():]
        consultaSql = 'SELECT Id, NombreRegion, Activo FROM CatRegion'
        regionesdb = run_query(consultaSql)
        lv.controls.clear()
        lv.controls.append(lista_regiones)
        generar_tabla(regionesdb)
        page.update()

    def selectedrow(e):    
        if e.control.selected:
            e.control.selected=False
        else:
            e.control.selected=True
            idreg = int(e.control.cells[0].content.value)
            reg = str(e.control.cells[1].content.value)
            act = bool(e.control.cells[2].content.value)
            # act = str(e.control.cells[2].content.value)
            regionId.value = idreg
            regionNombre.value = reg
            regionActivo.value = act
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
        #page.update()

    def limpiarControles():
        regionId.value = ''
        regionNombre.value = ''
        regionActivo.value = False
        botonesAgregar()

    # def regionesAdd(nuevaRegion):        
    def regionesAdd():
        nuevaRegion = regionNombre.value.upper()
        consultaSql = 'INSERT INTO CatRegion (NombreRegion, Activo) VALUES(?, 1)'
        try:
            run_query(consultaSql, (nuevaRegion,))
            regionesLista()
            limpiarControles()
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
            alerta('EXITOSO', 'SE ACTUALIZO CORRECTAMENTE A ' + nuevaRegion)
        except Exception as ex:
            alerta('WARNING', 'OCURRIO UN ERROR')

    def botonesAgregar():
        regionActivo.visible = False
        btnAgregarRegistro.visible =  True
        btnEditarRegistro.visible = False        
        page.update()

    def botonesEditar():
        regionActivo.visible = True
        btnAgregarRegistro.visible = False
        btnEditarRegistro.visible = True
        print(regionNombre.value)
        page.update()

    def alerta(titulo, mensaje):
        dlg = ft.AlertDialog(title= ft.Text(titulo), content= ft.Text(mensaje))
        page.open(dlg)
        

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
                                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                                    ft.Row(controls = [btnAgregarRegistro]),
                                    # ft.CupertinoFilledButton('AGREGAR', 
                                    #                          width=220, 
                                    #                          opacity_on_click=0.3,
                                    #                          border_radius=10, 
                                    #                          on_click=lambda _:regionesAdd(regionNombre.value.upper())),
                                    ft.Row(controls= [btnEditarRegistro])
                                    #ft.CupertinoFilledButton()  
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
                    #     ,
                    #     ft.Row(controls = [
                    #         ft.CupertinoFilledButton('Actualizar Lista', 
                    #                                          width=220, 
                    #                                          opacity_on_click=0.3,
                    #                                          border_radius=10, 
                    #                                          on_click=lambda _:regionesLista())
                    #     ]
                    # )
                ])
            ]
        )
    )

    botonesAgregar()
    regionesLista()

ft.app(target=main)