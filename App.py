from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

def get_db_connection():
    
    try:
        return pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='bd_tigo'
        )
    except pymysql.MySQLError as e:
        raise Exception(f"Database connection failed: {str(e)}")

def fetch_datos_guardados():
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT Nombre_Software, Maquina FROM asignadas")
            resultados = cursor.fetchall()
        return [{'Nombre_Software': row[0], 'Maquina': row[1]} for row in resultados]
    except pymysql.MySQLError as e:
        raise Exception(f"Database query failed: {str(e)}")
    finally:
        conn.close()

def inventario(datos_guardados, nombre_equipo):
    
    try:
        softwares = [item['Nombre_Software'] for item in datos_guardados if item['Maquina'] == nombre_equipo]

        if not softwares:
            return "El equipo cuenta con software básico"
        softwares_unicos = sorted(list(set(softwares)))
        if len(softwares_unicos) == 1:
            return f"El equipo cuenta con software básico y a parte con {softwares_unicos[0]}"
        lista_softwares = ", ".join(softwares_unicos[:-1]) + " y " + softwares_unicos[-1]
        return f"El equipo cuenta con software básico y a parte con {lista_softwares}"
    
    except Exception as e:
        return f"Error inesperado: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        equipo = request.form.get("equipo", "").strip()
        if equipo:
            try:
                datos_guardados = fetch_datos_guardados()
                resultado = inventario(datos_guardados, equipo)
            except Exception as e:
                resultado = f"Error: {str(e)}"
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)