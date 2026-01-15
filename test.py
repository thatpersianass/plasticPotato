import pytest
import crear_bbdd
import consultas
import transacciones
from connection import get_connection

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """ 
    Fixture que prepara la base de datos antes de ejecutar los tests.
    Reinicia las tablas y carga los datos iniciales de Connor Kauffman, Rawayana y Neomai.
    """
    crear_bbdd.crear_estructura()
    yield

# --- TESTS DE CONEXIÓN Y ESTRUCTURA ---

def test_conexion_servidor():
    """ Verifica que la conexión con el host localhost y puerto 5432 es exitosa. """
    conn = get_connection()
    assert conn is not None
    conn.close()

# --- TESTS DE CONSULTAS OBLIGATORIAS ---

def test_consulta_generos_rock():
    """ Verifica que la búsqueda por género 'Rock' devuelve discos (Connor/Rawayana/Neomai). """
    resultados = consultas.consulta_generos('Rock')
    assert len(resultados) >= 3  # Al menos Leavin You, Malportada y Carmesí
    # Verificamos que los títulos sean correctos
    titulos = [r[0] for r in resultados]
    assert 'Leavin You' in titulos
    assert 'Carmesí' in titulos

def test_consulta_compras_cliente():
    """ Verifica los discos comprados por 'José Joselito'. """
    compras = consultas.consulta_cliente('José Joselito')
    assert len(compras) == 2
    assert compras[0][0] == 'Malportada'

def test_consulta_colaboradores():
    """ Verifica que Neomai aparece como colaboradora en 'Síndrome de Stendhal'. """
    artistas = consultas.consulta_colaboradores('Síndrome de Stendhal')
    assert len(artistas) > 0

    assert artistas[0][0] == 'Neomai'

# --- TESTS DE TRANSACCIONES (COMMIT Y ROLLBACK) ---

def test_transaccion_exitosa_commit():
    """ Verifica que insertar un artista y disco en una transacción persiste los datos. """
    exito = transacciones.insertar_artista_y_disco(
        'Prueba', 'Test', 'España', 'Disco Test', 2026, ['Test']
    )
    assert exito is True

    res = consultas.consulta_colaboradores('Disco Test')
    assert len(res) > 0

def test_transaccion_rollback_fallido():
    """ 
    Verifica que ante un error de integridad (ID duplicado), 
    la base de datos ejecuta un ROLLBACK y no guarda datos parciales.
    """
    # Intentamos la demostración de fallo por ID duplicado
    resultado_msg = transacciones.rollback_duplicado() 
    assert "ROLLBACK EXITOSO" in resultado_msg
    
    # Verificamos que el 'Artista Fantasma' NO existe en la base de datos
    artistas = consultas.listar_todos_artistas()
    nombres_artistas = [a[1] for a in artistas]
    assert 'Artista' not in nombres_artistas

# --- TESTS DE ACTUALIZACIÓN Y BORRADO ---

def test_actualizar_pedido():
    """ Verifica la modificación del array de discos en una venta. """
    exito = transacciones.actualizar_discos_venta(1, [3])
    assert exito is True

    ventas = consultas.listar_todas_ventas()
    venta_actualizada = next(v for v in ventas if v[0] == 1)
    assert venta_actualizada[3] == [3]

def test_eliminar_pedido():
    """ Verifica el borrado físico de una venta. """
    exito = transacciones.eliminar_venta(1)
    assert exito is True

    ventas = consultas.listar_todas_ventas()
    ids_ventas = [v[0] for v in ventas]
    assert 1 not in ids_ventas