# 🎵 Sistema de Gestión Musical - Modelo Objeto-Relacional (BDOR)

Este proyecto implementa una solución avanzada para la gestión de un catálogo musical y ventas utilizando **PostgreSQL** y **Python**. El sistema aprovecha las capacidades del modelo **Objeto-Relacional** para manejar estructuras de datos complejas como tipos compuestos y arrays, optimizando la integridad y la eficiencia de las consultas.

---

## 🧠 Memoria de Decisiones Técnicas

El diseño se centra en reducir la complejidad de las relaciones N:M tradicionales mediante el uso de herramientas nativas de PostgreSQL.

### 1. Modelado de Datos
* **Tipos Compuestos (`artist_type`, `sale_info`)**: Se han definido tipos de datos personalizados para agrupar atributos relacionados. Esto permite tratar filas de la base de datos como objetos estructurados, facilitando el mapeo en Python.
* **Arrays de Datos (`TEXT[]`, `INTEGER[]`)**: Se utilizan para almacenar géneros musicales y colecciones de IDs de artistas/discos. Esto elimina la necesidad de múltiples tablas puente, simplificando la lógica de negocio y los `JOIN`.

### 2. Gestión de Transacciones (Atomicidad)
Se implementó una lógica estricta de **Commit** y **Rollback**:
* **Éxito**: Operaciones compuestas (como insertar un artista y su disco simultáneamente) se confirman juntas.
* **Resiliencia**: Si cualquier parte de una transacción falla, se ejecuta un `ROLLBACK` automático, garantizando que no queden datos parciales o huérfanos.

---

## 🧪 Explicación Detallada de los Tests (Pytest)

La suite de pruebas automatizadas en `test.py` es el núcleo de validación del sistema. Se han implementado **8 tests críticos** para asegurar la estabilidad:

* **Integridad de Conexión (`test_conexion`)**: Verifica que el puente `psycopg2` entre Python y el host de PostgreSQL (5432) es estable.
* **Consultas BDOR (`test_generos`, `test_compras`, `test_colaboradores`)**: 
    * Validan que el operador `ANY` recorre correctamente los **arrays** de géneros.
    * Comprueban que el acceso por punto `(tipo_compuesto).campo` extrae los datos esperados de los objetos.
* **Validación de Rollback (`test_rollback`)**: 
    * Forzamos una violación de clave primaria (ID duplicado).
    * El test verifica que el sistema detecta el error y que el primer registro de la transacción **no se guardó**, confirmando la **atomicidad**.
* **Ciclo CRUD (`test_actualizar`, `test_eliminar`)**: Asegura que las modificaciones en los arrays de los pedidos y el borrado físico de registros funcionan sin corromper el resto de la base de datos.



---

## ⚙️ Configuración de PostgreSQL

Para que el proyecto funcione, la base de datos debe cumplir con los siguientes requisitos:

1.  **Creación de la BD**: Crear una base de datos llamada `music_store`.
2.  **Codificación**: Asegurar que sea `UTF-8` para soportar tildes en nombres como "Pérez" o "Carmesí".
3.  **Permisos**: El usuario (ej. `postgres`) debe tener permisos para ejecutar `CREATE TYPE` y `DROP TYPE`.

### Parámetros de Conexión (`connection.py`)
```python
host="localhost",
database="music_store",
user="tu_usuario",
password="tu_password"
📊 Comparativa de ModelosCaracterísticaRelacional ClásicoModelo Objeto-Relacional (BDOR)Relaciones Muchos a MuchosTablas intermedias/puente.Arrays de Identificadores.Atributos de FilaSolo datos atómicos.Tipos Compuestos (Objetos).Consultas ComplejasMúltiples JOINs.Acceso directo a campos del objeto.IntegridadNormalización estricta.Encapsulamiento de datos relacionados.🚀 Guía de Uso RápidoInstalaciónBashpip install psycopg2-binary pytest
EjecuciónMenú Principal: python main.py (Incluye feedback visual con iconos ✅, ❌ y ⚠️).Ejecutar Tests: python -m pytest -v test.pyProyecto desarrollado para la práctica de Bases de Datos Objeto-Relacionales. Dataset: Connor Kauffman, Rawayana, Neomai, MicroTDH.
---

### ¿Cómo guardarlo?
1. Copia todo el contenido del bloque de arriba.
2. Abre un editor de texto (Notepad, VS Code, etc.).
3. Pega el contenido.
4. Guarda el archivo como **`README.md`** en la raíz de tu proyecto.

**¿Hay algún otro detalle de la configuración o del código que quieras ajustar antes de subirlo a tu repositorio?**