
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny,IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .permissions import IsSelf
from users.models import User
from .models import Complaint
from .serializers import CompliantSerializer


class ComplaintViewSet(ModelViewSet):
  queryset = Complaint.objects.all()
  serializer_class = CompliantSerializer

  def get_permissions(self):
      if self.action == "list":
          permission_classes = [IsAdminUser | IsSelf]
      elif self.action == "retrieve" :
          permission_classes = [IsAdminUser | IsSelf]
      elif self.action == "complaintCreate" :
          permission_classes = [AllowAny]
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
          query_set = queryset.filter(author=user)
          return query_set

  @action(detail=False, methods=["post"])  
  def complaintCreate(self, request ):
        # 알림 관리자
        content = request.data["content"]
        complaintype = request.data["complaintype"]
        user= User.objects.get(id = request.user.id)
        # print(user)
        compliant = Complaint.objects.create(content=content,complaintype=complaintype,author=user)
        if compliant:
            return Response(status=status.HTTP_200_OK,)
        else:
            # 유저가 없으면 먼가 잘못 됬음
            return Response(status=status.HTTP_404_NOT_FOUND)

