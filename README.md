# Distribuidora Industrial del Pacífico S.A.

Proyecto de Python para administrar un inventario y registrar ventas mediante un menú de consola.

## Archivos
- `main.py`: inicia el programa.
- `modelo.py`: administra productos, ventas y alertas en memoria.
- `vista.py`: muestra menús, mensajes y tablas.
- `controlador.py`: valida datos y coordina el programa.
- `datos/datos_prueba.csv`: catálogo de ejemplo que se carga al iniciar.

## Cómo ejecutar
Necesita Python 3. Abra una terminal en esta carpeta y ejecute:

```bash
python main.py
```

Para simular una fecha específica:

```bash
python main.py 2026-10-25
```

La fecha debe tener formato `AAAA-MM-DD`. Los datos de productos y ventas se guardan en memoria durante la ejecución; las ventas no se conservan al cerrar el programa.

## Menú
1. Registrar producto
2. Actualizar stock
3. Realizar venta
4. Generar alertas
5. Consultar inventario
6. Consultar ventas de la sesión
0. Salir
