"""Capa vista: muestra información y solicita datos al usuario."""

ANCHO = 78


def mostrar_mensaje(texto):
    print(texto)


def mostrar_exito(texto):
    print(f"[OK] {texto}")


def mostrar_error(texto):
    print(f"[ERROR] {texto}")


def mostrar_titulo(texto):
    print("\n" + "=" * ANCHO)
    print(texto)
    print("=" * ANCHO)


def pedir_texto(mensaje):
    return input(f"{mensaje} ").strip()


def mostrar_bienvenida(fecha_texto, cantidad_productos):
    mostrar_titulo("DISTRIBUIDORA INDUSTRIAL DEL PACÍFICO S.A.")
    print("Sistema de Gestión de Inventarios y Punto de Venta")
    print(f"Fecha del sistema: {fecha_texto} | Productos en catálogo: {cantidad_productos}")


def mostrar_menu():
    mostrar_titulo("MENÚ PRINCIPAL")
    print("1. Registrar producto")
    print("2. Actualizar stock")
    print("3. Realizar venta")
    print("4. Generar alertas")
    print("5. Consultar inventario")
    print("6. Consultar ventas de la sesión")
    print("0. Salir")
    print("-" * ANCHO)


def mostrar_inventario(filas):
    mostrar_titulo("INVENTARIO")
    if not filas:
        print("El catálogo está vacío.")
        return
    encabezado = f"{'Código':<10} {'Nombre':<22} {'Categoría':<14} {'Stock':>6} {'Mín.':>5} {'P. venta':>12} {'Vence':<10}"
    print(encabezado)
    print("-" * len(encabezado))
    for p in filas:
        marca = " *" if p["stock_bajo"] else ""
        print(f"{p['codigo']:<10} {p['nombre'][:22]:<22} {p['categoria'][:14]:<14} {p['stock']:>6}{marca:<2} {p['stock_minimo']:>5} {p['precio_venta']:>12,.2f} {p['fecha_vencimiento'] or '-':<10}")
    print("* = stock bajo (stock igual o inferior al mínimo)")


def mostrar_alertas(alertas):
    mostrar_titulo("ALERTAS GENERADAS")
    if not alertas:
        print("No hay alertas.")
        return
    for alerta in alertas:
        print(f"{alerta['codigo_producto']} | {alerta['tipo_alerta']} | {alerta['mensaje']}")
    print(f"Total de alertas: {len(alertas)}")


def mostrar_resumen_venta(lineas, subtotal, total_impuestos, total_general, tasa):
    mostrar_titulo("RESUMEN DE LA VENTA")
    print(f"{'Código':<10} {'Producto':<22} {'Cant.':>6} {'P. unit.':>12} {'Subtotal':>12}")
    print("-" * 66)
    for linea in lineas:
        print(f"{linea['codigo']:<10} {linea['nombre'][:22]:<22} {linea['cantidad']:>6} {linea['precio_unitario']:>12,.2f} {linea['subtotal']:>12,.2f}")
    print("-" * 66)
    print(f"{'Subtotal:':<25} ₡{subtotal:>12,.2f}")
    print(f"{'Impuesto (' + format(tasa * 100, '.0f') + '%):':<25} ₡{total_impuestos:>12,.2f}")
    print(f"{'TOTAL A PAGAR:':<25} ₡{total_general:>12,.2f}")


def mostrar_stock_actualizado(cambios):
    print("Stock actualizado:")
    for cambio in cambios:
        print(f"{cambio['codigo']} - {cambio['nombre']}: {cambio['anterior']} -> {cambio['nuevo']}")


def mostrar_ventas(ventas, resumen):
    mostrar_titulo("VENTAS DE LA SESIÓN")
    if not ventas:
        print("Aún no se han realizado ventas en esta sesión.")
        return
    print(f"{'Factura':<10} {'Fecha':<12} {'Líneas':>7} {'Impuestos':>14} {'Total':>14}")
    print("-" * 62)
    for venta in ventas:
        print(f"{venta['numero_factura']:<10} {venta['fecha']:<12} {len(venta['productos_vendidos']):>7} {venta['total_impuestos']:>14,.2f} {venta['total_general']:>14,.2f}")
    print("-" * 62)
    print(f"Ventas realizadas: {resumen['cantidad_ventas']}")
    print(f"Impuestos acumulados: ₡{resumen['total_impuestos']:,.2f}")
    print(f"TOTAL ACUMULADO: ₡{resumen['total_general']:,.2f}")
