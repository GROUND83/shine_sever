import os
import requests
import json
from rest_framework.response import Response
from rest_framework import status
from config.settings import get_secret

def sendpush(data):
    playerId = data["playerId"]
    # customdata = data["data"]
    headings = data["headings"]
    subtitle = data["subtitle"]
    contents = data["contents"]

    # restkey = os.environ.get("ONESIGBAL_REST")
    # appid = os.environ.get("ONESIGNAL_APPID")
    ONESIGNAL_KEY = get_secret("ONESIGNAL_KEY")
    header = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {ONESIGNAL_KEY}",
    }
    payload = {
        "app_id": get_secret("ONESIGNAL_ID"),
        "include_player_ids": [playerId],
        # "ios_sound": "nil",
        # "ios_badgeType": "Increase",
        # "ios_badgeCount": 1,
        "headings": {"en": "English Message", "ko": headings},
        # "subtitle": {"en": "English Message", "ko": subtitle},
        "contents": {"en": "English Message", "ko": contents},
        # "data": customdata,
    }

    req = requests.post(
        "https://onesignal.com/api/v1/notifications",
        headers=header,
        data=json.dumps(payload),
    )

    return req
    # return Response(data=req.reason, status=status.HTTP_200_OK)
