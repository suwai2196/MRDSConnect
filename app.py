import urllib
import json
import os

from pprint import pprint

from flask import Flask
from flask import request
from flask import make_response

#Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])

def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") == "listPizzas":

        #result = req.get("result")
        #parameters = result.get("parameters")
        #zone = parameters.get("bank-name")
        speech = "The offered pizzas are "
        print("Response:")
        print(speech)
        return {
            "fulfillmentText": speech,
            "displayText": '25',
            "source": "pizzaWebhook"
        }

    if __name__ == '__main__':
        port = int(os.getenv('PORT', 80))
        print("Starting app on port %d" % (port))
        app.run(debug=True, port=port, host='0.0.0.0')
