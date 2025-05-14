import flet as ft
from flet import *
import pyodbc

def main(page:ft.Page):
    # servidor = 'ECI-SDMYT-001'
    servidor = 'DESKTOP-SMKHTJB'
    basedatos = 'DepositoVehicular'
    
    stringConexion = f"DRIVER={{SQL Server}}; SERVER={servidor}; DATABASE={basedatos}; Trusted_Connection=yes"   #  CADENA DE CONEXION

    page.theme_mode = ft.ThemeMode.LIGHT
    # ancho_win = 800
    # largo_win = 1000
    
    # page.window_width=ancho_win
    # page.window_height=largo_win

    # page.window.max_width=ancho_win
    # page.window.max_height=largo_win

    # page.window.min_width=ancho_win
    # page.window.min_height=largo_win

    # anchocol = 180

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


    def cargarRegiones():
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


    def cargarMunicipiosLista():
        consultaSql = 'SELECT cmun.[Id],UPPER([Municipio]),creg.NombreRegion FROM [CatMunicipio] cmun INNER JOIN CatRegion creg ON cmun.RegionId = creg.Id ORDER BY cmun.Id'
        municipiosDb = run_query(consultaSql)
        lv.controls.clear()
        lv.controls.append(lista_municipios)
        gererar_tabla(municipiosDb)
        page.update()


    def gererar_tabla(filas):
        rows = []
        for fila in filas:
            cells = []
            for col in fila:
                cells.append(ft.DataCell(ft.Text(col)))
            rows.append(ft.DataRow(cells=cells, on_select_changed=selectedrow))
        lista_municipios.rows = rows
        page.update()


    def selectedrow(e):
        municipioIdSelected = str(e.control.cells[0].content.value)
        consultaSql = 'SELECT cm.Id, UPPER(Municipio), RegionId, cre.NombreRegion [region] FROM CatMunicipio cm INNER JOIN CatRegion cre ON cm.RegionId = cre.Id WHERE cm.Id = ?'        
        municipioDb = run_query(consultaSql,(municipioIdSelected,))
        municipioIdProp.value = str(municipioDb[0][0])
        municipioNombreProp.value = str(municipioDb[0][1])
        municipioSelectRegion.value = str(municipioDb[0][2]) + '- ' + str(municipioDb[0][3])
        controlesEditar()
        page.update()


    def municipioAdd():
        municipio = municipioNombreProp.value
        regionId = regionSeleccionada()
        consultaSql = 'INSERT INTO CatMunicipio (Municipio, RegionId) VALUES (? , ?)'
        try:
            run_query(consultaSql, (municipio, int(regionId),))
            alerta('EXITOSO', 'REGISTRO GUARDADO EXITOSAMENTE')
            cargarMunicipiosLista()
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
            cargarMunicipiosLista()
            limpiarControles()
        except Exception as ex:
            print('ERROR AL ACRTUALIZAR')
            

    def limpiarControles():
        municipioIdProp.value = ''
        municipioNombreProp.value = ''
        # municipioSelectRegion.options = []
        # cargarRegiones()
        controlesAgregar()
        page.update()
        

    def controlesAgregar():
        btnAgregar.visible = True
        btnEditar.visible = False
        btnCancelarEdicion.visible = False
        page.update()


    def controlesEditar():
        btnAgregar.visible = False
        btnEditar.visible = True
        btnCancelarEdicion.visible = True
        page.update()    


    def cancelarEdicion():
        controlesAgregar()
        limpiarControles()
        page.update()


    def regionSeleccionada(): # (e):
        textoSeleccionado = municipioSelectRegion.value
        posicion = textoSeleccionado.find('-')
        if posicion != -1:
            valor = textoSeleccionado[:posicion]
            # labelIdReg.value = f'VALOR Id: {valor}'
            return valor
        else:
            # labelIdReg.value = 'OCURRIO UN ERROR AL SELECCIONAR EL ELEMENTO'
            alerta('ALERTA', 'OCURRIO UN ERROR AL SELECCIONAR EL ELEMENTO')
        page.update()


    lv = ft.ListView(expand=1, auto_scroll=False)
    lista_municipios = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('ID')),
            ft.DataColumn(ft.Text('MUNICIPIO')),
            ft.DataColumn(ft.Text('REGION'))
        ], rows=[]
    )

    labelIdReg = ft.Text(size=50, color= Colors.GREEN_300)

    # FORMULARIO
    municipioIdProp = ft.TextField(label='Id', width= 80, read_only= True)
    municipioNombreProp = ft.TextField(label='MUNICIPIO', width= 720)
    municipioSelectRegion = Dropdown(label= 'REGIÓN', width=350, enable_filter= True, editable= True, on_change=lambda _:regionSeleccionada())
    # BOTONES
    btnAgregar = ft.CupertinoFilledButton('AGREGAR', width= 120, opacity_on_click=0.3, border_radius=10, on_click=lambda _:municipioAdd())
    btnEditar = ft.CupertinoFilledButton('EDITAR', width= 120, opacity_on_click=0.3, border_radius=10, visible= False, on_click=lambda _:municipioUpdate())
    btnCancelarEdicion = ft.CupertinoFilledButton('CANCELAR', width= 120, opacity_on_click=0.3, border_radius=10, visible= False, on_click=lambda _:cancelarEdicion())
    
    page.add(
        ft.Row(
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            controls= [
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
            controls=[btnAgregar, btnEditar, btnCancelarEdicion]
        ),
        ft.Row(
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=800,
                    height=450,
                    alignment=ft.alignment.top_center, 
                    content=lv
                )
            ]             
        ),
        ft.Row(
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            controls=[labelIdReg]
        )
    )

    controlesAgregar()
    cargarRegiones()
    cargarMunicipiosLista()


ft.app(target=main)