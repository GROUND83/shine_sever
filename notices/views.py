from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Notice
from .serializers import NoticeSerializer

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class NoticeViewSet(ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action == "list"or self.action == "mainnotice"  or self.action == "retrieve":
            permission_classes = [AllowAny]

        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"])
    def mainnotice(self, request):
        notice = Notice.objects.all()[0:5]
        if notice is not None:
            # 유저가 있으면
            print(notice)
            serializer = NoticeSerializer(notice, many=True)
            print(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            # 유저가 없으면 먼가 잘못 됬음
            return Response(status=status.HTTP_404_NOT_FOUND)
