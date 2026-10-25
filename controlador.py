"""Capa controlador: valida entradas y coordina modelo y vista."""

import csv
import math
import os
from datetime import datetime

import modelo
import vista

TASA_IMPUESTO = 0.13
DIAS_ALERTA_VENCIMIENTO = 7
RUTA_DATOS_PRUEBA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos", "datos_prueba.csv")


def validar_texto_obligatorio(texto):
    if not texto:
        return False, "Este campo es obligatorio y no puede quedar vacío."
    return True, texto


def validar_entero_positivo(texto):
    try:
        numero = int(texto)
    except ValueError:
        return False, "Digite un número entero, sin letras ni decimales."
    if numero <= 0:
        return False, "El valor debe ser mayor que cero."
    return True, numero


def validar_entero_no_negativo(texto):
    try:
        numero = int(texto)
    except ValueError:
        return False, "Digite un número entero válido."
    if numero < 0:
        return False, "El valor no puede ser negativo."
    return True, numero


def validar_flotante_no_negativo(texto):
    try:
        numero = float(texto.replace(",", "."))
    except ValueError:
        return False, "Digite un número válido, por ejemplo 1250.50."
    if not math.isfinite(numero) or numero < 0:
        return False, "Digite un número válido que no sea negativo."
    return True, numero


def validar_fecha_opcional(texto):
    if texto == "":
        return True, ""
    try:
        datetime.strptime(texto, modelo.FORMATO_FECHA)
    except ValueError:
        return False, "Fecha inválida. Use YYYY-MM-DD, por ejemplo 2026-12-31."
    return True, texto


def es_stock_bajo(producto):
    return producto["stock"] <= producto["stock_minimo"]


def dias_para_vencer(producto, fecha_actual):
    if not producto["fecha_vencimiento"]:
        return None
    vencimiento = datetime.strptime(producto["fecha_vencimiento"], modelo.FORMATO_FECHA).date()
    return (vencimiento - fecha_actual).days


def vence_pronto(dias):
    return dias is not None and dias <= DIAS_ALERTA_VENCIMIENTO


def calcular_venta(carrito):
    lineas = []
    subtotal = 0.0
    for codigo, cantidad in carrito.items():
        producto = modelo.obtener_producto(codigo)
        subtotal_linea = round(cantidad * producto["precio_venta"], 2)
        lineas.append({
            "codigo": codigo,
            "nombre": producto["nombre"],
            "cantidad": cantidad,
            "precio_unitario": producto["precio_venta"],
            "subtotal": subtotal_linea,
        })
        subtotal += subtotal_linea
    subtotal = round(subtotal, 2)
    impuestos = round(subtotal * TASA_IMPUESTO, 2)
    total = round(subtotal + impuestos, 2)
    return lineas, subtotal, impuestos, total


def calcular_stock_sugerido(producto):
    return max(producto["stock_minimo"] * 2 - producto["stock"], 1)


def solicitar(mensaje, validador):
    while True:
        texto = vista.pedir_texto(mensaje)
        valido, resultado = validador(texto)
        if valido:
            return resultado
        vista.mostrar_error(resultado)


def registrar_producto():
    vista.mostrar_titulo("REGISTRAR PRODUCTO")
    codigo = solicitar("Código del producto:", validar_texto_obligatorio).upper()
    if modelo.existe_producto(codigo):
        vista.mostrar_error("Ya existe un producto con ese código.")
        return
    nombre = solicitar("Nombre:", validar_texto_obligatorio)
    categoria = solicitar("Categoría:", validar_texto_obligatorio)
    stock = solicitar("Stock inicial:", validar_entero_no_negativo)
    stock_minimo = solicitar("Stock mínimo:", validar_entero_no_negativo)
    precio_compra = solicitar("Precio de compra (₡):", validar_flotante_no_negativo)
    precio_venta = solicitar("Precio de venta (₡):", validar_flotante_no_negativo)
    fecha_vencimiento = solicitar("Fecha de vencimiento (YYYY-MM-DD) o Enter si no aplica:", validar_fecha_opcional)
    modelo.agregar_producto({
        "codigo": codigo,
        "nombre": nombre,
        "categoria": categoria,
        "stock": stock,
        "stock_minimo": stock_minimo,
        "precio_compra": precio_compra,
        "precio_venta": precio_venta,
        "fecha_vencimiento": fecha_vencimiento,
    })
    vista.mostrar_exito("Producto registrado correctamente.")


def actualizar_stock():
    vista.mostrar_titulo("ACTUALIZAR STOCK")
    codigo = solicitar("Código del producto:", validar_texto_obligatorio).upper()
    producto = modelo.obtener_producto(codigo)
    if producto is None:
        vista.mostrar_error("No existe un producto con ese código.")
        return
    cantidad = solicitar("Cantidad que desea agregar:", validar_entero_positivo)
    anterior = producto["stock"]
    nuevo = modelo.incrementar_stock(codigo, cantidad)
    vista.mostrar_stock_actualizado([{"codigo": codigo, "nombre": producto["nombre"], "anterior": anterior, "nuevo": nuevo}])


def realizar_venta():
    vista.mostrar_titulo("REALIZAR VENTA")
    if modelo.cantidad_productos() == 0:
        vista.mostrar_error("No hay productos registrados en el inventario.")
        return
    carrito = {}
    while True:
        codigo = vista.pedir_texto("Código del producto (Enter para terminar):").upper()
        if not codigo:
            break
        producto = modelo.obtener_producto(codigo)
        if producto is None:
            vista.mostrar_error("No existe un producto con ese código.")
            continue
        cantidad = solicitar("Cantidad:", validar_entero_positivo)
        cantidad_total = carrito.get(codigo, 0) + cantidad
        if producto["stock"] < cantidad_total:
            vista.mostrar_error(f"Stock insuficiente. Disponible: {producto['stock'] - carrito.get(codigo, 0)}.")
            continue
        carrito[codigo] = cantidad_total
        vista.mostrar_mensaje(f"Agregado: {producto['nombre']} x {cantidad}.")
    if not carrito:
        vista.mostrar_mensaje("No se registró ninguna venta.")
        return
    lineas, subtotal, impuestos, total = calcular_venta(carrito)
    vista.mostrar_resumen_venta(lineas, subtotal, impuestos, total, TASA_IMPUESTO)
    confirmar = vista.pedir_texto("¿Confirmar la venta? (S/N):").upper()
    if confirmar != "S":
        vista.mostrar_mensaje("Venta cancelada.")
        return
    cambios = []
    productos_vendidos = []
    for linea in lineas:
        anterior = modelo.obtener_producto(linea["codigo"])["stock"]
        nuevo = modelo.descontar_stock(linea["codigo"], linea["cantidad"])
        cambios.append({"codigo": linea["codigo"], "nombre": linea["nombre"], "anterior": anterior, "nuevo": nuevo})
        productos_vendidos.append({"codigo": linea["codigo"], "cantidad": linea["cantidad"], "subtotal": linea["subtotal"]})
    numero_factura = modelo.siguiente_numero_factura()
    modelo.registrar_venta({
        "numero_factura": numero_factura,
        "fecha": modelo.obtener_fecha().isoformat(),
        "productos_vendidos": productos_vendidos,
        "total_impuestos": impuestos,
        "total_general": total,
    })
    vista.mostrar_exito(f"Venta {numero_factura} registrada correctamente.")
    vista.mostrar_stock_actualizado(cambios)


def generar_alertas():
    modelo.limpiar_alertas()
    hoy = modelo.obtener_fecha()
    for producto in modelo.obtener_catalogo():
        if es_stock_bajo(producto):
            modelo.agregar_alerta(
                producto["codigo"], "stock_bajo",
                f"Stock {producto['stock']} <= mínimo {producto['stock_minimo']} (reponer aproximadamente {calcular_stock_sugerido(producto)}).",
            )
        dias = dias_para_vencer(producto, hoy)
        if vence_pronto(dias):
            if dias < 0:
                texto = f"VENCIDO hace {-dias} día(s) ({producto['fecha_vencimiento']})"
            elif dias == 0:
                texto = f"Vence HOY ({producto['fecha_vencimiento']})"
            else:
                texto = f"Vence en {dias} día(s) ({producto['fecha_vencimiento']})"
            modelo.agregar_alerta(producto["codigo"], "vencimiento_proximo", texto)
    vista.mostrar_alertas(modelo.obtener_alertas())


def consultar_inventario():
    filas = []
    for producto in modelo.obtener_catalogo():
        fila = dict(producto)
        fila["stock_bajo"] = es_stock_bajo(producto)
        filas.append(fila)
    vista.mostrar_inventario(filas)


def consultar_ventas_del_dia():
    ventas = modelo.obtener_ventas()
    resumen = {
        "cantidad_ventas": len(ventas),
        "total_impuestos": round(sum(v["total_impuestos"] for v in ventas), 2),
        "total_general": round(sum(v["total_general"] for v in ventas), 2),
    }
    vista.mostrar_ventas(ventas, resumen)


ACCIONES = {
    "1": registrar_producto,
    "2": actualizar_stock,
    "3": realizar_venta,
    "4": generar_alertas,
    "5": consultar_inventario,
    "6": consultar_ventas_del_dia,
}


def iniciar(fecha_texto=None):
    if fecha_texto is not None:
        try:
            modelo.fijar_fecha(fecha_texto)
        except ValueError:
            vista.mostrar_error("Fecha inválida. Use YYYY-MM-DD; se usará la fecha de hoy.")
    cargados = 0
    if os.path.exists(RUTA_DATOS_PRUEBA):
        try:
            cargados = modelo.cargar_catalogo_desde_csv(RUTA_DATOS_PRUEBA)
        except (OSError, csv.Error):  # la ausencia/lectura del archivo no impide iniciar
            cargados = 0
    vista.mostrar_bienvenida(modelo.obtener_fecha().isoformat(), modelo.cantidad_productos())
    if cargados:
        vista.mostrar_mensaje(f"Productos de prueba cargados: {cargados}.")
    else:
        vista.mostrar_mensaje("No se cargaron datos de prueba; puede registrar productos desde el menú.")


def mostrar_menu():
    vista.mostrar_menu()


def leer_opcion():
    return vista.pedir_texto("Seleccione una opción:")


def procesar_opcion(opcion):
    if opcion == "0":
        return False
    accion = ACCIONES.get(opcion)
    if accion is None:
        vista.mostrar_error("Opción no válida. Digite un número del 0 al 6.")
    else:
        accion()
    return True


def despedirse():
    vista.mostrar_mensaje("Sesión finalizada. Los datos en memoria se descartan al cerrar el programa.")
