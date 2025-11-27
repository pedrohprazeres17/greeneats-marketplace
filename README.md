# 🌱 GreenEats Marketplace

Marketplace de Comida Saudável - Plataforma para agricultores cadastrarem e gerenciarem produtos frescos (frutas, legumes e verduras).

## 📋 Sobre o Projeto

Este projeto foi desenvolvido como parte de uma avaliação acadêmica e implementa um sistema completo de marketplace com:
- **Backend**: API REST em Python/Flask
- **Banco de Dados**: Airtable (via API REST)
- **Frontend**: Interface moderna com HTML5, CSS3 e JavaScript Vanilla

## 🚀 Stack Tecnológica

- **Backend**: Python 3.x + Flask
- **Database**: Airtable
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Bibliotecas**: Flask, Requests, Flask-CORS

## 📁 Estrutura do Projeto

```
greeneats-marketplace/
├── app.py                      # Backend Flask com API REST
├── config_local.py             # Credenciais locais (NÃO versionado)
├── config_local.py.example     # Template de configuração
├── requirements.txt            # Dependências Python
├── .gitignore                  # Arquivos ignorados pelo Git
├── templates/
│   └── index.html             # Frontend (Painel do Agricultor)
├── agile_docs.md              # Documentação Ágil (User Stories + Kanban)
└── README.md                  # Este arquivo
```

## 🔧 Instalação

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Instalar Dependências

**Opção 1 (Recomendada):** Usar requirements.txt
```bash
pip install -r requirements.txt
```

**Opção 2:** Instalar manualmente
```bash
pip install flask requests flask-cors
```

### Passo 2: Configuração do Airtable

**IMPORTANTE**: As credenciais da API não estão no código por segurança.

**Para configurar localmente:**

1. Copie o arquivo de exemplo:
   ```bash
   copy config_local.py.example config_local.py
   ```

2. Edite `config_local.py` e adicione seu token:
   ```python
   AIRTABLE_API_TOKEN_LOCAL = "seu_token_aqui"
   ```

**Credenciais do projeto:**
- BASE_ID: `appCLOkNeG69OCs6H`
- TABELA: `Produtos`
- API_TOKEN: Configure no arquivo `config_local.py` (não versionado)

**Estrutura da Tabela no Airtable:**
A tabela "Produtos" deve ter as seguintes colunas:
- `titulo` (Single line text)
- `descricao` (Long text)
- `preco` (Number)
- `categoria` (Single select: Fruta, Legume, Verdura)
- `imagem_url` (URL)

## ▶️ Como Executar

1. Navegue até o diretório do projeto:
```bash
cd c:\Users\User\Desktop\P2
```

2. Execute o servidor Flask:
```bash
python app.py
```

3. Acesse no navegador:
```
http://localhost:5000
```

Você verá a mensagem no terminal:
```
🌱 GreenEats Marketplace - Servidor iniciado!
📍 Acesse: http://localhost:5000
==================================================
```

## 📡 Endpoints da API

### 1. Renderizar Frontend
- **GET** `/`
- Renderiza a página principal (index.html)

### 2. Validar Produto (Parte 2)
- **POST** `/validar-produto`
- **Body (JSON)**:
```json
{
  "titulo": "Maçã Orgânica",
  "preco": 5.50,
  "categoria": "Fruta"
}
```
- **Response**:
```json
{
  "valido": true,
  "erros": []
}
```

**Regras de Validação:**
- Título: mínimo 5 caracteres
- Preço: maior que 0
- Categoria: deve ser "Fruta", "Legume" ou "Verdura"

### 3. Listar Produtos (Parte 3)
- **GET** `/produtos`
- **Response**:
```json
[
  {
    "id": "recXXXXXXXXXXXXXX",
    "titulo": "Maçã Orgânica",
    "descricao": "Maçã fresca e orgânica",
    "preco": 5.50,
    "categoria": "Fruta",
    "imagem_url": "https://exemplo.com/maca.jpg"
  }
]
```

### 4. Criar Produto (Parte 3)
- **POST** `/produtos`
- **Body (JSON)**:
```json
{
  "titulo": "Cenoura Orgânica",
  "descricao": "Cenoura fresca da fazenda",
  "preco": 3.50,
  "categoria": "Legume",
  "imagem_url": "https://exemplo.com/cenoura.jpg"
}
```
- **Response (Sucesso)**:
```json
{
  "sucesso": true,
  "mensagem": "Produto cadastrado com sucesso!",
  "produto": { ... }
}
```
- **Response (Erro de Validação)**:
```json
{
  "sucesso": false,
  "erros": ["O título deve ter no mínimo 5 caracteres"]
}
```

### 5. Deletar Produto (Parte 3)
- **DELETE** `/produtos/<id>`
- **Response**:
```json
{
  "sucesso": true,
  "mensagem": "Produto excluído com sucesso!"
}
```

## 🎨 Funcionalidades do Frontend

### Painel do Agricultor
- ✅ Formulário de cadastro de produtos
- ✅ Validação em tempo real com feedback visual
- ✅ Listagem dinâmica de produtos
- ✅ Exclusão de produtos
- ✅ Design moderno e responsivo
- ✅ Animações suaves
- ✅ Tema escuro com gradientes verdes

### Campos do Formulário
1. **Título** (obrigatório) - mínimo 5 caracteres
2. **Descrição** (opcional)
3. **Preço** (obrigatório) - deve ser maior que 0
4. **Categoria** (obrigatório) - Fruta, Legume ou Verdura
5. **URL da Imagem** (opcional)

## 📚 Documentação Ágil

Consulte o arquivo `agile_docs.md` para:
- **User Stories**: 3 histórias de usuário focadas no cadastro de produtos
- **Estrutura Kanban**: Colunas sugeridas para gestão no Trello

## 🧪 Testando a Aplicação

### Teste 1: Cadastro Válido
1. Acesse http://localhost:5000
2. Preencha o formulário:
   - Título: "Banana Prata"
   - Descrição: "Banana fresca e doce"
   - Preço: 4.50
   - Categoria: Fruta
   - URL Imagem: (opcional)
3. Clique em "Cadastrar Produto"
4. Verifique se aparece mensagem de sucesso
5. Produto deve aparecer na lista à direita

### Teste 2: Validação de Erros
1. Tente cadastrar com título "Uva" (menos de 5 caracteres)
2. Sistema deve exibir erro: "O título deve ter no mínimo 5 caracteres"
3. Tente cadastrar com preço 0 ou negativo
4. Sistema deve exibir erro: "O preço deve ser maior que zero"
5. Tente cadastrar com categoria inválida
6. Sistema deve exibir erro sobre categoria

### Teste 3: Exclusão
1. Clique no botão "Excluir" de um produto
2. Confirme a exclusão
3. Produto deve ser removido da lista

## 🔒 Segurança

⚠️ **IMPORTANTE**: Este projeto é para fins acadêmicos. Em produção:
- Nunca exponha tokens de API no código
- Use variáveis de ambiente (.env)
- Implemente autenticação e autorização
- Adicione rate limiting
- Valide dados no backend E frontend

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flask'"
**Solução**: Execute `pip install flask requests flask-cors`

### Erro: "Connection refused" ao acessar localhost:5000
**Solução**: Verifique se o servidor Flask está rodando (`python app.py`)

### Produtos não aparecem na listagem
**Solução**: 
1. Verifique se as credenciais do Airtable estão corretas
2. Confirme que a tabela "Produtos" existe no Airtable
3. Verifique se as colunas estão nomeadas corretamente

### Erro 401 (Unauthorized) do Airtable
**Solução**: Verifique se o API_TOKEN está válido e correto

## 👨‍💻 Autor

Desenvolvido como avaliação acadêmica do projeto "Marketplace de Comida Saudável - GreenEats"

## 📄 Licença

Este projeto é para fins educacionais.
