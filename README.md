This project is 90% based on [OpenAI's project demo](https://github.com/openai/openai-cs-agents-demo)

# OpenAI E-commerce Agents

OpenAI E-commerce Agents is an experimental demo project showcasing an AI-driven customer service platform for e-commerce scenarios. It uses OpenAI’s multi-agent framework to handle common support tasks such as seat changes, cancellations, FAQs, and payment assistance. The system is built on top of the OpenAI Agents SDK and consists of a Python backend that orchestrates specialized agents, and a frontend interface for real-time interaction.

## Overview

This project demonstrates how multiple specialized agents can collaborate to handle customer service tasks efficiently. A “Triage Agent” receives all user queries and delegates them to appropriate specialist agents, such as:

- Order Status Agent
- Return Agent
- Product FAQ Agent
- Discount Agent
- Payment Agent

Each agent is configured with a specific prompt, context, and tools. Guardrails can also be applied to enforce constraints on agent behavior.

## Architecture

- **Backend (Python):** Manages agent definitions, tools, routing logic, and the FastAPI server.
- **Frontend (Next.js/React):** Provides a user-facing chat interface and displays agent interactions and guardrails.
- **Agents SDK:** Handles message loops, agent tool execution, and handoffs between agents.
- **Guardrails:** Ensure the agents stay on-topic and safe using relevance and jailbreak checks.

## Installation

### Prerequisites

- Python 3.13+
- Yarn 1.22+
- OpenAI API key

### 1. Clone the repository

```bash
git clone https://github.com/thiagonatandev/openai-ecommerce-agents.git
cd openai-ecommerce-agents
```

### 2. Set your OpenAI API key

Export your API key as an environment variable:

```bash
export OPENAI_API_KEY=your-api-key-here
```

Or create a `.env` file inside the `python-backend/` directory:

```
OPENAI_API_KEY=your-api-key-here
```

### 3. Install backend dependencies

```bash
cd python-backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Install frontend dependencies

```bash
cd ../ui
yarn
```

## Usage

### 1. Start the backend

```bash
cd python-backend
source .venv/bin/activate
python -m uvicorn api:app --reload --port 8000
```

### 2. Start the frontend

In a new terminal:

```bash
cd ui
yarn dev:next
```

### 3. Open your browser

Visit [http://localhost:3000](http://localhost:3000) to use the interface. You can interact with the agents through the chat interface.


## Development Status

**This project is currently under active development.**  
Interfaces and implementations may change. Contributions and feedback are welcome.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
