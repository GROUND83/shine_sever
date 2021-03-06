from time import sleep
from django.shortcuts import render
import random
import base64
import string
from PIL import Image
from datetime import datetime, timedelta
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
import requests
import json
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework import status
from .models import User
from seats.models import Seat
from checks.models import Check
from vertifies.models import Vertifie
from .serializers import UserSerializer
from .permissions import IsSelf
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout, login
from django.conf import settings
from .Alimtalk import aboutPassword, aboutId, sendAuthCode
import jwt
from django.core.files.base import ContentFile
import datetime as pydatetime
from django.utils import timezone
import pytz
from ewelink.ewelink import Ewelink
from .utils import qrauth, dooropen, seatstate

# Create your views here.
class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "retrieve" or self.action == "delete":
            permission_classes = [IsAdminUser | IsSelf]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"])
    def delete(self, request):
        id = request.data["id"]
        username = request.data["username"]
        try:
            user = User.objects.get(id=id, username=username)
            user.delete()
            return Response({"message": "delete"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"message": "user not found"}, status=status.HTTP_401_UNAUTHORIZED
            )

    # ?????????
    @action(detail=False, methods=["post"])
    def auth(self, request):
        phone = request.data["phone"]
        password = request.data["password"]
        # ?????? ??????
        try:
            userPhone = User.objects.get(phone=phone)
            if userPhone is not None:
                user = authenticate(phone=phone, password=password)
                if user is not None:
                    # ????????? ?????????
                    encoded_jwt = jwt.encode(
                        {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
                    )
                    return Response(data={"token": encoded_jwt, "id": user.pk})
                else:
                    # ????????? ????????? ?????? ?????? ??????
                    return Response(
                        {"message": "??????????????? ?????????????????????."},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
        except User.DoesNotExist:
            return Response(
                {"message": "??????????????? ????????????."}, status=status.HTTP_401_UNAUTHORIZED
            )

    # deviceId ????????????
    @action(detail=False, methods=["post"])
    def onsignalId(self, request):
        onsignalId = request.data.get("onsignalId")
        id = request.data.get("id")

        user = User.objects.get(id=id)

        if user is not None:
            # ????????? ?????????
            user.onsignalId = onsignalId
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            # ????????? ????????? ?????? ?????? ??????
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=["post"])
    def startQrcode(self, request):
        # ????????? qr????????? open ???
        id = request.data.get("id")
        time = request.data.get("time")
        randomcode = random.randint(1000, 10000)
        user = User.objects.get(id=id)

        if user is not None:
            # ????????? ?????????
            user.qrauthcode = randomcode
            user.qrtime = time
            user.save()
            return Response(
                data={"deviceId": user.deviceId, "randomcode": randomcode},
                status=status.HTTP_200_OK,
            )
        else:
            # ????????? ????????? ?????? ?????? ??????
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=["post"])
    def loungeCheck(self, request):
        # qrauth
        # ???????????? (type = "switch.loungdoor")
        deviceId = request.data.get("deviceId")
        randomcode = request.data.get("randomcode")
        print(deviceId, randomcode)
        qrcheck = qrauth(deviceId=deviceId, randomcode=randomcode)
        print(qrcheck)
        if qrcheck:
            loungdoor = dooropen(type="switch.loungdoor")
            if loungdoor:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "??????????????????"}, status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response({"message": "??????????????????"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=["post"])
    def mainCheck(self, request):
        # qrauth
        # ???????????? (type = "switch.loungdoor")
        deviceId = request.data.get("deviceId")
        randomcode = request.data.get("randomcode")
        print(deviceId, randomcode)
        qrcheck = qrauth(deviceId=deviceId, randomcode=randomcode)
        print(qrcheck)

        if qrcheck:
            # maindoor = dooropen(type="switch.maindoor")
            maindoor = dooropen(type="switch.loungdoor")
            if maindoor:
                # ?????? ??????
                seatcheck = seatstate(deviceId=deviceId, type="in")
                print(seatcheck)
                if seatcheck:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"message": "??????????????????"}, status=status.HTTP_401_UNAUTHORIZED
                    )
            else:
                return Response(
                    {"message": "??????????????????"}, status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response({"message": "??????????????????"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=["post"])
    def mainCheckOut(self, request):
        # ????????????
        deviceId = request.data.get("deviceId")
        randomcode = request.data.get("randomcode")
        print(deviceId, randomcode)
        qrcheck = qrauth(deviceId=deviceId, randomcode=randomcode)
        print(qrcheck)

        if qrcheck:

            seatcheck = seatstate(deviceId=deviceId, type="out")
            print(seatcheck)
            if seatcheck:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "??????????????????"}, status=status.HTTP_401_UNAUTHORIZED
                )

        else:
            return Response({"message": "??????????????????"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=["post"])
    def register(self, request):

        phone = request.data["phone"]
        gender = request.data["gender"]
        password = request.data["password"]
        username = request.data["username"]
        user_type = request.data["user_type"]
        user_birth = request.data["user_birth"]
        personalPolicy = request.data["personalPolicy"]
        deviceId = request.data["deviceId"]

        school_name = request.data["school_name"]
        school_grade = request.data["school_grade"]
        avator = request.data["user_image"]
        format, imgstr = avator.split(";base64,")
        ext = format.split("/")[-1]
        user_image = ContentFile(
            base64.b64decode(imgstr), name=f"{username}-{datetime.now().second}.{ext}"
        )
        timeAlram = True
        eventAlram = True

        # onsignalId = request.data["onsignalId"]
        try:
            user = User.objects.get(phone=phone)

            return Response(
                data={"message": "?????????????????? ?????? ??????????????????."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except User.DoesNotExist:
            # ??????????????? ??????
            user = User.objects.create(
                phone=phone,
                gender=gender,
                password=password,
                username=username,
                user_type=user_type,
                user_birth=user_birth,
                personalPolicy=personalPolicy,
                school_name=school_name,
                school_grade=school_grade,
                timeAlram=timeAlram,
                eventAlram=eventAlram,
                user_image=user_image,
                deviceId=deviceId
                # onsignalId=onsignalId,
            )
            user.set_password(password)
            user.save()
            user = authenticate(phone=phone, password=password)
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "id": user.pk})

    # ??????????????? ????????????
    @action(detail=False, methods=["post"])
    def updatepush(self, request):
        pushid = request.data.get("pushuserId")
        userid = request.user.id
        try:
            # ?????? ?????? ??????
            user = User.objects.get(id=userid)
            user.onsignalId = pushid
            user.save()
            return Response(data={"message": "ok"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # ?????? ?????? ??????
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    # ????????????
    @action(detail=False, methods=["post"])
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

    # ???????????? ??????
    @action(detail=False, methods=["post"])
    def sendsms(self, request):

        phone_number = request.data.get("phone")
        auth_number = random.randint(1000, 10000)
        print(phone_number)
        try:
            user = User.objects.get(phone=phone_number)
            if user is not None:
                # ????????? ?????? ?????? ?????????
                data = {"phone_number": phone_number, "auth_number": auth_number}
                sendSMS = sendAuthCode(data=data)

                if sendSMS is True:
                    Vertifie.objects.update_or_create(
                        phone=phone_number,
                        defaults={
                            "code": auth_number,
                            "limitTime": datetime.now() + timedelta(seconds=180),
                        },
                    )
                    # sms ??????

                    return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # ????????????
            return Response(
                {"message": "????????? ?????????????????????."}, status=status.HTTP_400_BAD_REQUEST
            )

    # ???????????? ?????? ??????
    @action(detail=False, methods=["post"])
    def vertisms(self, request):
        phone_number = request.data.get("phone")
        code = request.data.get("code")
        try:
            verti = Vertifie.objects.get(phone=phone_number)
            if verti is not None:

                if verti.limitTime > timezone.now():
                    if verti.code == code:
                        auth_number = random.randint(1000, 10000)
                        newpassword = f"Shinestudyplace{auth_number}"

                        try:
                            user = User.objects.get(
                                phone=phone_number,
                            )
                            if user is not None:
                                user.set_password(newpassword)
                                user.save()
                                data = {
                                    "password": newpassword,
                                    "phone_number": phone_number,
                                }
                                kakao = aboutPassword(data=data)
                                if kakao is True:
                                    return Response(
                                        {"message": "success"},
                                        status=status.HTTP_200_OK,
                                    )
                                else:
                                    return Response(
                                        {"message": "sms fail"},
                                        status=status.HTTP_400_BAD_REQUEST,
                                    )
                        except User.DoesNotExist:
                            return Response(
                                {"message": "?????????????????? ????????????."},
                                status=status.HTTP_400_BAD_REQUEST,
                            )

                    else:
                        # ??????????????? ?????? ?????? ?????? ??????
                        return Response(
                            {"message": "??????????????? ????????????."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    return Response(
                        {"message": "??????????????? ?????? ???????????????."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        except Vertifie.DoesNotExist:
            # ??????????????? ??????
            return Response(status=status.HTTP_400_BAD_REQUEST)
