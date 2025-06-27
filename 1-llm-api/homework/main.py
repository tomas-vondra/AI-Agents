import os
import yfinance as yf
import json

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    # Use your OpenAI API key from environment variables
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Define a function to get the current exchange rate for a currency pair
def get_currency_exchange_rate(pair: str):
    # Define ticker symbol for the currency pair (=X means exchange rate)
    ticker = pair + "=X"
    # Get the data using yfinance
    data = yf.Ticker(ticker)

    # Fetch the historical data for the currency pair
    hist = data.history(period="1d")
    # Throw exception if no data is found
    if hist.empty or 'Close' not in hist or hist['Close'].empty:
        raise ValueError(f"No data found for currency pair: {pair}")

    # Get the most recent closing price, which represents the conversion rate
    conversion_rate = hist['Close'].iloc[-1]

    return conversion_rate

# custom tools for the LLM to call
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_currency_exchange_rate",
            "description": "Use this function to get the current exchange price between pair.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pair": {
                        "type": "string",
                        "description": "The pair of currencies to convert, e.g. EURUSD for Euro to US Dollar",
                    }
                },
                "required": ["pair"],
            },
        }
    }
]

# Map function names to actual function implementations
available_functions = {
    "get_currency_exchange_rate": get_currency_exchange_rate
}

def main():

    # Define the first prompt.
    # role: system is used to set the behavior of the assistant.
    # role: user is used to provide input to the assistant.
    # role: assistant is used to provide output from the assistant.
    # role: tool is used to provide input to the assistant in a way that is not visible to the user.
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What is the exchange rate between EUR and CZK?"},
    ]

    print("Prompt: What is the exchange rate between EUR and CZK?")

    # Call the LLM
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        parallel_tool_calls=False
    )

    print("LLM response:" + str(response))


    # Extract the response message
    # The response can contain multiple choices (results) if we use n parameter, but default is 1.
    response_message = response.choices[0].message

    # Check if the response contains tool calls
    if response_message.tool_calls:
        # Add the assistant's message with tool calls to history
        # We are iterating through the tool calls and executing them one by one. But in this case we only expect one tool call.
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

        # Process ALL tool calls (but in this case we only expect one tool call)
        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            # Parse the arguments from the tool call to a dictionary, so we can pass them to the function via **kwargs
            tool_args = json.loads(tool_call.function.arguments)
            tool_id = tool_call.id

            # Check if the tool has a corresponding function
            function_to_call = available_functions.get(tool_name)
            if function_to_call is None:
                raise KeyError(f"No function mapped for tool name '{tool_name}'")

            print(f"Executing tool: {tool_name}({tool_args})")

            # Takes the dictionary of arguments and unpacks it to keyword arguments
            # f tool_args = {"pair": "CZKEUR"}, then function_to_call(**tool_args) is equivalent to calling function_to_call(pair="CZKEUR").
            function_response = function_to_call(**tool_args)

            print(f"Tool result: {function_response}")

            # Add tool response to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_id,
                "name": tool_name,
                "content": json.dumps(function_response)
            })

            # Call the LLM again with the updated messages including the tool response
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                parallel_tool_calls=False
            )

    # Print the response after the tool calls
    response_message = response.choices[0].message
    print("LLM response after tool calls:" + str(response_message))

    # Extract the content of the response message
    content = response_message.content


    # Append the final response to the messages
    messages.append({
        "role": "assistant",
        "content": content
    })

    # Print the final content
    print("--- Full response: ---")
    print(content)



if __name__ == "__main__":
    main()

