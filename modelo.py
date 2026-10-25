"""Capa modelo: mantiene los datos del sistema en memoria."""

import copy
import csv
from datetime import date, datetime

FORMATO_FECHA = "%Y-%m-%d"
_catalogo = []
_ventas = []
_alertas = []
_fecha_sistema = date.today()


def fijar_fecha(texto_fecha):
    global _fecha_sistema
    _fecha_sistema = datetime.strptime(texto_fecha, FORMATO_FECHA).date()


def obtener_fecha():
    return _fecha_sistema


def buscar_producto(codigo):
    codigo = codigo.strip().upper()
    for producto in _catalogo:
        if producto["codigo"] == codigo:
            return producto
    return None


def obtener_producto(codigo):
    producto = buscar_producto(codigo)
    return copy.deepcopy(producto) if producto is not None else None


def existe_producto(codigo):
    return buscar_producto(codigo) is not None


def cantidad_productos():
    return len(_catalogo)


def agregar_producto(producto):
    codigo = producto["codigo"].strip().upper()
    if existe_producto(codigo):
        raise ValueError("El código del producto ya existe.")
    nuevo = dict(producto)
    nuevo["codigo"] = codigo
    _catalogo.append(nuevo)


def obtener_catalogo():
    return copy.deepcopy(_catalogo)


def incrementar_stock(codigo, cantidad):
    producto = buscar_producto(codigo)
    if producto is None:
        raise ValueError("No existe un producto con ese código.")
    producto["stock"] += cantidad
    return producto["stock"]


def descontar_stock(codigo, cantidad):
    producto = buscar_producto(codigo)
    if producto is None:
        raise ValueError("No existe un producto con ese código.")
    if producto["stock"] < cantidad:
        raise ValueError("No hay suficiente stock disponible.")
    producto["stock"] -= cantidad
    return producto["stock"]


def cargar_catalogo_desde_csv(ruta):
    cargados = 0
    with open(ruta, newline="", encoding="utf-8-sig") as archivo:
        for fila in csv.DictReader(archivo):
            try:
                producto = {
                    "codigo": fila["codigo"].strip().upper(),
                    "nombre": fila["nombre"].strip(),
                    "categoria": fila["categoria"].strip(),
                    "stock": int(fila["stock"]),
                    "stock_minimo": int(fila["stock_minimo"]),
                    "precio_compra": float(fila["precio_compra"]),
                    "precio_venta": float(fila["precio_venta"]),
                    "fecha_vencimiento": fila.get("fecha_vencimiento", "").strip(),
                }
                if producto["fecha_vencimiento"]:
                    datetime.strptime(producto["fecha_vencimiento"], FORMATO_FECHA)
                if producto["stock"] < 0 or producto["stock_minimo"] < 0:
                    continue
                if producto["precio_compra"] < 0 or producto["precio_venta"] < 0:
                    continue
                agregar_producto(producto)
                cargados += 1
            except (ValueError, KeyError, TypeError):
                continue
    return cargados


def siguiente_numero_factura():
    return f"F-{len(_ventas) + 1:04d}"


def registrar_venta(venta):
    _ventas.append(copy.deepcopy(venta))


def obtener_ventas():
    return copy.deepcopy(_ventas)


def limpiar_alertas():
    _alertas.clear()


def agregar_alerta(codigo_producto, tipo_alerta, mensaje):
    _alertas.append({
        "codigo_producto": codigo_producto,
        "tipo_alerta": tipo_alerta,
        "mensaje": mensaje,
    })


def obtener_alertas():
    return copy.deepcopy(_alertas)


def reiniciar():
    global _fecha_sistema
    _catalogo.clear()
    _ventas.clear()
    _alertas.clear()
    _fecha_sistema = date.today()
