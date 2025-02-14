from flask import Flask, request, render_template, jsonify
import re

app = Flask(__name__)

OPERADORES = {
    '¬': lambda x: not x,
    '∧': lambda x, y: x and y,
    '∨': lambda x, y: x or y,
    '→': lambda x, y: (not x) or y,
    '↔': lambda x, y: x == y
}


def avaliar(expressao, valores):
    for letra, valor in valores.items():
        expressao = expressao.replace(letra, str(valor))

    expressao = expressao.replace("¬", " not ")
    expressao = expressao.replace("∧", " and ")
    expressao = expressao.replace("∨", " or ")
    expressao = expressao.replace("→", " <= ")
    expressao = expressao.replace("↔", " == ")

    return eval(expressao)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.json
        expressao = data["expressao"]
        valores = {k: bool(int(v)) for k, v in data["valores"].items()}
        resultado = avaliar(expressao, valores)
        return jsonify({"resultado": resultado})
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
