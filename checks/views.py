
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .permissions import IsSelf
from .models import Check
from users.models import User
from .serializers import CheckSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"

class CheckViewSet(ModelViewSet):
  queryset = Check.objects.all()
  serializer_class = CheckSerializer
  pagination_class = StandardResultsSetPagination


  def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser | IsSelf]
        elif self.action == "retrieve" :
            permission_classes = [AllowAny | IsSelf]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

  def get_queryset(self):
        queryset = self.queryset  
        user = User.objects.get(id=self.request.user.id)
      
        if user.is_staff:
            query_set = queryset
            return query_set
        elif user.is_staff is False:
            query_set = queryset.filter(seatUser=user)
            return query_set

  # def create(self, request, *args, **kwargs):
  #       # 알림 관리자
  #       print("알림 관리자")
  #       serializer = self.get_serializer(data=request.data)
  #       serializer.is_valid(raise_exception=True)
  #       self.perform_create(serializer)
   
  #       return Response(serializer.data, status=status.HTTP_201_CREATED)