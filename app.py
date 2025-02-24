from flask import Flask, render_template, request, redirect, jsonify
import json
import os
import random

app = Flask(__name__)

# Arquivo JSON para armazenar as fichas
FICHAS_FILE = 'fichas.json'

# Carregar fichas existentes ou criar uma lista vazia
if os.path.exists(FICHAS_FILE):
    try:
        with open(FICHAS_FILE, 'r') as f:
            fichas = json.load(f)
    except json.decoder.JSONDecodeError:
        fichas = []
else:
    fichas = []

# Rota para a página inicial
@app.route('/')
def inicio():
    return render_template('inicio.html')

# Rota para a página de criação de ficha
@app.route('/criar-ficha')
def criar_ficha():
    return render_template('criar_ficha.html')

# Rota para a página de fichas salvas
@app.route('/fichas-salvas')
def fichas_salvas():
    return render_template('fichas_salvas.html', fichas=fichas)

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
    return redirect('/fichas-salvas')

# Rota para excluir uma ficha
@app.route('/excluir/<int:indice>', methods=['POST'])
def excluir_ficha(indice):
    if 0 <= indice < len(fichas):
        fichas.pop(indice)
        salvar_fichas()
    return redirect('/fichas-salvas')

# Rota para editar uma ficha
@app.route('/editar/<int:indice>', methods=['GET', 'POST'])
def editar_ficha(indice):
    if request.method == 'POST':
        fichas[indice] = {
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
        salvar_fichas()
        return redirect('/fichas-salvas')
    else:
        ficha = fichas[indice]
        return render_template('editar.html', ficha=ficha, indice=indice)

# Função para salvar as fichas no arquivo JSON
def salvar_fichas():
    with open(FICHAS_FILE, 'w') as f:
        json.dump(fichas, f, indent=4)

# Função para rolar dados
def rolar_dados(quantidade, faces):
    resultados = [random.randint(1, faces) for _ in range(quantidade)]
    return resultados

# Rota para rolar dados
@app.route('/rolar/<int:quantidade>d<int:faces>')
def rolar(quantidade, faces):
    resultados = rolar_dados(quantidade, faces)
    return jsonify({
        'quantidade': quantidade,
        'faces': faces,
        'resultados': resultados,
        'total': sum(resultados)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)