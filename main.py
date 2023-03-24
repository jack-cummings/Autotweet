from fastapi import FastAPI, Request, BackgroundTasks, Response, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
import uvicorn
import jinja2
import json
import requests
import urllib.parse
import os
import re
import openai
import pandas as pd
import smtplib
from email.message import EmailMessage


'''Core Functions'''
def get_prompt(inputs):
    # generate prompt
    prompt = f"You are a social media manager for a {inputs['size']}, {inputs['industry']}" \
             f" company based in {inputs['loc_city']}, {inputs['loc_state']} called {inputs['name']}." \
             f" Write a tweet that is topical and {inputs['wc']} to be sent as part of a social-media" \
             f" marketing campaign "  # randomly append website link
    return prompt


def get_tweet(prompt):
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
    return text, intent



''' APP Starts '''
# Launch app and mount assets
app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")
# init DB
con = sqlite3.connect("temp.db")
df = pd.read_csv('base_db.csv')
df.to_sql(name='customers', con=con, if_exists='replace')
# Openai Key
openai.api_key = os.environ["openai"]


@app.get("/")
async def home(request: Request):
    try:
        return templates.TemplateResponse('index.html', {"request": request})

    except Exception as e:
        print(e)
        return templates.TemplateResponse('error.html', {"request": request})

@app.get("/demo")
async def demo(request: Request):
    try:
        sql = '''SELECT * FROM Customers LIMIT 1'''
        df = pd.read_sql(sql,con)
        inputs = df.loc[0].to_dict()
        prompt = get_prompt(inputs)
        text, link = get_tweet(prompt)
        return templates.TemplateResponse('demo.html', {"request": request, "link": link, "text": text})

    except Exception as e:
        print(e)
        return templates.TemplateResponse('error.html', {"request": request})



if __name__ == '__main__':
    if os.environ['MODE'] == 'dev':
        import uvicorn
        uvicorn.run(app, port=4242, host='0.0.0.0')