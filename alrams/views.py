from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Alram
from users.models import User
from .serializers import AlramSerializer

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from cores.onSignal import sendpush


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class AlramViewSet(ModelViewSet):
    queryset = Alram.objects.all()
    serializer_class = AlramSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action == "list"or self.action == "sentAlram":
            permission_classes = [AllowAny]
        elif  self.action == "retrieve" or  self.action == "myalram":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = self.queryset
       
        user = User.objects.get(id=self.request.user.id)
        # alram = Alram.objects.get(to=user)
        if user.is_staff:
            query_set = queryset
            return query_set
        elif user.is_staff is False:
            query_set = queryset.filter(to=user)
            return query_set
            
    @action(detail=False, methods=["post"])
    def sentAlram(self, request):
        # 체크인 대상자만 발송?
        playerId = request.data["playerId"]
        userId = request.data["userId"]
        headings = request.data["headings"]
        subtitle = request.data["subtitle"]
        contents = request.data["contents"]

        data = {
            "playerId": playerId,
            "headings": headings,
            "subtitle": subtitle,
            "contents": contents,
        }
        send = sendpush(data)
        print(send.status_code)
        if send.status_code == 200:
            print(userId)
            user = User.objects.get(pk=userId)
            Alram.objects.create(
                headings=headings,
                subtitle=subtitle,
                contents=contents,
                sented=True,
                senttime=timezone.localtime(),
                to=user,
            )
            return Response(
                status=status.HTTP_200_OK,
            )
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # @action(detail=False, methods=["get"])
    # def myalram(self, request):
    #     # 체크인 대상자만 발송?
     
    #     user = request.user
    #     print(user)
    #     alrams = Alram.objects.all(to_id=user.id)

    #     if alrams :
    #         serializer = AlramSerializer(alrams,many=True)
    #         return Response(serializer.data,
    #             status=status.HTTP_200_OK,
    #         )
    #     else:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)
