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
    response = client.post('/producto', json={"nombre": "Peras", "cantidad": 20})
    assert response.status_code == 201
    assert response.json["message"] == "Producto agregado exitosamente"

def test_obtener_producto(client):
    response = client.get('/producto/1')
    assert response.status_code in [200, 404]  # Dependiendo si el producto existe o no

def test_actualizar_producto(client):
    response = client.put('/producto/1', json={"cantidad": 50})
    assert response.status_code in [200, 404]  # Dependiendo si el producto existe o no
