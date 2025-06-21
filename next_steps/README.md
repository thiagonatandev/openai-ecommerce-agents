# Fase 2: Banco de Dados SQLite e Lógica de Agentes

## Visão Geral

Esta pasta contém um banco de dados **SQLite** (`ecom_database.db`) que simula a base de dados para uma aplicação de e-commerce. O objetivo desta fase do teste é utilizar este banco de dados para desenvolver a lógica dos agentes de IA apresentados na interface "Agent View".

O uso do SQLite permite uma interação mais realista, onde os dados podem ser consultados e modificados dinamicamente, simulando um ambiente de produção.

O script `database_setup.py` foi usado para criar e popular o banco de dados a partir dos mocks iniciais. Você pode executá-lo para recriar o banco de dados do zero a qualquer momento.

## Estrutura do Banco de Dados

O banco de dados `ecom_database.db` contém as seguintes tabelas:

-   `products`: Contém uma lista de produtos disponíveis na loja.
    -   **Usado por**: `Product FAQ Agent`.
-   `orders`: Armazena os pedidos realizados pelos clientes.
    -   **Usado por**: `Order Status Agent`, `Return Agent`.
-   `order_items`: Tabela de associação que liga produtos a pedidos.
    -   **Usado por**: Vários agentes para detalhar os itens de um pedido.
-   `customers`: Um registro dos clientes da loja.
    -   **Usado por**: Vários agentes para associar interações a um cliente.
-   `discounts`: Lista de cupons de desconto.
    -   **Usado por**: `Discount Agent`.
-   `payments`: Detalhes sobre as transações de pagamento.
    -   **Usado por**: `Payment Agent`.
-   `returns`: Um registro de solicitações de devolução.
    -   **Usado por**: `Return Agent`.

## Próximos Passos (Objetivo do Teste)

O desafio agora é implementar a lógica que permite aos agentes de IA interagirem com o banco de dados SQLite para executar suas funções.

### 1. Conexão e Acesso aos Dados

Você precisará se conectar ao banco de dados em seu código. Em Python, isso é feito de forma simples com a biblioteca `sqlite3`:

```python
import sqlite3
import os

# Caminho para o banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'ecom_database.db')

# Conectar ao banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Exemplo de consulta
cursor.execute("SELECT * FROM products WHERE id = ?", ('prod_123',))
product = cursor.fetchone()
print(product)

# Fechar a conexão
conn.close()
```

### 2. Implementação da Lógica dos Agentes

Para cada agente, implemente a lógica que consulta o banco de dados para obter as informações necessárias.

-   **Exemplo (Order Status Agent)**:
    -   Recebe um `order_number` do contexto da conversa.
    -   Executa uma query no banco de dados para buscar o pedido correspondente na tabela `orders`.
    -   Retorna uma resposta formatada com o status e o código de rastreio.

### 3. Gerenciamento do Contexto da Conversa

Demonstre como o `Conversation Context` seria preenchido e utilizado. O `Triage Agent` identificaria a intenção e as entidades (como `order_number` ou `customer_email`) e as passaria para o agente especialista correspondente.

### 4. Simulação de API de Rastreio com Mockoon

Para tornar o `Order Status Agent` mais realista, o ideal é que ele consulte uma API de rastreio externa em vez de apenas ler um código estático do banco de dados. Mockoon é a ferramenta perfeita para simular essa API.

**Por que Mockoon?**

*   **Rápido e Fácil:** Possui uma interface gráfica que permite configurar rotas e respostas em minutos.
*   **Sem Código:** Você não precisa escrever ou manter um servidor. A aplicação cuida de tudo.
*   **Realismo:** Permite criar respostas dinâmicas, simular latência e diferentes cenários de erro, tornando o mock muito próximo de uma API real.

**Passo a Passo para Configurar:**

1.  **Baixe e Instale o Mockoon:** Acesse o [site oficial do Mockoon](https://mockoon.com/) e baixe a aplicação para o seu sistema operacional.

2.  **Crie a Rota de Rastreio:**
    *   Com o Mockoon aberto, crie uma nova rota.
    *   **Método:** `GET`
    *   **Endpoint:** `/tracking/:tracking_code`. O trecho `:tracking_code` cria um parâmetro dinâmico que podemos usar na resposta.
    *   A URL base da sua API local será algo como `http://localhost:3001`. Portanto, a URL completa para a chamada será `http://localhost:3001/tracking/BR123456789PT`.

3.  **Configure a Resposta da API:**
    *   Na aba **Body**, cole o JSON abaixo. Ele usa a _templating syntax_ do Mockoon para injetar o `tracking_code` da URL diretamente na resposta, tornando-a dinâmica.

    ```json
    {
      "tracking_code": "{{urlParam 'tracking_code'}}",
      "status": "Em Trânsito",
      "carrier": "Mock-Logística",
      "history": [
        {
          "date": "2025-07-24T18:00:00Z",
          "location": "Centro de Distribuição, Curitiba - PR",
          "description": "Objeto em trânsito para a sua cidade"
        },
        {
          "date": "2025-07-23T10:00:00Z",
          "location": "Unidade de Tratamento, São Paulo - SP",
          "description": "Objeto postado"
        }
      ],
      "estimated_delivery": "2025-07-28"
    }
    ```

4.  **Inicie o Servidor:** Clique no botão de "play" verde no topo para iniciar sua API mockada.

**Integração com o Agente:**

Agora, a lógica do `Order Status Agent` deve ser atualizada para, além de buscar o pedido no banco, fazer uma chamada HTTP para a API de rastreio.

-   **Exemplo da nova lógica (Order Status Agent)**:
    1.  Recebe um `order_number`.
    2.  Consulta o banco de dados na tabela `orders` para obter o `tracking_code`.
    3.  Se houver um `tracking_code`, faz uma requisição `GET` para `http://localhost:3001/tracking/{tracking_code}`.
    4.  Formata uma resposta para o usuário combinando as informações do banco com os detalhes da API de rastreio.

-   **Exemplo de chamada em Python:**

```python
import requests

# Código obtido do banco de dados
tracking_code = "BR123456789PT" 
# URL da API mockada no Mockoon
url = f"http://localhost:3001/tracking/{tracking_code}"

try:
    response = requests.get(url)
    response.raise_for_status()  # Lança um erro para status 4xx/5xx
    
    tracking_data = response.json()
    print(tracking_data)
    # Aqui você processaria os dados para o agente...

except requests.exceptions.RequestException as e:
    print(f"Erro ao consultar a API de rastreio: {e}")

```

O objetivo final é criar um protótipo funcional que simule a interação do sistema de agentes com sua base de dados **e com serviços de terceiros** para resolver as solicitações dos clientes. 