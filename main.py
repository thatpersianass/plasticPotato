import crear_bbdd
import consultas
import transacciones

def main():
    """ 
    Punto de entrada principal de la aplicación. Gestiona el menú y 
    las llamadas a los módulos de BDOR, consultas y transacciones.
    """
    while True:
        print("""
    ==========================================================
            🎵 SISTEMA DE GESTIÓN MUSICAL (BDOR) 🎵
    ==========================================================
        1. 🛠️  Reiniciar BD (Tablas y Datos iniciales)
        2. 📋 Ver Todo (Artistas, Discos y Ventas)
        3. 🎸 Consultar Discos por Género
        4. 👤 Consultar Compras de un Cliente
        5. 🤝 Consultar Colaboradores de un Disco
        6. 💾 Añadir Artista y Disco (COMMIT)
        7. 🧨 Forzar Error de ID Duplicado (ROLLBACK)
        8. 📝 Actualizar Cliente en Pedido
        9. 🗑️  Eliminar un Pedido
        0. 🚪 Salir
    =========================================================="""
        )
        
        opcion = input("👉 Seleccione una opción: ")

        if opcion == "1":
            try:
                crear_bbdd.crear_estructura()
                print("\n✅ Estructura y datos iniciales cargados correctamente.")
            except Exception as e:
                print(f"\n❌ Error al reiniciar la base de datos: {e}")

        elif opcion == "2":
            print("\nℹ️  LISTADO COMPLETO DE LA BASE DE DATOS:")
            # Artistas
            artistas = consultas.listar_todos_artistas()
            print("\n--- Artistas ---")
            for a in artistas: print(f"  ID: {a[0]} | {a[1]} {a[2]} ({a[3]})")
            # Discos
            discos = consultas.listar_todos_discos()
            print("\n--- Discos ---")
            for d in discos: print(f"  ID: {d[0]} | {d[1]} | Géneros: {d[3]}")
            # Ventas
            ventas = consultas.listar_todas_ventas()
            print("\n--- Ventas ---")
            for v in ventas: print(f"  Venta {v[0]}: {v[1]} compró {v[3]}")

        elif opcion == "3":
            print("\n🔍 GÉNEROS DISPONIBLES:")
            lista = consultas.obtener_lista_generos()
            if not lista:
                print("⚠️  No hay géneros registrados.")
            else:
                for i, g in enumerate(lista, 1): print(f"  {i}. {g}")
                sel = int(input("\n👉 Elija el número del género: ")) - 1
                if 0 <= sel < len(lista):
                    res = consultas.consulta_generos(lista[sel])
                    print(f"\n✅ Discos de '{lista[sel]}':")
                    for r in res: print(f"  - {r[0]} ({r[1]})")
                else: print("❌ Selección no válida.")

        elif opcion == "4":
            print("\n🔍 CLIENTES CON COMPRAS:")
            lista = consultas.obtener_lista_clientes()
            if not lista:
                print("⚠️  No hay clientes con compras.")
            else:
                for i, c in enumerate(lista, 1): print(f"  {i}. {c}")
                sel = int(input("\n👉 Elija el número del cliente: ")) - 1
                if 0 <= sel < len(lista):
                    res = consultas.consulta_cliente(lista[sel])
                    print(f"\n✅ Compras de '{lista[sel]}':")
                    for r in res: print(f"  - {r[0]}")
                else: print("❌ Selección no válida.")

        elif opcion == "5":
            print("\n🔍 CATÁLOGO DE DISCOS:")
            lista = consultas.obtener_lista_titulos_discos()
            if not lista:
                print("⚠️  No hay discos registrados.")
            else:
                for i, t in enumerate(lista, 1): print(f"  {i}. {t}")
                sel = int(input("\n👉 Elija el número del disco: ")) - 1
                if 0 <= sel < len(lista):
                    res = consultas.consulta_colaboradores(lista[sel])
                    print(f"\n✅ Colaboradores en '{lista[sel]}':")
                    for r in res: print(f"  - {r[0]} {r[1]}")
                else: print("❌ Selección no válida.")

        elif opcion == "6":
            print("\nℹ️  ALTA DE NUEVO ARTISTA Y DISCO:")
            nom = input("Nombre: "); ape = input("Apellido: "); nac = input("Nacionalidad: ")
            tit = input("Título Disco: "); anio = input("Año: ")
            gens = input("Géneros (separados por coma): ").split(",")
            
            if transacciones.insertar_artista_y_disco(nom, ape, nac, tit, int(anio), [g.strip() for g in gens]):
                print("\n✅ Transacción completada: Datos persistidos en la BD.")
            else:
                print("\n❌ La transacción falló y se ejecutó un ROLLBACK.")

        elif opcion == "7":
            print("\n⚠️  EJECUTANDO PRUEBA DE ERROR (ID DUPLICADO)...")
            resultado = transacciones.rollback_duplicado()
            print(f"\nℹ️  Resultado: {resultado}")
        
        elif opcion == "8":
            print("\n📝 ACTUALIZAR CANCIONES DEL PEDIDO")
            ventas_lista = consultas.listar_todas_ventas()
            
            if not ventas_lista:
                print("⚠️ No hay pedidos registrados.")
            else:
                for i, v in enumerate(ventas_lista, 1):
                    print(f"  {i}. Pedido #{v[0]} (Cliente: {v[1]})")
                
                sel_v = int(input("\n👉 Seleccione el número de pedido a editar: ")) - 1
                id_venta_sel = ventas_lista[sel_v][0]

                print("\n🎸 CANCIONES DISPONIBLES EN EL CATÁLOGO:")
                discos_cat = consultas.obtener_discos_id_y_titulo()
                for d in discos_cat:
                    print(f"  ID: {d[0]} | Título: {d[1]}")
                
                entrada = input("\n👉 Introduzca los IDs de las nuevas canciones (separados por comas): ")
                nuevos_ids = [int(x.strip()) for x in entrada.split(",")]

                if transacciones.actualizar_discos_venta(id_venta_sel, nuevos_ids):
                    print(f"\n✅ Pedido #{id_venta_sel} actualizado con éxito con los discos: {nuevos_ids}.")
                else:
                    print("\n❌ Error: No se pudo actualizar el pedido.")

        elif opcion == "9":
            print("\n🗑️  SELECCIONE EL PEDIDO A ELIMINAR:")
            lista = consultas.listar_todas_ventas()
            if not lista:
                print("⚠️  No hay ventas para eliminar.")
            else:
                for i, v in enumerate(lista, 1):
                    print(f"  {i}. Pedido #{v[0]} - Cliente: {v[1]} ({v[2]})")
                
                sel = int(input("\n👉 Elija el número del pedido a borrar: ")) - 1
                if 0 <= sel < len(lista):
                    id_v = lista[sel][0]
                    confirmar = input(f"⚠️  ¿Seguro que desea borrar el pedido #{id_v}? (s/n): ")
                    if confirmar.lower() == 's':
                        if transacciones.eliminar_venta(id_v):
                            print(f"✅ Pedido #{id_v} eliminado correctamente.")
                        else:
                            print("❌ Error al intentar eliminar el pedido.")
                else:
                    print("❌ Selección no válida.")

        elif opcion == "0":
            print("\n👋 Saliendo del sistema. ¡Hasta pronto!")
            break
        else:
            print("\n❌ Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()