import openai
import pandas as pd
import urllib.parse
import os
from email.message import EmailMessage
import smtplib
from random import randint

'''Core Functions'''
def get_prompt(inputs):
    shuffle_int = randint(1,2)
    wc = inputs[f'wc{shuffle_int}']
    # generate prompt
    prompt = f"You are a social media manager for a {inputs['size']}, {inputs['industry']}" \
             f" company based in {inputs['loc_city']}, {inputs['loc_state']} called {inputs['name']}." \
             f" Write a tweet that is topical and {wc} to be sent as part of a social-media" \
             f" marketing campaign "  # randomly append website link
    return prompt


def get_tweet(prompt):

    # get tweet content
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt.split('.')[0]},
            {"role": "user", "content": prompt.split('.')[1]},
        ]
    )

    text = resp.choices[0].message['content']

    # encode prompt
    text_safe = urllib.parse.quote(text)
    intent = f'https://twitter.com/intent/tweet?text={text_safe}'

    return text, intent

def sendEmail(text,link):
    email_address = "johnmcummings3@gmail.com"
    email_password = os.environ['email_code']

    # create email
    msg = EmailMessage()
    msg['Subject'] = f"Tweet This!"
    msg['From'] = email_address
    msg['To'] = email_address
    msg.set_content(f"Tweet This! \n {text} \n Click here to tweet: {link}")

    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

''' Main Run'''
# Openai Key
openai.api_key = os.environ["openai"]
# Build "db"
df = pd.read_csv('base_db.csv')

for id in df['uid'].to_list():
    temp_df = df[df['uid']==id]
    if temp_df.shape[0]==1:
        inputs = temp_df.head(1).to_dict()
        prompt = get_prompt(inputs)
        text, link = get_tweet(prompt)
        sendEmail(text, link)
        print(text, link)
    else:
        print(f'error: {id}')