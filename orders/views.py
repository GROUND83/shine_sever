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
        # I'mport; 아이디로 확인 가격확인

        ispaid = iamport.is_paid(response["amount"], imp_uid=imp_uid)
        # json data 로드
        customdata = json.loads(response["custom_data"])
        howManydate = len(customdata["menudata"])
        phone = customdata["phone"]
        order = Order.objects.get(merchant_uid=merchant_uid)
        # paid, 금액동일
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
                        lat = "원창"
                        lng = "원창"
                        # deliveryStartdate = customdata["deliveryStartdate"]
                        menudata = customdata["menudata"]
                        fork = customdata["fork"]
                        # coupon = customdata["coupon"]
                        deliveryDate = datetime.datetime.strptime(
                            customdata["deliveryStartdate"], "%Y-%m-%d"
                        ).date()

                        # 오더생성

                        order.imp_uid = response["imp_uid"]
                        order.orderType = orderType
                        order.pg_provider = response["pg_provider"]
                        # order.status = 'paid'
                        # 결재금액
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
                        # PG사 거래고유번호
                        order.pg_tid = response["pg_tid"]
                        order.receipt_url = response["receipt_url"]
                        order.status = response["status"]
                        order.user = User.objects.get(phone=phone)
                        order.save()

                        if importstatus == "paid":
                            order = Order.objects.get(merchant_uid=merchant_uid)
                            for idx, data in enumerate(customdata["menudata"]):
                                Orderdata.objects.create(
                                    orderDataType="주문",
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
                                    deliver="원창",
                                )
                            # 쿠폰 확인
                            #
                            order = Order.objects.get(merchant_uid=merchant_uid)
                            order.done = True
                            order.save()

                            data = {
                                "phone_number": phone,
                                "date": deliveryDate,
                            }
                            # 처음주문 카카오발송
                            sendKakao = firstOrder(data=data)

                            # 텔레그렘으로 바꿀껏 관리자 알림
                            send_telegram(
                                text=f"주문자:{orderer}\n주문타입:{orderType}\n{howManydate}일\n총수량:{orderAmount}개\n배송시작일:{deliveryDate}\n주문이 추가되었습니다."
                            )

                            orderType = customdata["orderType"]
                            phone = customdata["phone"]
                            orderAmount = customdata["orderAmount"]
                            # 알람추가 - 입금완료
                            alram = Alram.objects.create(
                                alramtype="order",
                                headings="주문이 완료되었습니다.",
                                subtitle=f"{orderType} {howManydate}일 총{orderAmount}개 주문 완료 되었습니다",
                                contents="정성껏 만들어 배송하겠습니다. ~ 😀😀",
                                itemid=merchant_uid,
                                readed=False,
                            )
                            alram.to.add(User.objects.get(phone=phone))
                            if sendKakao is True:
                                return Response("카카오 메세지가 정상 발송되었습니다.")
                            else:
                                return Response("카카오 메세지 발송 실폐")
                    else:
                        return Response("오더가 없습니다.")
        # 켄슬 (결재취소,부분취소포함)
        elif importstatus == "cancelled":
            order.status = "cancelled"
            order.save()
            orderType = customdata["orderType"]
            phone = customdata["phone"]
            orderAmount = customdata["orderAmount"]
            data = {
                "phone_number": phone,
            }
            # 카카오알림
            callendOrder(data=data)
            # 알람추가
            alram = Alram.objects.create(
                alramtype="order",
                headings="주문 취소가 완료 되었습니다.",
                subtitle=f"{merchant_uid}건의 주문이 취소되었습니다.",
                contents="앞으로 더욱 더 노력하겠습니다.감사합니다.😀",
                itemid=merchant_uid,
                readed=False,
            )
            alram.to.add(User.objects.get(phone=phone))
            return Response("done cancelled")
        # 결제실페
        elif importstatus == "failed":
            order = Order.objects.get(merchant_uid=merchant_uid)
            order.delete()
            # 알람추가
            phone = customdata["phone"]
            alram = Alram.objects.create(
                alramtype="order",
                headings="주문이 실폐하였습니다.",
                subtitle=f"{merchant_uid}건의 주문이 실페하였습니다.",
                contents="주문정보를 확인하시고 다시 한번 주문 부탁드립니다.~ 😀😀",
                itemid=merchant_uid,
                readed=False,
            )
            alram.to.add(
                User.objects.get(phone=phone),
            )
            return Response("done failed")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
