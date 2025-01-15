from db_config import get_connection

def consultar_producto(id_producto):
    if not isinstance(id_producto, int) or id_producto <= 0:
        return {"error": "El ID del producto debe ser un número entero positivo."}
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()
    conn.close()
    return producto if producto else {"error": "Producto no encontrado."}

def agregar_producto(nombre, cantidad):
    if not isinstance(cantidad, int) or cantidad <= 0:
        return {"error": "La cantidad debe ser un número entero positivo."}
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, cantidad) VALUES (%s, %s)", (nombre, cantidad))
    conn.commit()
    conn.close()
    return {"message": "Producto agregado exitosamente."}

# Pruebas manuales
if __name__ == "__main__":
    print(agregar_producto("Manzanas", 50))
    print(consultar_producto(1))
