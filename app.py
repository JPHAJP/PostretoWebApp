from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from weasyprint import HTML
import os, json

app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate)

# Ruta para servir el archivo productos.json
@app.route("/productos")
def productos():
    with open("productos.json", "r") as f:
        productos = json.load(f)
    return jsonify(productos)

# Página de inicio
@app.route("/")
def home():
    return render_template("index.html")  # Nueva plantilla para la página de inicio

@app.route("/editar_productos", methods=["GET", "POST"])
def editar_productos():
    # Cargar los productos desde el archivo JSON
    productos_path = "productos.json"
    with open(productos_path, "r") as f:
        productos = json.load(f)

    if request.method == "POST":
        # Guardar los datos enviados desde el formulario
        productos_actualizados = request.form.get("productos_data")
        try:
            productos_actualizados = json.loads(productos_actualizados)  # Convertir a JSON
            with open(productos_path, "w") as f:
                json.dump(productos_actualizados, f, indent=4)  # Guardar con formato
            return redirect(url_for("editar_productos"))
        except Exception as e:
            return f"Error al guardar los productos: {str(e)}", 400

    return render_template("editar_productos.html", productos=productos)

@app.route("/productos/api", methods=["GET"])
def obtener_productos():
    with open("productos.json", "r") as file:
        productos = json.load(file)
    return jsonify(productos)

# Ruta para guardar los productos
@app.route("/guardar_productos", methods=["POST"])
def guardar_productos():
    try:
        # Obtener los datos enviados desde el cliente
        nuevos_productos = request.json
        
        # Validar los datos básicos (opcional)
        if not isinstance(nuevos_productos, list):
            return jsonify({"error": "Formato de datos inválido. Se esperaba una lista."}), 400
        
        # Guardar los datos en el archivo JSON
        with open("productos.json", "w") as file:
            json.dump(nuevos_productos, file, ensure_ascii=False, indent=4)
        
        return jsonify({"message": "Productos guardados exitosamente."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @app.route("/productos/editar", methods=["GET", "POST"])
def editar_productos():
    print("Ruta /productos/editar activa")
    return "Página de edición activa"


# Ruta para manejar el formulario de recibo
@app.route("/recibo", methods=["GET", "POST"])
def recibo():
    if request.method == "POST":
        cliente = request.form["cliente"]
        num_productos = int(request.form["num_productos"])
        productos = []

        for i in range(num_productos):
            productos.append({
                "nombre": request.form[f"producto_{i}_nombre"],
                "cantidad": int(request.form[f"producto_{i}_cantidad"]),
                "precio_unitario": float(request.form[f"producto_{i}_precio_unitario"]),
                "presentacion": request.form[f"producto_{i}_presentacion"],
            })

        anticipo = float(request.form["anticipo"])
        fecha = request.form["fecha"]
        total = sum(p["cantidad"] * p["precio_unitario"] for p in productos)
        restante = total - anticipo

        # Renderizar el HTML del recibo
        recibo_html = render_template("recibo.html", cliente=cliente, productos=productos, total=total, anticipo=anticipo, restante=restante, fecha=fecha)
        
        # Redirigir a la ruta de descarga del PDF, pasando los datos necesarios
        return download(cliente, fecha, recibo_html)

    return render_template("formulario.html")  # Formulario para capturar datos del recibo

# Ruta para descargar el recibo como PDF
@app.route("/download", methods=["POST"])
def download(cliente, fecha, html_content):
    # Generar el nombre del archivo PDF
    nombre_archivo = f"Recibo entrega - {cliente} - {fecha}.pdf"

    # Generar el PDF a partir del contenido HTML
    pdf = HTML(string=html_content, base_url='https://postretowebapp.onrender.com/').write_pdf()

    # Preparar la respuesta con el PDF
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename={nombre_archivo}"

    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)