from django.db import models
import os
import hashlib
import hmac
import json
import base64
import time
import requests
from rest_framework.response import Response


from django.utils.timezone import now


def make_signature(string):
    secret_key = bytes("05HdU5LygzTgFq9fYdQebZmUt566iirKnJLO1gzu", "UTF-8")
    string = bytes(string, "UTF-8")
    string_hmac = hmac.new(secret_key, string, digestmod=hashlib.sha256).digest()
    string_base64 = base64.b64encode(string_hmac).decode("UTF-8")
    return string_base64


# def make_signature(message):
#     # timestamp = int(time.time() * 1000)
#     # timestamp = str(timestamp)

#     # access_key = os.environ.get("SMS_ACCESS_KEY_ID")
#     SMS_SECRET_KEY = os.environ.get("SMS_SERVICE_SECRET")
#     secret_key = bytes(SMS_SECRET_KEY, "UTF-8")

#     # method = "POST"
#     # uri = "/sms/v2/services/ncp:sms:kr:278317119934:shinestudyplace/messages"
#     # # /sms/v2/services/{serviceId}/messages 문자 서비스 같은 경우 com 뒤에서 부터 끝까지 넣어준다.
#     # # serviceId는 사용하려는 API의 ServiceID를 넣어준다. 아래 사진 참조
#     # message = method + " " + uri + "\n" + timestamp + "\n" + access_key
#     # message = bytes(message, "UTF-8")
#     signingKey = base64.b64encode(
#         hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()
#     )
#     return signingKey


def sendAuthCode(data):

    SMS_ACCESS_KEY_ID = os.environ.get("SMS_ACCESS_KEY_ID")
    SERVICE_ID = os.environ.get("SERVICE_ID")

    phone_number = data["phone_number"]
    auth_number = data["auth_number"]

    url = "https://sens.apigw.ntruss.com"
    uri = "/sms/v2/services/ncp:sms:kr:278317119934:shinestudyplace/messages"
    api_url = url + uri
    timestamp = str(int(time.time() * 1000))
    access_key = "TYl4BI7hgRhRlcaViWWU"
    string_to_sign = "POST " + uri + "\n" + timestamp + "\n" + access_key
    signature = make_signature(string_to_sign)
    print(signature)

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": access_key,
        "x-ncp-apigw-signature-v2": signature,
    }
    message = f"안녕하세요?샤인스터디플레이스입니다.\n고객님의 인증번호는{auth_number}입니다."  # 메세지 내용을 저장
    phone = "01067090956"
    body = {
        "type": "SMS",
        "contentType": "COMM",
        "from": "01028720404",
        "content": message,
        "messages": [{"to": phone}],
    }
    body = json.dumps(body)
    response = requests.post(api_url, headers=headers, data=body)
    print(response.json())
    sms_json = response.json()
    if sms_json["statusCode"] == "202":
        return True
    else:
        return False


def aboutPassword(data):
    # serviceId = os.environ.get("NAVER_SMS")
    SMS_ACCESS_KEY_ID = os.environ.get("SMS_ACCESS_KEY_ID")
    phone_number = data["phone_number"]
    password = data["password"]
    # date = request.data.get("date")
    timestamp = str(int(time.time() * 1000))

    url = "https://sens.apigw.ntruss.com"
    uri = (
        "/alimtalk/v2/services/"
        + "ncp:kkobizmsg:kr:2564166:todaysaladtakl"
        + "/messages"
    )
    api_url = url + uri
    string_to_sign = "POST " + uri + "\n" + timestamp + "\n" + SMS_ACCESS_KEY_ID
    signature = make_signature(string_to_sign)

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": SMS_ACCESS_KEY_ID,
        "x-ncp-apigw-signature-v2": signature,
    }
    body = {
        "plusFriendId": "@투데이샐러드",
        "templateCode": "findpass",
        "messages": [
            {
                "countryCode": "82",
                "to": phone_number,
                "content": f"😀 안녕하세요?  투데이샐러드입니다 .😀\n고객님의 비밀번호는\n\n{password} 입니다.\n\n새로 설정된 패스워드로 로그인 하시고,\n\n새로운 패스워드로 설정하세요.\n\n항상 최선을 다하는 투데이샐러드가 되겠습니다.",
            }
        ],
    }
    body = json.dumps(body)
    sms_requests = requests.post(api_url, headers=headers, data=body)
    sms_json = sms_requests.json()

    if sms_json["statusCode"] == "202":
        return True
    else:
        return False


def aboutId(data):
    # serviceId = os.environ.get("NAVER_SMS")
    SMS_ACCESS_KEY_ID = os.environ.get("SMS_ACCESS_KEY_ID")
    phone_number = data["phone_number"]
    userid = data["userid"]
    # date = request.data.get("date")
    timestamp = str(int(time.time() * 1000))

    url = "https://sens.apigw.ntruss.com"
    uri = (
        "/alimtalk/v2/services/"
        + "ncp:kkobizmsg:kr:2564166:todaysaladtakl"
        + "/messages"
    )
    api_url = url + uri
    string_to_sign = "POST " + uri + "\n" + timestamp + "\n" + SMS_ACCESS_KEY_ID
    signature = make_signature(string_to_sign)

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": SMS_ACCESS_KEY_ID,
        "x-ncp-apigw-signature-v2": signature,
    }
    body = {
        "plusFriendId": "@투데이샐러드",
        "templateCode": "findid",
        "messages": [
            {
                "countryCode": "82",
                "to": phone_number,
                "content": f"😀 안녕하세요?  투데이샐러드입니다 .😀\n\n고객님의 아이디는\n\n{userid} 입니다.\n\n항상 최선을 다하는 투데이샐러드가 되겠습니다.",
            }
        ],
    }
    body = json.dumps(body)
    sms_requests = requests.post(api_url, headers=headers, data=body)
    sms_json = sms_requests.json()

    if sms_json["statusCode"] == "202":
        return True
    else:
        return False
