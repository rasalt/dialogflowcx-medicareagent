# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_storage_app]
import logging
import os

from flask import Flask, jsonify, request, make_response

app = Flask(__name__)


#from model import InputForm
import sys
import json
import google.cloud 
from google.cloud import bigquery
from datetime import datetime
from datetime import date

# [START healthcare_get_session]
project_id = os.environ['PROJECT_ID']
cloud_region = os.environ['REGION']

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

#http://10.1.1.1:5000/login?username=alex&password=pw1
#Row(('0', '81fc5cdf-7a61-43fe-8f61-5eb21a480174', 'Bunny174', 'Sauer652', '328 Howell Crossroad', 'Kingston', 'Massachusetts', '02364', datetime.date(1972, 8, 12), 'NULL'), {'id': 0, 'fhirid': 1, 'name': 2, 'familyname': 3, 'addressline': 4, 'addresscity': 5, 'addressstate': 6, 'addresspostalcode': 7, 'dob': 8, 'email': 9})


def insert_order(transaction, state, custy, product):
    from random import randint

    destination = custy['addressline'] + ' ' + custy['addresscity'] + ' ' + custy['addressstate'] + ' ' + custy['addresspostalcode']
    row_ct = transaction.execute_update(
        "INSERT OrderProcessing (Date, Product, Quantity, FromDistribCenter, CustomerId, Destination, OrderId)  VALUES ('{}', '{}', 1, '{}','{}','{}',{})".format(str(date.today()), product, state, custy['id'], destination, randint(0,65535))
    )
    print("{} record(s) inserted.".format(row_ct))
    data = 'Hello '+ custy['name'] + ' ' + custy['familyname'] + '.' + ' Your order of ' + product + ', Quantity of 1 is placed on ' + str(date.today()) + ' . It will be shipped to ' + destination + ' within the next 24 hours. '
    send_sms(data, custy['phnumber'])

def determineLiveAgentHandoff(req, intent, params):
    fulfillmenttext = "Sorry, you seem to be having a bad day. Let's get you connected to our staff"
    return {'fulfillmentText': fulfillmenttext, "liveAgentHandoff": 'true'}

def welcomeIntent(req, intent, params, source):
    fulfillmenttext = "Welcome to the Medtronic Support Portal." 
    if (source == "CHAT"):
       fulfillmenttext = fulfillmenttext + " Please enter your email address, last name, and date of birth to confirm your identity."
    
    if (source == "PHONE"):
       fulfillmenttext = fulfillmenttext + "  We have found your phone number on file. To verify your identity we will ask for your last name and date of birth. Please start by saying your last name."

    return {'fulfillmentText': fulfillmenttext}
      
# Global variable    
sessionval = {}
def getDialogflowParams(req):
    sess = req["sessionInfo"]
    param = sess["parameters"]
    return param

def getDialogflowIntent(req):
    param = req["fulfillmentInfo"]
    intent = param["tag"]
    return intent

def getDialogflowText(req):
    return req['text']

def addDataDb(project_id, dataset, table, params):
    print("Params are {}".format(params))
    from google.cloud import bigquery
    client = bigquery.Client()
    table_id = project_id + "." + dataset + "."+table
    rowdata = {}

    rowdata["membername"] = params["fullname"]
    rowdata["alcoholproblem"] = params['alcoholproblem'] 
    rowdata["doctors"] = [] 

    for i in params['doctor']:
        print("i is {}".format(i))
        rowdata["doctors"].append(i["name"])

    rowdata["practices"] = [] 
    for i in params['practice']:
        rowdata["practices"].append(i["business-name"])

    rowdata["alcoholfrequency"] = params['drink_frequency']
    rowdata["hospitalsadmitted"] = params['hospital']
    if (params['pcp_aware']=="False"):
        rowdata["pcp_aware"] = False
    else:
        rowdata["pcp_aware"]= True
    rowdata["tobaccoproducts"] = params['tobaccoprod']
    
    print("Rowdata is {}".format(rowdata))

    rows_to_insert = [
      rowdata
    ]

    errors = client.insert_rows_json(
      table_id, rows_to_insert, row_ids=[None] * len(rows_to_insert)
    )  # Make an API request.
    if errors == []:
      print("New rows have been added.")
    else:
      print("Encountered errors while inserting rows: {}".format(errors))
    return True

@app.route("/webhook", methods=['GET', 'POST'])
def webhook():

    project_id = os.environ['PROJECT_ID']
    dataset = os.environ['DATASET']
    table_id = os.environ['TABLE_ID']
    req = request.get_json() 
    print(" REQUEST IS: {}".format(req))  
    params = getDialogflowParams(req)
    intent = getDialogflowIntent(req)
    if intent == "webhook_end":
        # Write all the parameters into Bigquery
        # Print parameters
	#print("Parameters are {}".format(request['sessionInfo']['parameters']))
        addDataDb(project_id, dataset, table_id, params)
  
    #print("Val is {}".format(val))  
    val = ""
    webhookresponse = {}
    webhookresponse['fulfillment_response'] = {}
    webhookresponse['fulfillment_response']['messages'] = []


    
    webhookresponse['sessionInfo'] = {}
    webhookresponse['sessionInfo']['parameters'] = params

    message = {}
    message['text'] = {}
    message['text']['text'] = []
    message['text']['text'].append(val)

    webhookresponse['fulfillment_response']['messages'].append(message)
   
    print("Webhookresponse is {}".format(webhookresponse))
    resp = json.dumps(webhookresponse, indent=4)
    r = make_response(resp)
    r.headers['Content-Type'] = 'application/json'
    return r

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
