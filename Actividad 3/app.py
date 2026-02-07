from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

productos = [
    {"id": 1, "nombre": "Labial", "descripcion": "Labial color rojo", "precio": 150},
    {"id": 2, "nombre": "Base", "descripcion": "Base para maquillaje", "precio": 220}
]

@app.route("/productos", methods=["GET"])
def obtener_productos():
    return jsonify({"success": True, "productos": productos})

@app.route("/productos", methods=["POST"])
def crear_producto():
    data = request.get_json()
    if not data or "nombre" not in data or "descripcion" not in data or "precio" not in data:
        return jsonify({"error": "Faltan datos"}), 400
    if type(data["precio"]) not in [int, float] or data["precio"] < 0:
        return jsonify({"error": "El precio debe ser un número positivo"}), 400
    nuevo_producto = {
        "id": len(productos) + 1,
        "nombre": data["nombre"],
        "descripcion": data["descripcion"],
        "precio": data["precio"]
    }
    productos.append(nuevo_producto)
    return jsonify({"success": True, "producto": nuevo_producto}), 201

@app.route("/productos/<int:id>", methods=["PUT"])
def actualizar_producto(id):
    data = request.get_json()
    for producto in productos:
        if producto["id"] == id:
            producto["nombre"] = data.get("nombre", producto["nombre"])
            producto["descripcion"] = data.get("descripcion", producto["descripcion"])
            producto["precio"] = data.get("precio", producto["precio"])
            return jsonify({"success": True, "producto": producto})
    return jsonify({"error": "Producto no encontrado"}), 404

@app.route("/productos/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    for producto in productos:
        if producto["id"] == id:
            productos.remove(producto)
            return jsonify({"success": True, "mensaje": "Producto eliminado correctamente"})
    return jsonify({"error": "Producto no encontrado"}), 404

@app.errorhandler(404)
def ruta_no_encontrada(error):
    return jsonify({"error": "Ruta no encontrada"}), 404

@app.errorhandler(Exception)
def error_general(error):
    return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run(debug=True)
