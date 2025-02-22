from flask import Flask, render_template, request, Response, jsonify, redirect, url_for, send_file
import database as dbase 
from database import fs
from bson import ObjectId
from product import Product
import io  

db = dbase.dbConnection()

app  = Flask(__name__)

#CODIGO PARA SUBIR UNA IMAGEN POR ID 
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No se envió ninguna imagen"}), 400
    
    image = request.files['image']
    content_type = image.content_type  # Obtener el tipo MIME

    if not content_type:
        return jsonify({"error": "No se pudo determinar el tipo de archivo"}), 400

    image_id = fs.put(image, filename=image.filename, content_type=content_type)  # Guardar en GridFS con tipo MIME

    return jsonify({"message": "Imagen subida con éxito", "image_id": str(image_id)}), 201

# Ruta para obtener una imagen por ID
@app.route('/image/<image_id>', methods=['GET'])
def get_image(image_id):
    try:
        print("Buscando imagen con ID:", image_id)  # Depuración
        obj_id = ObjectId(image_id)
        print("Convertido a ObjectId:", obj_id)  # Depuración

        image = fs.get(obj_id)  # Obtener la imagen desde GridFS
        print("Imagen encontrada:", image.filename)  # Depuración

        return send_file(io.BytesIO(image.read()), mimetype=image.content_type)  
    except Exception as e:
        print("Error al obtener imagen:", e)  # Depuración
        return jsonify({"error": "Imagen no encontrada"}), 404

@app.route('/debug-images')
def debug_images():
    image_list = []
    for img in fs.find():
        image_list.append({
            "id": str(img._id),
            "filename": img.filename,
            "content_type": img.content_type
        })
    
    return jsonify(image_list)

@app.route('/gallery')
def gallery():
    images = fs.find()  # Obtener todas las imágenes de GridFS
    image_list = [{"id": str(img._id), "filename": img.filename} for img in images]

    return render_template('gallery.html', images=image_list)

