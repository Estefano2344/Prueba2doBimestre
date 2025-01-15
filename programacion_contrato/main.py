from db_config import get_connection

def actualizar_stock(id_producto, nueva_cantidad):
    assert isinstance(id_producto, int) and id_producto > 0, "El ID del producto debe ser un entero positivo."
    assert isinstance(nueva_cantidad, int) and nueva_cantidad >= 0, "La nueva cantidad debe ser un entero no negativo."
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET cantidad = %s WHERE id_producto = %s", (nueva_cantidad, id_producto))
    conn.commit()
    conn.close()
    return {"message": "Stock actualizado exitosamente."}

# Pruebas manuales
if __name__ == "__main__":
    print(actualizar_stock(1, 100))
