import unicodedata
from flask import Flask, render_template, request

app = Flask(__name__)

# Dicionário de valores das letras
valores_letras = {
       'A': 1, 'Á': 1, 'Ã': 1, 'Â': 1, 'Å': 1, 'Ä': 1, 'À': 1, 'B': 2, 'C': 3, 'D': 4,
    'E': 5, 'É': 5, 'È': 5, 'Ê': 5, 'Ë': 5, 'F': 6, 'G': 7, 'H': 8,
    'I': 9, 'Í': 9, 'Ì': 9, 'Î': 9, 'Ï': 9, 'J': 9, 'Y': 9, 'Ÿ': 9,
    'K': 10, 'L': 20, 'M': 30, 'N': 40, 'Ñ': 40, 'O': 50, 'Õ': 50, 'Ó': 50,
    'Ò': 50, 'Ô': 50, 'Ö': 50, 'P': 60, 'Q': 70, 'R': 80, 'S': 90, 'T': 100,
    'U': 200, 'Ú': 200, 'Ù': 200, 'Ü': 200, 'V': 200, 'W': 200, 'X': 300, 'Z': 400
}

# Dicionário de vibrações
vibracoes = {
    1: 'FORTE', 2: 'FORTE', 3: 'FORTE', 4: 'FORTE', 5: 'NEUTRO', 6: 'NEUTRO',
    7: 'NEUTRO', 8: 'NEUTRO', 9: 'VITORIOSO', 11: 'VITORIOSO', 14: 'VITORIOSO', 20: 'VITORIOSO',
    10: 'BOM', 12: 'BOM', 17: 'BOM', 19: 'BOM',
    13: 'PÉSSIMO', 15: 'PÉSSIMO', 16: 'PÉSSIMO', 18: 'PÉSSIMO',
    21: 'PERFEITO', 22: 'PERFEITO AOS AVESSOS'

}

@app.route('/')
def home():
    # Certifique-se de que você tem um arquivo index.html em sua pasta templates
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    nome = request.form['nome']
    nomes = nome.split()  # Divide o nome em partes
    resultados = []
    soma_total = 0
    for nome_individual in nomes:
        nome_sem_acentos = remover_acentos(nome_individual)
        numero = calcular_numero_nome_simples(nome_sem_acentos)
        vibracao = obter_vibracao(numero)
        resultados.append((nome_sem_acentos, numero, vibracao))
        soma_total += numero
    while soma_total > 22:
        soma_total = sum(int(digito) for digito in str(soma_total))
    vibracao_final = obter_vibracao(soma_total)
    return render_template('resultado.html', resultados=resultados, soma_total=soma_total, vibracao_final=vibracao_final)

@app.route('/calcular_nome')
def calcular_nome():
    nome = request.args.get('nome', '')
    if nome:
        nome_sem_acentos = remover_acentos(nome)
        numero = calcular_numero_nome_simples(nome_sem_acentos)
        vibracao = obter_vibracao(numero)
        return f"Nome: {nome}, Número: {numero}, Vibração: {vibracao}"
    else:
        return "Por favor, forneça um nome na query string usando ?nome=SEUNOME"

def remover_acentos(texto):
    texto_normalizado = unicodedata.normalize('NFD', texto)
    return ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn').upper()

def calcular_numero_nome_simples(nome):
    total = sum(valores_letras[letra] for letra in nome if letra in valores_letras)
    while total > 22:
        total = sum(int(digito) for digito in str(total))
    return total

def obter_vibracao(numero):
    return vibracoes.get(numero, "Desconhecido")

if __name__ == '__main__':
    app.run(debug=True)