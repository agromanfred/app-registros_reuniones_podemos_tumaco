from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import config

from flask import send_file
import pandas as pd
import io

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

# 🔹 Modelo
class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120))
    cedula = db.Column(db.String(20), unique=True)
    telefono = db.Column(db.String(20))
    barrio = db.Column(db.String(100))

    ocupacion = db.Column(db.String(200), nullable=True)

    

# 🔹 Crear tablas

with app.app_context():
    db.create_all()

# 🔹 Ruta raíz
@app.route('/')
def home():
    return "API funcionando"

# 🔹 Ruta formulario
@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

# 🔹 Guardar datos
@app.route('/registro', methods=['POST'])
def crear_registro():
    data = request.json

    nuevo = Registro(
        nombre=data['nombre'],
        cedula=data['cedula'],
        telefono=data.get('telefono'),
        barrio=data.get('barrio'),
        ocupacion=data.get('ocupacion')
    )

    db.session.add(nuevo)
    db.session.commit()

    return jsonify({'mensaje': 'Registro guardado'})



# 🔹 Ver registros
@app.route('/registros')
def ver_registros():
    datos = Registro.query.all()
    return jsonify([{
        "nombre": r.nombre,
        "cedula": r.cedula,
        "telefono": r.telefono,
        "barrio": r.barrio,
        "ocupacion": r.ocupacion

    } for r in datos])

import pandas as pd
from flask import request, jsonify

@app.route('/subir_excel', methods=['POST'])

def subir_excel():

    try:

        archivo = request.files['archivo']

        df = pd.read_excel(archivo)

        df.columns = df.columns.str.strip().str.lower()

        insertados = 0
        actualizados = 0
        duplicados = 0
        errores = 0

        for _, row in df.iterrows():

            try:
                nombre = str(row['nombre']).strip()
                cedula = str(row['cedula']).strip()
                telefono = str(row['telefono']).strip()
                barrio = str(row['barrio']).strip()
        

                ocupacion = ""

                if 'ocupacion' in df.columns:
                    ocupacion = str(row['ocupacion']).strip()

                # Buscar por cédula
                existente = Registro.query.filter_by(cedula=cedula).first()

                if existente:

                    cambios = False

                    if existente.nombre != nombre:
                        existente.nombre = nombre
                        cambios = True

                    if existente.telefono != telefono:
                        existente.telefono = telefono
                        cambios = True

                    if existente.barrio != barrio:
                        existente.barrio = barrio
                        cambios = True

                    if existente.ocupacion != ocupacion:
                        existente.ocupacion = ocupacion
                        cambios = True

                    if cambios:
                        db.session.commit()
                        actualizados += 1
                    else:
                        duplicados += 1

                else:

                    nuevo = Registro(
                        nombre=nombre,
                        cedula=cedula,
                        telefono=telefono,
                        barrio=barrio,
                        ocupacion=ocupacion
                    )

                    db.session.add(nuevo)
                    db.session.commit()

                    insertados += 1

            except Exception as e:
                db.session.rollback()
                errores += 1

        return jsonify({
            "insertados": insertados,
            "actualizados": actualizados,
            "duplicados": duplicados,
            "errores": errores
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
    
@app.route('/exportar_excel', methods=['GET'])
def exportar_excel():
    try:
        # Obtener datos desde la BD
        registros = Registro.query.all()

        # Convertir a lista de diccionarios
        data = []
        for r in registros:
            data.append({
                "nombre": r.nombre,
                "cedula": r.cedula,
                "telefono": r.telefono,
                "barrio": r.barrio,
                "ocupacion": r.ocupacion    
            })

        # Crear DataFrame
        df = pd.DataFrame(data)

        # Crear archivo en memoria
        output = io.BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)

        # Enviar archivo
        return send_file(
            output,
            download_name="registros.xlsx",
            as_attachment=True
        )

    except Exception as e:
        return {"error": str(e)}, 500
    
# 🔻 SIEMPRE AL FINAL
if __name__ == '__main__':
    app.run(debug=True)