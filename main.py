# Curso: Fundamentos de Tecnología Digitales
# Profesor: Adonis Aleman G.
# Estudiante: Leandro Cordero

import sys
import controlador


def main():
    fecha_texto = sys.argv[1] if len(sys.argv) > 1 else None
    controlador.iniciar(fecha_texto)
    continuar = True
    try:
        while continuar:
            controlador.mostrar_menu()
            opcion = controlador.leer_opcion()
            continuar = controlador.procesar_opcion(opcion)
    except (EOFError, KeyboardInterrupt):
        print()
    finally:
        controlador.despedirse()


if __name__ == "__main__":
    main()
