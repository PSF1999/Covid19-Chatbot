# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/
# python -m rasa run --m ./models --endpoints endpoints.yml --port 5005 -vv --enable-api

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionCoronaTracker(Action):

    def name(self) -> Text:
        return "action_corona_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get("https://api.covid19india.org/data.json").json()
        
        entities = tracker.latest_message['entities']
        print("Last Message Now",entities)
        state = None
        for e in entities:
            if e['entity'] == "state":
                state = e['value']

        for data in response["statewise"]:
            if data["state"] == state.title():
                active = data["active"]

        dispatcher.utter_message(text="Total active cases in {} are {}".format(state.title(),active))

        return []
