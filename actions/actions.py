# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
import json
import requests
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted, Restarted, SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
# from rasa.shared.core.events import AllSlotsReset

key = '2ccc483f4aaa466e86d1ad0603a37e8f'
with open('actions/city2loc.json', 'r', encoding='utf8') as f:
    city2loc = json.load(f)
url = 'https://devapi.qweather.com/v7/weather/now?'

class Quert_Climate(Action):
    def name(self) -> Text:
        return "action_query_city_climate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot('city')
        loc = city2loc.get(city, 0)
        res = requests.get(url, params={
            'key':key,
            'location':loc,
        })
        info = json.loads(res.content)
        print(info)
        if info['code'] != '200':
            dispatcher.utter_message('目前没有该城市的信息呢。')
            return []
        response = f'{city}的实况温度为{info["now"]["temp"]}℃。'
        dispatcher.utter_message(text=response)
        # return [AllSlotsReset()]
        return []


class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self):
        return 'action_default_fallback'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message('我不理解您的意思呢')
        return [UserUtteranceReverted()]
