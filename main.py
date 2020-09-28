import urllib
import json
import os

from pprint import pprint

from flask import Flask
from flask import request
from flask import make_response
from owlready2 import *

#Flask app should start in global layout
app = Flask(__name__)

def ConnectOnto():
    my_world = World()
    my_world.get_ontology("file://C:/Users/Hp/AppData/Local/Programs/Python/Python38-32/pythonProject/owl/mdrs.owl").load()  # path to the owl file is given here
    #sync_reasoner(my_world)
    # reasoner is started and synchronized here
    graph = my_world.as_rdflib_graph()
    return graph

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
    if req.get("queryResult").get("action") == "brandPhones":
        graph = ConnectOnto()
        result = req.get("queryResult")
        parameters = result.get("parameters")
        a = None

        brand = parameters.get("brand")
        #Activity = parameters.get("Activity")
        #c = ', tr:'.join(map(str, Activity))

        query = ("PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  \
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>  \
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  \
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>  \
                    PREFIX MDRS: <http://www.MRDS.com#> \
                    SELECT DISTINCT ?phone \
                    WHERE { ?phone MDRS:manufacturedBy ?brand.  \
                    FILTER(?brand=MDRS:%s)}" %(brand))
        results = graph.query(query)
        response = []
        for item in results:
            phone = str(item['phone'].toPython())
            phone = re.sub(r'.*#', "", phone)
            response.append('-' + phone)
            a = '\n'.join(map(str, response))
        print(a)
        if a is None:
            b = "Sorry, we don't have offer for you now."
        else:
            b = "These are offered devices for you from"+brand+"  \n" + a

        fulfillmentText = b
        print("Response:")
        print(fulfillmentText)
        return {
            # "data": {},
            # "contextOut": [],
            "speech": fulfillmentText,
            "fulfillmentText": fulfillmentText,
            "displayText": fulfillmentText,
            "source": "webhookdata"
        }

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))
    print("Starting app on port %d" % (port))
    app.run(debug=True, port=port, host='0.0.0.0')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
