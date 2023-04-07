import openai
import pandas as pd
import urllib.parse
import os
from email.message import EmailMessage
import smtplib
from random import randint
import gspread
from io import StringIO

'''Core Functions'''
def drive_con():
    creds = {
      "type": os.environ['g_type'],
      "project_id": os.environ['g_proj_id'],
      "private_key_id": os.environ['g_priv_key_id'],
      "private_key": os.environ['g_priv_key'].replace('\\n', '\n'),
      "client_email": os.environ['g_client_email'],
      "client_id": os.environ['g_client_id'],
      "auth_uri": os.environ['g_auth_uri'],
      "token_uri": os.environ['g_token_uri'],
      "auth_provider_x509_cert_url": os.environ['g_auth_prov_cirt'],
      "client_x509_cert_url": os.environ['g_client_cirt_url'],
    }
    sa = gspread.service_account_from_dict(creds)
    return sa


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

def sendEmail(text,link,to_email):
    from_email_address = "johnmcummings3@gmail.com"
    to_email_address = to_email
    print(to_email_address)
    email_password = os.environ['email_code']

    # create email
    msg = EmailMessage()
    msg['Subject'] = f"Tweet This!"
    msg['From'] = from_email_address
    msg['To'] = to_email_address
    msg.set_content(f"Tweet This! \n {text} \n Click here to tweet: {link}")

    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(from_email_address, email_password)
        smtp.send_message(msg)

''' Main Run'''
# Openai Key
openai.api_key = os.environ["openai"]
# Build "db"
sa = drive_con()
sh = sa.open('auto_tweet').sheet1
df = pd.DataFrame(sh.get_all_records())

for id in df['uid'].to_list():
    temp_df = df[df['uid']==id]
    if temp_df.shape[0]==1:
        inputs = temp_df.T[id].to_dict()
        prompt = get_prompt(inputs)
        text, link = get_tweet(prompt)
        sendEmail(text, link, inputs['email'].strip())
        print(text, link)
    else:
        print(f'error: {id}')