import pytest
from unittest.mock import patch, MagicMock
from main import actualizar_stock

# Mock para la conexión a la base de datos
def mock_get_connection():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn


@patch("main.get_connection", side_effect=mock_get_connection)
def test_actualizar_stock_exitoso(mock_get_connection):
    id_producto = 1
    nueva_cantidad = 100

    resultado = actualizar_stock(id_producto, nueva_cantidad)

    # Verifica el resultado
    assert resultado == {"message": "Stock actualizado exitosamente."}

    # Verifica que se llamaron los métodos del mock
    mock_get_connection.assert_called_once()
    mock_conn = mock_get_connection.return_value
    mock_cursor = mock_conn.cursor.return_value

    mock_cursor.execute.assert_called_once_with(
        "UPDATE productos SET cantidad = %s WHERE id_producto = %s",
        (nueva_cantidad, id_producto),
    )
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

def test_actualizar_stock_id_producto_invalido():
    with pytest.raises(AssertionError, match="El ID del producto debe ser un entero positivo."):
        actualizar_stock(-1, 100)

    with pytest.raises(AssertionError, match="El ID del producto debe ser un entero positivo."):
        actualizar_stock("uno", 100)

def test_actualizar_stock_cantidad_invalida():
    with pytest.raises(AssertionError, match="La nueva cantidad debe ser un entero no negativo."):
        actualizar_stock(1, -100)

    with pytest.raises(AssertionError, match="La nueva cantidad debe ser un entero no negativo."):
        actualizar_stock(1, "cien")

def test_actualizar_stock_conexion_fallida():
    with patch("main.get_connection", side_effect=Exception("Error de conexión")):
        with pytest.raises(Exception, match="Error de conexión"):
            actualizar_stock(1, 100)
