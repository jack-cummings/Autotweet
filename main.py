import pandas
import openai
import requests
import urllib.parse
import os


inputs = {'size': 'small',
          'size_desc': 'family owned',
          'industry': 'HVAC',
          'loc_city': 'Chapel Hill',
          'loc_state': 'NC',
          'name': 'Stone Services',
          'mode': 'single tweet',
          'wc1': 'topical',
          'wc2': 'funny'} # local

openai.api_key = os.environ["openai"]

def get_tweet(inputs):
    # generate prompt
    prompt = f"You are a social media manager for a {inputs['size']}, {inputs['size_desc']}, {inputs['industry']}" \
             f" company based in {inputs['loc_city']}, {inputs['loc_state']} called {inputs['name']}." \
             f" Write a {inputs['mode']} that are {inputs['wc1']} and {inputs['wc2']} to be sent as part of a social-media" \
             f" marketing campaign "  # randomly append website link

    # print(f"prompt 0: {prompt.split('.')[0]}")
    # print(f"prompt 1: {prompt.split('.')[1]}")

    # get tweet content
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt.split('.')[0]},
            {"role": "user", "content": prompt.split('.')[1]},
        ]
    )

    text = resp.choices[0].message['content']
    print(f"text: {text}")

    # encode prompt
    text_safe = urllib.parse.quote(text)
    intent = f'https://twitter.com/intent/tweet?text={text_safe}'
    print(intent)
    #return

get_tweet(inputs)