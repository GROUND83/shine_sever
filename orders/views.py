from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Order
from users.models import User
from seats.models import Seat
from .permissions import IsSelf
import datetime
from random import randint
from orders.serializers import OrderSerializer

# Create your views here.
class OrdersViewSet(ModelViewSet):
    queryset = Order.objects.all()
    # serializer_class = UserSerializer
    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser | IsSelf]
        if self.action == "retrieve":
            permission_classes = [IsSelf]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"])
    def mid(self, request):
        # imp_uid = request.data["imp_uid"]
        # merchant_uid = request.data["merchant_uid"]
        phone = request.data.get("phone")
        seatname = request.data.get("seatname")
        seat = Seat.objects.get(seat_title=seatname)
        user = User.objects.get(phone=phone)

        date = datetime.datetime.now()
        nowdata = date.strftime("%Y%m%d")
        random = str(randint(100000, 999999))
        mid = f"ORD{user.pk}-{nowdata}{random}"
        order = Order.objects.create(merchant_uid=mid, user=user, seat=seat)
        serialrizer = OrderSerializer(order).data
        return Response(data=serialrizer)

    @action(detail=False, methods=["post"])
    def importcallback(self, request):
        user_ip = request.META["HTTP_X_FORWARDED_FOR"]

        iamport = Iamport(
            imp_key=os.environ.get("IMPORT_REST_API"),
            imp_secret=os.environ.get("IMPORT_REST_API_SECRET"),
        )
        imp_uid = request.data.get("imp_uid")
        merchant_uid = request.data.get("merchant_uid")
        importstatus = request.data.get("status")
        response = iamport.find(imp_uid=imp_uid)
        # print(response)
        # I'mport; ???????????? ?????? ????????????

        ispaid = iamport.is_paid(response["amount"], imp_uid=imp_uid)
        # json data ??????
        customdata = json.loads(response["custom_data"])
        howManydate = len(customdata["menudata"])
        phone = customdata["phone"]
        order = Order.objects.get(merchant_uid=merchant_uid)
        # paid, ????????????
        if ispaid is True and importstatus == "paid":
            for ip in settings.ALLOWED_HOSTS:
                if ip == user_ip:
                    if order is not None:
                        orderType = customdata["orderType"]
                        # orderName = customdata["orderName"]
                        orderAmount = customdata["orderAmount"]
                        orderer = customdata["orderer"]
                        phone = customdata["phone"]
                        request = customdata["request"]

                        deliveryAddress = customdata["deliveryAddress"]
                        address1 = customdata["address1"]
                        etc = customdata["etc"]
                        lat = "??????"
                        lng = "??????"
                        # deliveryStartdate = customdata["deliveryStartdate"]
                        menudata = customdata["menudata"]
                        fork = customdata["fork"]
                        # coupon = customdata["coupon"]
                        deliveryDate = datetime.datetime.strptime(
                            customdata["deliveryStartdate"], "%Y-%m-%d"
                        ).date()

                        # ????????????

                        order.imp_uid = response["imp_uid"]
                        order.orderType = orderType
                        order.pg_provider = response["pg_provider"]
                        # order.status = 'paid'
                        # ????????????
                        order.amount = response["amount"]
                        order.buyer_addr = deliveryAddress
                        order.room = address1
                        order.etc = etc
                        order.viaX = lng
                        order.viaY = lat
                        order.buyer_email = response["buyer_email"]
                        order.buyer_name = response["buyer_name"]
                        order.buyer_tel = response["buyer_tel"]
                        order.deriverynote = request
                        order.customdata = menudata
                        order.deliveryDate = deliveryDate
                        order.fork = fork
                        order.howmany = orderAmount
                        order.howmanyDate = len(customdata["menudata"])
                        # unix timestamp
                        order.paid_at = response["paid_at"]
                        # PG??? ??????????????????
                        order.pg_tid = response["pg_tid"]
                        order.receipt_url = response["receipt_url"]
                        order.status = response["status"]
                        order.user = User.objects.get(phone=phone)
                        order.save()

                        if importstatus == "paid":
                            order = Order.objects.get(merchant_uid=merchant_uid)
                            for idx, data in enumerate(customdata["menudata"]):
                                Orderdata.objects.create(
                                    orderDataType="??????",
                                    merchant_uid=merchant_uid,
                                    imp_uid=response["imp_uid"],
                                    date=data["date"],
                                    menu=data["menu"],
                                    num=idx + 1,
                                    howmany=orderAmount,
                                    menuAmount=data["amount"],
                                    orderSize=data["size"],
                                    orderType=orderType,
                                    phone=phone,
                                    buyer_addr=deliveryAddress,
                                    room=address1,
                                    etc=etc,
                                    deriverynote=request,
                                    orderer=orderer,
                                    viaX=lng,
                                    viaY=lat,
                                    fork=fork,
                                    deliver="??????",
                                )
                            # ?????? ??????
                            #
                            order = Order.objects.get(merchant_uid=merchant_uid)
                            order.done = True
                            order.save()

                            data = {
                                "phone_number": phone,
                                "date": deliveryDate,
                            }
                            # ???????????? ???????????????
                            sendKakao = firstOrder(data=data)

                            # ?????????????????? ????????? ????????? ??????
                            send_telegram(
                                text=f"?????????:{orderer}\n????????????:{orderType}\n{howManydate}???\n?????????:{orderAmount}???\n???????????????:{deliveryDate}\n????????? ?????????????????????."
                            )

                            orderType = customdata["orderType"]
                            phone = customdata["phone"]
                            orderAmount = customdata["orderAmount"]
                            # ???????????? - ????????????
                            alram = Alram.objects.create(
                                alramtype="order",
                                headings="????????? ?????????????????????.",
                                subtitle=f"{orderType} {howManydate}??? ???{orderAmount}??? ?????? ?????? ???????????????",
                                contents="????????? ????????? ?????????????????????. ~ ????????",
                                itemid=merchant_uid,
                                readed=False,
                            )
                            alram.to.add(User.objects.get(phone=phone))
                            if sendKakao is True:
                                return Response("????????? ???????????? ?????? ?????????????????????.")
                            else:
                                return Response("????????? ????????? ?????? ??????")
                    else:
                        return Response("????????? ????????????.")
        # ?????? (????????????,??????????????????)
        elif importstatus == "cancelled":
            order.status = "cancelled"
            order.save()
            orderType = customdata["orderType"]
            phone = customdata["phone"]
            orderAmount = customdata["orderAmount"]
            data = {
                "phone_number": phone,
            }
            # ???????????????
            callendOrder(data=data)
            # ????????????
            alram = Alram.objects.create(
                alramtype="order",
                headings="?????? ????????? ?????? ???????????????.",
                subtitle=f"{merchant_uid}?????? ????????? ?????????????????????.",
                contents="????????? ?????? ??? ?????????????????????.???????????????.????",
                itemid=merchant_uid,
                readed=False,
            )
            alram.to.add(User.objects.get(phone=phone))
            return Response("done cancelled")
        # ????????????
        elif importstatus == "failed":
            order = Order.objects.get(merchant_uid=merchant_uid)
            order.delete()
            # ????????????
            phone = customdata["phone"]
            alram = Alram.objects.create(
                alramtype="order",
                headings="????????? ?????????????????????.",
                subtitle=f"{merchant_uid}?????? ????????? ?????????????????????.",
                contents="??????????????? ??????????????? ?????? ?????? ?????? ??????????????????.~ ????????",
                itemid=merchant_uid,
                readed=False,
            )
            alram.to.add(
                User.objects.get(phone=phone),
            )
            return Response("done failed")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
