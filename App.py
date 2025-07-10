from flask import Flask, render_template, request, url_for
import pandas as pd
import os
import mysql.connector


app = Flask(__name__)

def inventario(archivo_excel, nombre_equipo):
    try:
        df = pd.read_excel(archivo_excel)
        softwares = df[df['Equipo'] == nombre_equipo]['Software instakados'].tolist()

        if not softwares:
            return f"El equipo cuenta con software básico"
            
        else:
            softwares_unicos = sorted(list(set(softwares)))
            if len(softwares_unicos) == 1:
                return f"El equipo cuenta con software básico y a parte con {softwares_unicos[0]}"
                
            else:
                lista_softwares = ", ".join(softwares_unicos[:-1]) + " y " + softwares_unicos[-1]
                return f"El equipo cuenta con software básico y a parte con {lista_softwares}"
            
    except FileNotFoundError:
        return "Error: Archivo Excel no encontrado"
    except Exception as e:
        return f"Error ine8sperado: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        equipo = request.form.get("equipo", "").strip()
        if equipo:
            excel_path = os.path.join(os.path.dirname(__file__), "inventario.xlsx")
            resultado = inventario(excel_path, equipo)
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)