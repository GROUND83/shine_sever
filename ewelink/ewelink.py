import requests, base64, hashlib, hmac, time, random, json, uuid, re

from typing import Dict

from .constants import Constants
from .exceptions import *
from .models import Object


class Ewelink(Constants):
    def __init__(self, email: str, password: str, phone: int = None):
        super().__init__()
        self.email = email
        self.password = password
        self.region = "as"
        self.phone = str(phone)
        self.API_URL = f"https://{self.region}-api.coolkit.cc:8080/api"
        # self.__check_creds_action()

    def getDevices(self):
        res = self.__make_request(
            uri="/user/device",
            qs=f"?lang=en&appid={self.APP_ID}&ts={str(time.time())}&version=6&getTags=1",
        )
        return Object(res.json())

    def getDevice(self, id: str):
        res = self.__make_request(
            uri="/user/device/" + id,
            qs=f"?deviceid={id}&appid={self.APP_ID}&nonce={self.__nonce()}&ts={str(time.time())}&version=6",
        )
        return Object(res.json())

    def setDevicePowerState(self, id: str, state: str, channel=1):
        cstate = self.getDevicePowerState(id, channel=channel)
        if state == "toggle":
            state = "on" if cstate == "off" else "off"
        res = self.__make_request(
            method="POST",
            uri="/user/device/status",
            json={
                "deviceid": id,
                "params": {"switch": state},
                "appid": self.APP_ID,
                "nonce": self.__nonce(),
                "ts": int(time.time()),
                "version": 6,
            },
        )
        res = self.__check_res(res.json())
        switch = self.getDevicePowerState(id)
        res["switch"] = switch
        return res

    def setDevicePowerStateOn(self, id: str,  channel=1):
        cstate = self.getDevicePowerState(id, channel=channel)
      
        res = self.__make_request(
            method="POST",
            uri="/user/device/status",
            json={
                "deviceid": id,
                "params": {"switch": "on"},
                "appid": self.APP_ID,
                "nonce": self.__nonce(),
                "ts": int(time.time()),
                "version": 6,
            },
        )
        res = self.__check_res(res.json())
        switch = self.getDevicePowerState(id)
        res["switch"] = switch
        return res
    def setDevicePowerStateOff(self, id: str,  channel=1):
        cstate = self.getDevicePowerState(id, channel=channel)
       
        res = self.__make_request(
            method="POST",
            uri="/user/device/status",
            json={
                "deviceid": id,
                "params": {"switch": "off"},
                "appid": self.APP_ID,
                "nonce": self.__nonce(),
                "ts": int(time.time()),
                "version": 6,
            },
        )
        res = self.__check_res(res.json())
        switch = self.getDevicePowerState(id)
        res["switch"] = switch
        return res
    def getDevicePowerState(self, id: str, channel=1):
        return self.getDevice(id)["params"]["switch"]

    def __make_request(
        self, uri: str, method: str = "GET", json: Dict[str, str] = {}, qs: str = ""
    ) -> requests.Response:
        try:
            res = requests.request(
                method,
                self.API_URL + uri + qs,
                headers={
                    "Authorization": f"Bearer {self.__get_creds()['at']}",
                },
                json=json,
            )
            return res
        except KeyError:
            raise Exception("Authorization failed.")

    def __check_creds(self) -> Dict[str, str]:
        res = self.__get_creds()
        try:
            keys = [i for i in res]
            if "region" in keys and "error" in keys:
                self.API_URL = f"https://{res['region']}-api.coolkit.cc:8080/api"
                res = self.__get_creds()
                keys = [i for i in res]
            if "at" in keys:
                return {"log": "ok", "status": "success"}
            print(res)
            return {"error": res["error"], "message": self.errors[res["error"]]}
        except KeyError:
            return {"log": "ok", "status": "success"}

    def __check_creds_action(self):
        temp = self.__check_creds()
        print(temp)
        try:
            if type(temp["error"]) == int:
                raise Exception(
                    "An error occured, please refer to the above dictionary for the problem."
                )
        except KeyError:
            pass

    def __get_creds(self) -> Dict[str, str]:
        if self.phone.isnumeric():
            if self.email.count("@") == 1 and self.email.count(".com") == 1:
                creds = self.__get_raw_creds(email=self.email, password=self.password)
            else:
                creds = self.__get_raw_creds(phone=self.phone, password=self.password)
        else:
            creds = self.__get_raw_creds(email=self.email, password=self.password)
        res = requests.request(
            "POST",
            self.API_URL + "/user/login",
            headers={
                "Authorization": f"Sign {creds[0]}",
            },
            json=creds[1],
        )
        return res.json()

    def __get_raw_creds(self, password: str, email=None, phone=None) -> list:
        creds = {
            "appid": self.APP_ID,
            "password": password,
            "ts": int(time.time()),
            "version": 6,
            "nonce": self.__nonce(),
            "os": "iOS",
            "model": "iPhone10,6",
            "romVersion": "11.1.2",
            "appVersion": "3.5.3",
            "imei": str(uuid.uuid4()),
        }
        if (
            not email
            or not re.match(
                r"^[a-zA-Z0-9.]+@[a-zA-Z\-]+\.[a-zA-Z]+(?:(?:\.[a-zA-Z]+)+?)?$",
                email,
                re.I,
            )
            and re.match(
                r"^(?:\+\d{,4})?\d{10}$",
                str(phone).replace(" ", "").replace("(", "").replace(")", ""),
            )
        ):
            creds["phoneNumber"] = phone
        else:
            creds["email"] = email
        return [
            base64.b64encode(
                hmac.new(
                    self.APP_SECRET,
                    msg=json.dumps(creds).encode(),
                    digestmod=hashlib.sha256,
                ).digest()
            ).decode(),
            creds,
        ]

    def __check_res(self, res: dict) -> dict:
        try:
            return {"error": res["error"], "message": self.errors[res["error"]]}
        except KeyError:
            return {"status": "ok"}

    def __nonce(self, len=15):
        return "".join(str(random.randint(0, 9)) for _ in range(len))
