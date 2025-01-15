import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_agregar_producto(client):
    response = client.post('/producto', json={"nombre": "Peras", "cantidad": 50})
    assert response.status_code == 201
    assert response.json["message"] == "Producto agregado exitosamente"

def test_obtener_producto_existente(client):
    # Se asume que el ID 1 existe en la base de datos
    response = client.get('/producto/1')
    assert response.status_code == 200
    assert "id_producto" in response.json
    assert "nombre" in response.json
    assert "cantidad" in response.json

def test_obtener_producto_inexistente(client):
    response = client.get('/producto/9999')  # Se asume que el ID 9999 no existe
    assert response.status_code == 404
    assert response.json["error"] == "Producto no encontrado"

def test_actualizar_producto_existente(client):
    # Se asume que el ID 1 existe en la base de datos
    response = client.put('/producto/1', json={"cantidad": 100})
    assert response.status_code == 200
    assert response.json["message"] == "Producto actualizado exitosamente"

def test_actualizar_producto_inexistente(client):
    response = client.put('/producto/9999', json={"cantidad": 100})
    assert response.status_code == 404
    assert response.json["error"] == "Producto no encontrado"

def test_agregar_producto_datos_invalidos(client):
    response = client.post('/producto', json={"nombre": "", "cantidad": -10})
    assert response.status_code == 400
    assert response.json["error"] == "Datos inválidos"