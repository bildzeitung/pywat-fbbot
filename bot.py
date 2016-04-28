"""
wat-bot

This bot listens incoming connections from Facebook.

Any message is sent as potential Javascript to node, and the console output
is sent back as a response.

"""

from flask import Flask, request
from pymessenger.bot import Bot
from subprocess import check_output
from tempfile import NamedTemporaryFile

import os
import requests

app = Flask(__name__)
TOKEN = "<token>"
bot = Bot(TOKEN)

def get_message(msg):
    tmp = NamedTemporaryFile(suffix='.js', delete=False)
    tmp.write('console.log(eval("%s"))' % msg)
    tmp.close()
    return check_output(['node', tmp.name])


@app.route("/webhook", methods = ['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == "<challenge>":
                return request.args.get("hub.challenge")
    if request.method == 'POST':
        output = request.json
        event = output['entry'][0]['messaging']
        for x in event:
            if (x.get('message') and x['message'].get('text')):
                message = x['message']['text']
                recipient_id = x['sender']['id']
                message = get_message(message)
            else:
                pass
        return "success"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
