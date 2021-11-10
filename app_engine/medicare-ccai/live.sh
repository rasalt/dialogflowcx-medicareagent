{
  "responseId": "bf88c5ac-8098-4f77-9e2d-93dc6eb1f8f6-5811cb77",
  "queryResult": {
    "queryText": "yes",
    "action": "TalktoHuman.TalktoHuman-yes",
    "parameters": {},
    "allRequiredParamsPresent": true,
    "fulfillmentMessages": [
      {
        "platform": "TELEPHONY",
        "telephonySynthesizeSpeech": {
          "text": "Please hold while I transfer you to the next available representative."
        }
      },
      {
        "platform": "TELEPHONY",
        "telephonyTransferCall": {
          "phoneNumber": "+18322769309"
        }
      },
      {
        "text": {
          "text": [
            ""
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": "projects/ccai-med/locations/global/agent/sessions/7b76b9d2-cae3-b2c6-1d40-3ab3cbea0650/contexts/talktorep",
        "lifespanCount": 1
      }
    ],
    "intent": {
      "name": "projects/ccai-med/locations/global/agent/intents/75c7934a-100a-4956-9ea5-a0318324e226",
      "displayName": "Talk to Human - yes",
      "liveAgentHandoff": true
    },
    "intentDetectionConfidence": 1,
    "languageCode": "en",
    "sentimentAnalysisResult": {
      "queryTextSentiment": {
        "score": 0.6,
        "magnitude": 0.6
      }
    }
  },
  "agentId": "d0a4e54e-38bf-40e1-a285-17bb9db3d28b"
}
