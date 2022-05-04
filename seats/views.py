import json
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Seat
from .serializers import SeatSerializer
from .permissions import IsSelf
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

# Create your views here.
class SeatsViewSet(ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        elif (
            self.action == "retrieve"
            or self.action == "getseat"
            or self.action == "getseatAbout"
            or self.action == "byroom"
        ):
            permission_classes = [IsAdminUser | AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"])
    def getseat(self, request):
        id = request.data.get("id")
        try:
            seat = Seat.objects.get(owner=id)
            if seat is not None:
                # 유저가 있으면
                serializer = SeatSerializer(seat)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                )
            else:
                # 유저가 없으면 먼가 잘못 됬음
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Seat.DoesNotExist:
            return Response({"message": "좌석이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["get"])
    def getseatAbout(self, request):

        try:

            room1A = Seat.objects.filter(room_type="1").filter(seat_type="A")
            room1B = Seat.objects.filter(room_type="1").filter(seat_type="B")
            room1C = Seat.objects.filter(room_type="1").filter(seat_type="C")
            room2A = Seat.objects.filter(room_type="2").filter(seat_type="A")
            room2B = Seat.objects.filter(room_type="2").filter(seat_type="B")
            room2C = Seat.objects.filter(room_type="2").filter(seat_type="C")
            room3A = Seat.objects.filter(room_type="3").filter(seat_type="A")
            room3B = Seat.objects.filter(room_type="3").filter(seat_type="B")
            room4A = Seat.objects.filter(room_type="4").filter(seat_type="A")
            room4B = Seat.objects.filter(room_type="4").filter(seat_type="B")
            room5A = Seat.objects.filter(room_type="5").filter(seat_type="A")
            room5B = Seat.objects.filter(room_type="5").filter(seat_type="B")
            room5C = Seat.objects.filter(room_type="5").filter(seat_type="C")
            room6A = Seat.objects.filter(room_type="6").filter(seat_type="A")
            room6B = Seat.objects.filter(room_type="6").filter(seat_type="B")
            room6C = Seat.objects.filter(room_type="6").filter(seat_type="C")
            room7A = Seat.objects.filter(room_type="7").filter(seat_type="A")
            room7B = Seat.objects.filter(room_type="7").filter(seat_type="B")
            room7C = Seat.objects.filter(room_type="7").filter(seat_type="C")
            room8A = Seat.objects.filter(room_type="8").filter(seat_type="A")
            room8B = Seat.objects.filter(room_type="8").filter(seat_type="B")
            room8C = Seat.objects.filter(room_type="8").filter(seat_type="C")
            room9 = Seat.objects.filter(room_type="9")
            data = [
                {
                    "room": "1",
                    "A": {
                        "whole": room1A.count(),
                        "avalible": room1A.filter(is_seat_full=False).count(),
                    },
                    "B": {
                        "whole": room1B.count(),
                        "avalible": room1B.filter(is_seat_full=False).count(),
                    },
                    "C": {
                        "whole": room1C.count(),
                        "avalible": room1C.filter(is_seat_full=False).count(),
                    },
                },
                {
                    "room": "2",
                    "A": {
                        "whole": room2A.count(),
                        "avalible": room2A.filter(is_seat_full=False).count(),
                    },
                    "B": {
                        "whole": room2B.count(),
                        "avalible": room2B.filter(is_seat_full=False).count(),
                    },
                    "C": {
                        "whole": room2C.count(),
                        "avalible": room2C.filter(is_seat_full=False).count(),
                    },
                },
                {
                    "room": "3",
                    "A": {
                        "whole": room3A.count(),
                        "avalible": room3A.filter(is_seat_full=False).count(),
                    },
                    "B": {
                        "whole": room3B.count(),
                        "avalible": room3B.filter(is_seat_full=False).count(),
                    },
                },
                {
                    "room": "4",
                    "A": {
                        "whole": room4A.count(),
                        "avalible": room4A.filter(is_seat_full=False).count(),
                    },
                    "B": {
                        "whole": room4B.count(),
                        "avalible": room4B.filter(is_seat_full=False).count(),
                    },
                },
                {
                    "room": "5",
                    "A": {
                        "whole": room5A.count(),
                        "avalible": room5A.filter(is_seat_full=False).count(),
                    },
                    "B": {
                        "whole": room5B.count(),
                        "avalible": room5B.filter(is_seat_full=False).count(),
                    },
                },
                {
                    "room": "6",
                    "A": {
                        "whole": room6A.count(),
                        "avalible": room6A.filter(is_seat_full=False).count(),
                    },
                    "B": {
                        "whole": room6B.count(),
                        "avalible": room6B.filter(is_seat_full=False).count(),
                    },
                    "C": {
                        "whole": room6C.count(),
                        "avalible": room6C.filter(is_seat_full=False).count(),
                    },
                },
                {
                    "room": "7",
                    "A": {
                        "whole": room7A.count(),
                        "avalible": room7A.filter(is_seat_full=False).count(),
                    },
                    "B": {
                        "whole": room7B.count(),
                        "avalible": room7B.filter(is_seat_full=False).count(),
                    },
                    "C": {
                        "whole": room7C.count(),
                        "avalible": room7C.filter(is_seat_full=False).count(),
                    },
                },
                {
                    "room": "8",
                    "A": {
                        "whole": room8A.count(),
                        "avalible": room8A.filter(is_seat_full=False).count(),
                    },
                    "B": {
                        "whole": room8B.count(),
                        "avalible": room8B.filter(is_seat_full=False).count(),
                    },
                    "C": {
                        "whole": room8C.count(),
                        "avalible": room8C.filter(is_seat_full=False).count(),
                    },
                },
                {
                    "room": "9",
                    "S": {
                        "whole": room9.count(),
                        "avalible": room9.filter(is_seat_full=False).count(),
                    },
                },
            ]

            if data is not None:

                json_string = json.dumps(data)
                return Response(
                    {json_string},
                    status=status.HTTP_200_OK,
                )
            else:
                # 유저가 없으면 먼가 잘못 됬음
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Seat.DoesNotExist:
            return Response({"message": "좌석이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["get"])
    def byroom(self, request):
        roomnumner = request.GET["room"]
        print(roomnumner)
        try:
            seat = Seat.objects.filter(room_type=roomnumner)
            if seat is not None:
                # 유저가 있으면
                serializer = SeatSerializer(seat, many=True)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                )
            else:
                # 유저가 없으면 먼가 잘못 됬음
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Seat.DoesNotExist:
            return Response({"message": "좌석이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
