from flask import Flask, request, jsonify
from db_config import get_connection

app = Flask(__name__)

@app.route('/producto/<int:id_producto>', methods=['GET'])
def obtener_producto(id_producto):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        producto = cursor.fetchone()
        conn.close()
        if producto:
            return jsonify(producto), 200
        return jsonify({"error": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/producto', methods=['POST'])
def agregar_producto():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        cantidad = data.get('cantidad')

        if not nombre or not isinstance(cantidad, int) or cantidad <= 0:
            return jsonify({"error": "Datos inválidos"}), 400

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, cantidad) VALUES (%s, %s)", (nombre, cantidad))
        conn.commit()
        conn.close()
        return jsonify({"message": "Producto agregado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/producto/<int:id_producto>', methods=['PUT'])
def actualizar_producto(id_producto):
    try:
        data = request.get_json()
        nueva_cantidad = data.get('cantidad')

        if not isinstance(nueva_cantidad, int) or nueva_cantidad < 0:
            return jsonify({"error": "Cantidad inválida"}), 400

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET cantidad = %s WHERE id_producto = %s", (nueva_cantidad, id_producto))
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Producto no encontrado"}), 404
        conn.close()
        return jsonify({"message": "Producto actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
