from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import config

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
        barrio=data.get('barrio')
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
        "barrio": r.barrio
    } for r in datos])

import pandas as pd
from flask import request, jsonify

@app.route('/subir_excel', methods=['POST'])
def subir_excel():
    try:
        archivo = request.files['archivo']
        df = pd.read_excel(archivo)

        # Normalizar columnas
        df.columns = df.columns.str.strip().str.lower()

        insertados = 0
        duplicados = 0
        errores = 0

        for _, fila in df.iterrows():
            try:
                nombre = fila.get('nombre')
                cedula = fila.get('cedula')

                if pd.isna(nombre) or pd.isna(cedula):
                    errores += 1
                    continue

                cedula = str(cedula).strip()

                # Verificar duplicado
                existe = Registro.query.filter_by(cedula=cedula).first()
                if existe:
                    duplicados += 1
                    continue

                nuevo = Registro(
                    nombre=str(nombre).strip(),
                    cedula=cedula,
                    telefono=str(fila.get('telefono', '')).strip(),
                    barrio=str(fila.get('barrio', '')).strip()
                )

                db.session.add(nuevo)
                db.session.commit()  # 🔥 commit por fila

                insertados += 1

            except Exception as e:
                db.session.rollback()  # 🔥 CLAVE
                errores += 1

        return jsonify({
            'insertados': insertados,
            'duplicados': duplicados,
            'errores': errores
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# 🔻 SIEMPRE AL FINAL
if __name__ == '__main__':
    app.run(debug=True)