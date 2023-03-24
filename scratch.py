# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
import os

openai.api_key = os.environ["openai"]

resp = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": prompt.split('.')[0]},
        {"role": "user", "content": prompt.split('.')[1]},
        # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        # {"role": "user", "content": "Where was it played?"}
    ]
)

print(resp.choices[0].message['content'])

openai.api_key = os.environ["openai"]

