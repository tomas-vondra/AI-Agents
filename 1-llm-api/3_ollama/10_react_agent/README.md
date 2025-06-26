# Ollama ReAct AI Agent

A proper **ReAct (Reason and Act)** agent implementation using Ollama local models that handles multiple tool calls in a loop.

## Key Features

- **Local Models**: Uses Ollama for running models locally
- **Multiple Tool Calls**: Processes ALL tool calls in each response
- **Mixed Tool Format**: Supports both function references and schema objects
- **No API Keys**: Runs completely locally

## API Differences from OpenAI

- **Tool Format**: Mixed format - direct function references and schema objects
- **Response**: Uses `ChatResponse` object with `message` attribute
- **No API Key**: Requires local Ollama installation
- **Tool Results**: Simple `role: "tool"` messages

## Prerequisites

```bash
# Install and run Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2
```

## Usage

```bash
# Setup environment
uv venv
source .venv/bin/activate
uv sync

# Run the agent
python main.py
```

## Examples

Same examples as OpenAI version but using Ollama's local models.