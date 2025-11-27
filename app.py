from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Credenciais do Airtable
# IMPORTANTE: Para uso em produção, configure as variáveis de ambiente
# Para desenvolvimento local, edite o arquivo config_local.py (não versionado)
BASE_ID = os.getenv("AIRTABLE_BASE_ID", "appCLOkNeG69OCs6H")
API_TOKEN = os.getenv("AIRTABLE_API_TOKEN", "")  # Configure via variável de ambiente ou config_local.py
NOME_TABELA = os.getenv("AIRTABLE_TABLE_NAME", "Produtos")

# Tentar carregar configuração local (se existir)
try:
    from config_local import AIRTABLE_API_TOKEN_LOCAL
    if not API_TOKEN:
        API_TOKEN = AIRTABLE_API_TOKEN_LOCAL
except ImportError:
    pass

if not API_TOKEN:
    print("⚠️  AVISO: AIRTABLE_API_TOKEN não configurado!")
    print("Crie um arquivo 'config_local.py' com: AIRTABLE_API_TOKEN_LOCAL = 'seu_token'")

# URL base da API do Airtable
AIRTABLE_URL = f"https://api.airtable.com/v0/{BASE_ID}/{NOME_TABELA}"

# Headers para autenticação
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Categorias válidas
CATEGORIAS_VALIDAS = ['Fruta', 'Legume', 'Verdura']


def validar_produto(dados):
    """
    Função de validação de produto conforme requisitos da Parte 2.
    
    Regras:
    - Preço deve ser maior que 0
    - Título deve ter no mínimo 5 caracteres
    - Categoria deve ser uma das opções válidas: Fruta, Legume, Verdura
    
    Args:
        dados (dict): Dicionário com os dados do produto
        
    Returns:
        dict: {"valido": bool, "erros": list}
    """
    erros = []
    
    # Validar título
    titulo = dados.get('titulo', '').strip()
    if len(titulo) < 5:
        erros.append("O título deve ter no mínimo 5 caracteres")
    
    # Validar preço
    try:
        preco = float(dados.get('preco', 0))
        if preco <= 0:
            erros.append("O preço deve ser maior que zero")
    except (ValueError, TypeError):
        erros.append("O preço deve ser um número válido")
    
    # Validar categoria
    categoria = dados.get('categoria', '').strip()
    if categoria not in CATEGORIAS_VALIDAS:
        erros.append(f"A categoria deve ser uma das seguintes: {', '.join(CATEGORIAS_VALIDAS)}")
    
    return {
        "valido": len(erros) == 0,
        "erros": erros
    }


@app.route('/')
def index():
    """Renderiza a página principal do frontend"""
    return render_template('index.html')


@app.route('/validar-produto', methods=['POST'])
def validar_produto_endpoint():
    """
    PARTE 2: Endpoint de validação de produto
    
    Recebe dados do produto e retorna se é válido ou não,
    junto com a lista de erros de validação.
    
    Returns:
        JSON: {"valido": bool, "erros": list}
    """
    dados = request.get_json()
    resultado = validar_produto(dados)
    return jsonify(resultado)


@app.route('/produtos', methods=['GET'])
def listar_produtos():
    """
    PARTE 3: Endpoint para listar todos os produtos do Airtable
    
    Returns:
        JSON: Lista de produtos
    """
    try:
        response = requests.get(AIRTABLE_URL, headers=HEADERS)
        response.raise_for_status()
        
        dados = response.json()
        produtos = []
        
        # Formatar os dados para o frontend
        for record in dados.get('records', []):
            produto = {
                'id': record['id'],
                'titulo': record['fields'].get('titulo', ''),
                'descricao': record['fields'].get('descricao', ''),
                'preco': record['fields'].get('preco', 0),
                'categoria': record['fields'].get('categoria', ''),
                'imagem_url': record['fields'].get('imagem_url', '')
            }
            produtos.append(produto)
        
        return jsonify(produtos)
    
    except requests.exceptions.RequestException as e:
        return jsonify({"erro": f"Erro ao buscar produtos: {str(e)}"}), 500


@app.route('/produtos', methods=['POST'])
def criar_produto():
    """
    PARTE 3: Endpoint para criar um novo produto
    
    Valida os dados antes de salvar no Airtable.
    
    Returns:
        JSON: Produto criado ou erros de validação
    """
    dados = request.get_json()
    
    # Validar produto antes de salvar
    validacao = validar_produto(dados)
    
    if not validacao['valido']:
        return jsonify({
            "sucesso": False,
            "erros": validacao['erros']
        }), 400
    
    # Preparar dados para o Airtable
    airtable_data = {
        "fields": {
            "titulo": dados.get('titulo', '').strip(),
            "descricao": dados.get('descricao', '').strip(),
            "preco": float(dados.get('preco', 0)),
            "categoria": dados.get('categoria', '').strip(),
            "imagem_url": dados.get('imagem_url', '').strip()
        }
    }
    
    try:
        response = requests.post(AIRTABLE_URL, headers=HEADERS, json=airtable_data)
        response.raise_for_status()
        
        produto_criado = response.json()
        
        return jsonify({
            "sucesso": True,
            "mensagem": "Produto cadastrado com sucesso!",
            "produto": {
                'id': produto_criado['id'],
                'titulo': produto_criado['fields'].get('titulo', ''),
                'descricao': produto_criado['fields'].get('descricao', ''),
                'preco': produto_criado['fields'].get('preco', 0),
                'categoria': produto_criado['fields'].get('categoria', ''),
                'imagem_url': produto_criado['fields'].get('imagem_url', '')
            }
        }), 201
    
    except requests.exceptions.RequestException as e:
        return jsonify({
            "sucesso": False,
            "erros": [f"Erro ao salvar produto: {str(e)}"]
        }), 500


@app.route('/produtos/<string:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    """
    PARTE 3: Endpoint para deletar um produto
    
    Args:
        produto_id (str): ID do produto no Airtable
        
    Returns:
        JSON: Confirmação de exclusão
    """
    try:
        url = f"{AIRTABLE_URL}/{produto_id}"
        response = requests.delete(url, headers=HEADERS)
        response.raise_for_status()
        
        return jsonify({
            "sucesso": True,
            "mensagem": "Produto excluído com sucesso!"
        }), 200
    
    except requests.exceptions.RequestException as e:
        return jsonify({
            "sucesso": False,
            "erro": f"Erro ao excluir produto: {str(e)}"
        }), 500


if __name__ == '__main__':
    print("🌱 GreenEats Marketplace - Servidor iniciado!")
    print("📍 Acesse: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)