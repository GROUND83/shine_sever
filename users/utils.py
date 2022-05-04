import requests
import json
from time import sleep
from .models import User
from seats.models import Seat
from checks.models import Check
from rest_framework.response import Response
from rest_framework import status
import datetime as pydatetime
from ewelink.ewelink import Ewelink


def qrauth(deviceId, randomcode):
    try:
        user = User.objects.get(deviceId=deviceId)
        # 유저가 있으면
        qrtime = float(user.qrtime)
        print(qrtime)
        time = pydatetime.datetime.now().timestamp()
        print(float(time))
        if user.qrauthcode == randomcode and qrtime + 10 >= float(time):
            return True
        else:
            return False
    except User.DoesNotExist:
        return False


def dooropen(type):

    url = "http://112.164.194.217:8123/api/services/switch/toggle"
    headers = {
        "content-type": "application/json",
        "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI4Mzg4MDI3YTMxMjg0MDg5Yjc5YjMwYTllOTA3NzU4NyIsImlhdCI6MTY1MDA4MjkxNywiZXhwIjoxOTY1NDQyOTE3fQ.bE9QsAbsmDutcso_HCCx_7M6KdF73JZvH8ITVwV6I80",
    }
    body = {"entity_id": type}
    body = json.dumps(body)
    response = requests.post(url, headers=headers, data=body)
    sleep(0.5)
    response1 = requests.post(url, headers=headers, data=body)
    door_json = response1.json()
    print(door_json)
    if door_json[0]["state"] == "off":
        return True
    else:
        return False


def seatstate(deviceId, type):
    print(deviceId)
    try:
        user = User.objects.get(deviceId=deviceId)
        print(user)
        try:
            seat = Seat.objects.get(owner=user)
            print(seat)
            print(seat.lightId)
            ewe = Ewelink(email="wonchang.k@gmail.com", password="Flslwl1212")
            lightType = ewe.getDevice(id=seat.lightId)
            print(lightType["params"]["switch"])
            lightstatus = lightType["params"]["switch"]
            if type == "out":
                print(type)
                ewe.setDevicePowerStateOff(id=seat.lightId)
                Check.objects.create(
                    seatName=seat.seat_title, seatUser=user, check_type="퇴실"
                )
                return True
            else:
                print(type)
                if lightstatus == "off":
                    ewe.setDevicePowerStateOn(id=seat.lightId)
                elif lightstatus == "on":
                    ewe.setDevicePowerStateOff(id=seat.lightId)
                Check.objects.create(
                    seatName=seat.seat_title, seatUser=user, check_type="입실"
                )

                return True

        except Seat.DoesNotExist:
            return False

    except User.DoesNotExist:
        return False
