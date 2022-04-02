from django.shortcuts import render
import random
import base64
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import User, UserType
from vertifies.models import Vertifie
from .serializers import UserSerializer
from .permissions import IsSelf
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth import authenticate, logout, login
from django.conf import settings
from .Alimtalk import aboutPassword, aboutId, sendAuthCode
import jwt
from django.core.files.base import ContentFile

# Create your views here.
class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "retrieve":
            permission_classes = [IsSelf]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"])
    def authQrcode(self, request):
        phone = request.data["phone"]

        # 유저 인증
        # user = authenticate(phone=phone, password=password)
        # print(user)
        user = User.objects.get(phone=phone)
        if user is not None:
            # 유저가 있으면
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "id": user.pk})
        else:
            # 유저가 없으면 먼가 잘못 됬음
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=["post"])
    def auth(self, request):
        phone = request.data["phone"]
        password = request.data["password"]
        # 유저 인증
        print(phone)
        user = authenticate(phone=phone, password=password)
        print(user)
        if user is not None:
            # 유저가 있으면
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "id": user.pk})
        else:
            # 유저가 없으면 먼가 잘못 됬음
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=["post"])
    def register(self, request):
        def decodeDesignImage(data):
            try:
                data = base64.b64decode(data.encode("UTF-8"))
                buf = io.BytesIO(data)
                img = Image.open(buf)
                return img
            except:
                return None

        phone = request.data["phone"]
        password = request.data["password"]
        username = request.data["username"]
        user_type = request.data["user_type"]
        user_birth = request.data["user_birth"]
        personalPolicy = request.data["personalPolicy"]
        parent_phone = request.data["parent_phone"]
        parent_name = request.data["parent_name"]
        is_shine = request.data["is_shine"]
        school_name = request.data["school_name"]
        school_grade = request.data["school_grade"]
        avator = request.data["user_image"]
        format, imgstr = avator.split(";base64,")
        ext = format.split("/")[-1]
        user_image = ContentFile(base64.b64decode(imgstr), name=username + ext)
        timeAlram = True
        eventAlram = True
        userType = UserType.objects.get(name=user_type)
        # onsignalId = request.data["onsignalId"]
        try:
            user = User.objects.get(phone=phone)

        except User.DoesNotExist:
            # 유저있는지 판단
            user = User.objects.create(
                phone=phone,
                password=password,
                username=username,
                user_type=userType,
                user_birth=user_birth,
                personalPolicy=personalPolicy,
                parent_phone=parent_phone,
                parent_name=parent_name,
                is_shine=is_shine,
                school_name=school_name,
                school_grade=school_grade,
                timeAlram=timeAlram,
                eventAlram=eventAlram,
                user_image=user_image
                # onsignalId=onsignalId,
            )
            user.set_password(password)
            user.save()
            user = authenticate(phone=phone, password=password)
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "id": user.pk})

        return Response(
            data={"message": "핸드폰번호가 이미 사용중입니다."}, status=status.HTTP_401_UNAUTHORIZED
        )

    # 푸쉬아이디 업데이트
    @action(detail=False, methods=["post"])
    def updatepush(self, request):
        pushid = request.data.get("pushuserId")
        userid = request.user.id
        try:
            # 중복 검사 실패
            user = User.objects.get(id=userid)
            user.onsignalId = pushid
            user.save()
            return Response(data={"message": "ok"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # 중복 검사 성공
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=["post"])
    def id_check(self, request):
        phone = request.data.get("phone")
        try:
            # 중복 검사 실패
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            # 중복 검사 성공
            user = None
        if user is None:
            possible = True
        else:
            possible = False
        return Response(data={"possible": possible}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def sendsms(self, request):
        phone_number = request.data.get("phone")
        auth_number = random.randint(1000, 10000)
        print(phone_number)
        try:
            user = User.objects.get(phone=phone_number)
            if user is not None:
                # 핸드폰 번호 이미 사용중
                return Response(
                    {"message": "핸드폰번호가 이미 사용중입니다."},
                    status=status.HTTP_204_NO_CONTENT,
                )
        except User.DoesNotExist:
            data = {"phone_number": phone_number, "auth_number": auth_number}
            kakao = sendAuthCode(data=data)

            if kakao is True:
                Vertifie.objects.update_or_create(
                    phone=phone_number, defaults={"code": auth_number}
                )
                # sms 보냄
                return Response(status=status.HTTP_200_OK)
            else:
                # 오류발생
                return Response(
                    {"message": "오류가 발생하였습니다."}, status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=False, methods=["post"])
    def vertisms(self, request):
        phone_number = request.data.get("phone")
        code = request.data.get("code")
        try:
            verti = Vertifie.objects.get(phone=phone_number)
            if verti is not None:
                if verti.code == code:
                    return Response(
                        status=status.HTTP_200_OK,
                    )
                else:
                    # 인증번호가 틀림
                    return Response(
                        status=status.HTTP_204_NO_CONTENT,
                    )
        except Vertifie.DoesNotExist:
            # 인증번호가 없음
            return Response(status=status.HTTP_400_BAD_REQUEST)
