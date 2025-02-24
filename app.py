from flask import Flask, render_template, request, redirect, jsonify
import json
import os

app = Flask(__name__)

# Arquivo JSON para armazenar as fichas
FICHAS_FILE = 'fichas.json'

# Carregar fichas existentes ou criar uma lista vazia
if os.path.exists(FICHAS_FILE):
    try:
        with open(FICHAS_FILE, 'r') as f:
            fichas = json.load(f)
    except json.decoder.JSONDecodeError:
        # Se o arquivo estiver vazio ou mal formatado, inicializa uma lista vazia
        fichas = []
else:
    fichas = []

# Rota principal para exibir as fichas
@app.route('/')
def index():
    return render_template('index.html', fichas=fichas)

# Rota para adicionar uma nova ficha
@app.route('/adicionar', methods=['POST'])
def adicionar_ficha():
    nova_ficha = {
        'nome': request.form['nome'],
        'classe': request.form['classe'],
        'nivel': request.form['nivel'],
        'atributos': {
            'forca': request.form['forca'],
            'destreza': request.form['destreza'],
            'constituicao': request.form['constituicao'],
            'inteligencia': request.form['inteligencia'],
            'sabedoria': request.form['sabedoria'],
            'carisma': request.form['carisma']
        }
    }
    fichas.append(nova_ficha)
    salvar_fichas()
    return redirect('/')

# Função para salvar as fichas no arquivo JSON
def salvar_fichas():
    with open(FICHAS_FILE, 'w') as f:
        json.dump(fichas, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True)

    if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)