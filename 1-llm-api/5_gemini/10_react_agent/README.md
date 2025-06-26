# Google Gemini ReAct AI Agent

A proper **ReAct (Reason and Act)** agent implementation using Google Gemini that handles multiple function calls in a loop.

## Key Features

- **Google Gemini**: Uses Gemini 2.5 Flash model
- **Multiple Function Calls**: Processes ALL function calls in each response
- **Unique API**: Different conversation format from other providers
- **Function Responses**: Uses specialized FunctionResponse objects

## API Differences from OpenAI

- **Content Format**: Uses `contents` array instead of `messages`
- **Function Calls**: Located in `part.function_call` within content parts
- **Function Responses**: Uses `types.FunctionResponse` objects
- **Configuration**: Tools configured via `GenerateContentConfig`

## Usage

```bash
# Setup environment
uv venv
source .venv/bin/activate
uv sync

# Add GEMINI_API_KEY to .env file
export GEMINI_API_KEY=your_key_here

# Run the agent
python main.py
```

## Examples

Same examples as other versions but adapted for Gemini's unique API format.