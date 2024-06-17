# import the libraries
from openai import OpenAI
import re
import os

# create an instance of the OpenAI class

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# system prompts
messages = [
     {
          "role": "system",
          "content": "You are a very experienced Chinese chef who are good at making fried dishes. You are humble, patient, and not talkative.",
     }
]

# additional system prompts
messages.append(
     {
          "role": "system",
          "content": "Your client is going to ask for suggesting dishes based on ingredients or ask for giving recipes to dishes or ask for criticizing the recipes given by what the client provides. If what the client asks for doesn't belong to any of the three categories, deny the request and ask the client to try again. If the client passes one or more ingredients, you should suggest a dish name that can be made with these ingredients by only suggesting the dish name not the receipt. If the client provides a dish name, you should give a receipt for that dish. If the client provides a receipt for a dish, you should criticize the receipt and suggest changes."
     }
)

# ask the user for input
dish = input("Please provide a dish name or ingredient(s) for dishes or a receipt for a dish:\n")

# add the user input to the messages
messages.append(
    {
        "role": "user",
        "content": dish
    }
)

# model to use
model = "gpt-3.5-turbo"

# create the completion
stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True,
)

# get the response
collected_messages = []
for chunk in stream:
    chunk_message = chunk.choices[0].delta.content or ""
    print(chunk_message, end="")
    collected_messages.append(chunk_message)

# add the response to the messages
messages.append(
    {
        "role": "system",
        "content": "".join(collected_messages)
    }
)