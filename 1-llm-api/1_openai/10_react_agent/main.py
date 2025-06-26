import os
import json
import yfinance as yf
from openai import OpenAI
from pprint import pprint
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Function Implementations
def get_stock_price(ticker: str):
    """Get the current price of a stock."""
    ticker_info = yf.Ticker(ticker).info
    current_price = ticker_info.get("currentPrice")
    return {"ticker": ticker, "current_price": current_price}


def get_dividend_date(ticker: str):
    """Get the next dividend payment date of a stock."""
    ticker_info = yf.Ticker(ticker).info
    dividend_date = ticker_info.get("dividendDate")
    return {"ticker": ticker, "dividend_date": dividend_date}

# Define custom tools
tools = [
     {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Use this function to get the current price of a stock.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The ticker symbol for the stock, e.g. GOOG",
                    }
                },
                "required": ["ticker"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_dividend_date",
            "description": "Use this function to get the next dividend payment date of a stock.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The ticker symbol for the stock, e.g. GOOG",
                    }
                },
                "required": ["ticker"],
            },
        }
    },
]

available_functions = {
    "get_stock_price": get_stock_price,
    "get_dividend_date": get_dividend_date,
}


class ReactAgent:
    """A ReAct (Reason and Act) agent that handles multiple tool calls."""
    
    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.max_iterations = 10  # Prevent infinite loops
        
    def run(self, messages: List[Dict[str, Any]]) -> str:
        """
        Run the ReAct loop until we get a final answer.
        
        The agent will:
        1. Call the LLM
        2. If tool calls are returned, execute them
        3. Add results to conversation and repeat
        4. Continue until LLM returns only text (no tool calls)
        """
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # Call the LLM
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                parallel_tool_calls=False
            )
            
            response_message = response.choices[0].message
            print(f"LLM Response: {response_message}")
            
            # Check if there are tool calls
            if response_message.tool_calls:
                # Add the assistant's message with tool calls to history
                messages.append({
                    "role": "assistant",
                    "content": response_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            }
                        }
                        for tc in response_message.tool_calls
                    ]
                })
                
                # Process ALL tool calls (not just the first one)
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    tool_id = tool_call.id
                    
                    print(f"Executing tool: {function_name}({function_args})")
                    
                    # Call the function
                    function_to_call = available_functions[function_name]
                    function_response = function_to_call(**function_args)
                    
                    print(f"Tool result: {function_response}")
                    
                    # Add tool response to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "name": function_name,
                        "content": json.dumps(function_response),
                    })
                
                # Continue the loop to get the next response
                continue
                
            else:
                # No tool calls - we have our final answer
                final_content = response_message.content
                
                # Add the final assistant message to history
                messages.append({
                    "role": "assistant",
                    "content": final_content
                })
                
                print(f"\nFinal answer: {final_content}")
                return final_content
        
        # If we hit max iterations, return an error
        return "Error: Maximum iterations reached without getting a final answer."


def main():
    # Create a ReAct agent
    agent = ReactAgent()
    
    # Example 1: Simple query (single tool call)
    print("=== Example 1: Single Tool Call ===")
    messages1 = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What is the current stock price for MSFT?"},
    ]
    
    result1 = agent.run(messages1.copy())
    print(f"\nResult: {result1}")
    
    # Example 2: Complex query requiring multiple tool calls
    print("\n\n=== Example 2: Multiple Tool Calls ===")
    messages2 = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What are the current prices and dividend dates for both MSFT and AAPL? Please provide a summary."},
    ]
    
    result2 = agent.run(messages2.copy())
    print(f"\nResult: {result2}")
    
    # Example 3: Sequential reasoning
    print("\n\n=== Example 3: Sequential Reasoning ===")
    messages3 = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Compare the stock prices of GOOGL and META. Which one is more expensive?"},
    ]
    
    result3 = agent.run(messages3.copy())
    print(f"\nResult: {result3}")


if __name__ == "__main__":
    main()