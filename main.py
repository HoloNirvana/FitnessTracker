import requests
import os
from datetime import datetime

API_KEY = os.environ['API_KEY']
APP_ID = os.environ['APP_ID']
PASSWORD = os.environ['PASSWORD']
USERNAME = os.environ['USERNAME']
SHEETY_ENDPOINT = os.environ['SHEETY_ENDPOINT']
exercise_endpoint = os.environ['exercise_endpoint']

GENDER = "man"
WEIGHT_KG = 100
HEIGHT_CM = 190
AGE = 35


# main info extraction from text
def get_info_from_text(text):

    # request part
    nutr_param = {
        "query": text,
        "gender": GENDER,
        "weight_kg": WEIGHT_KG,
        "height_cm": HEIGHT_CM,
        "age": AGE
    }

    headers = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY,
    }

    r = requests.post(url=exercise_endpoint, json=nutr_param, headers=headers)

    # building aprpriate info structure
    today = datetime.now()
    info = []
    for exercise in r.json()["exercises"]:
        data = {
            "workout": {
                "date": str(today.strftime("%d/%m/%Y")),
                "time": str(today.strftime("%H:%M:%S")),
                "exercise": exercise["name"],
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"],
            }
        }
        info.append(data)
    return info

# geting all data rows fron gsheet
def gsheet_get_data():
    # print(SHEETY_ENDPOINT,(USERNAME, PASSWORD))
    r = requests.get(url=SHEETY_ENDPOINT, auth=(USERNAME, PASSWORD))
    return r.text

# adding new data rows to gsheet
def gsheet_add_data(info):
    for data in info:
        requests.post(url=SHEETY_ENDPOINT, json=data, auth=(USERNAME, PASSWORD))


if __name__ == "__main__":
    user_input = input("enter your activity: ")
    info = get_info_from_text(user_input)
    gsheet_add_data(info)
    # gsheet_get_data()
   
    # print(API_KEY)
    # print(APP_ID) 
    # print(PASSWORD)
    # print(USERNAME)
    # print(SHEETY_ENDPOINT)
    # print(exercise_endpoint)