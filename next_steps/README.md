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

O objetivo final é criar um protótipo funcional que simule a interação do sistema de agentes com sua base de dados para resolver as solicitações dos clientes. 