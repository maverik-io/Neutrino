from flask import Flask
from threading import Thread
import random
import datetime
from pickle import load



app = Flask('')
now = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)
formatted_time = now.strftime("%I:%M:%S %p on %d/%m/%y")
website = ''
with open('website.html','r') as f:
    website = f.read()

@app.route('/')
def home():
  C = {}
  with open('Vars.dat','rb') as f:
    C = load(f)

  string = '<table style="color:#6DB7C0;border: 2px solid #6DB7C0;width : 100%;border-collapse: collapse;"><th>Name</th><th>Balance</th>'
  for i,j in C.items():
    string += f'<tr><td style = "border: 2px solid #6DB7C0;">{i}</td><td style = "border: 2px solid #6DB7C0;">∆{j}</td></tr>'

  string+='</table ">'
  htmlStuff = website.replace('[formatted_time]',formatted_time).replace('[table]',string)
  return htmlStuff

def run():
  app.run(
		host='0.0.0.0',
		port=random.randint(2000,9000)
	)

def keep_alive():
	'''
	Creates and starts new thread that runs the function run.
	'''
	t = Thread(target=run)
	t.start()