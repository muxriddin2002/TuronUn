from asyncio.log import logger
import pytz
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from home.models import *
from .serializers import *
from datetime import datetime, timedelta
from django.db.models import Q
#sms
from home.bugalter.functions import sendSmsOneContact
from django.utils import timezone
from decimal import *


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination


    def list(self, request):
        user_id = request.GET['user_id']
        user = Employee.objects.get(id=user_id)
        search = request.GET.get('item')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        month_ago = datetime.today()-timedelta(days=30)
        if from_date and to_date:
            orders = Order.objects.filter(date__range=[from_date, to_date], status__in=[3, 4], tegirmon=user.tegirmon ).order_by('-id')
        elif from_date:
            orders = Order.objects.filter(date__gte=from_date,status__in=[3, 4], tegirmon=user.tegirmon).order_by('-id')
        elif to_date:
            orders = Order.objects.filter(Q(date__lte=to_date) & Q(status__in=[3, 4]) , tegirmon=user.tegirmon).order_by('-id')
        elif from_date and to_date:
            orders = Order.objects.filter(date__range=[from_date, to_date], 
                status__in=[3, 4], tegirmon=user.tegirmon).order_by('-id')
        else:
            orders = Order.objects.filter(date__gte=month_ago.date(), tegirmon=user.tegirmon, status__in=[3, 4]).order_by('-id')
        checked_basket_ids = []
        for order in orders:
            for basket in order.baskets.all():
                if user.type == 15:
                    if basket.product:
                        if basket.product.product.type.name == 'Yem':
                            checked_basket_ids.append(basket.pk)
                if user.type == 16:
                    if basket.product:
                        if basket.product.product.type.name == 'Un':
                            checked_basket_ids.append(basket.pk)
                if user.type in [6 ,20]:
                    if basket.product:
                        checked_basket_ids.append(basket.pk)

        queryset = Order.objects.filter(baskets__id__in=checked_basket_ids).distinct().order_by('-id')

        def check_date_str(search):
            try:
                datetime.strptime(search, "%d-%m-%Y").date()
                return True
            except Exception:
                return False

        if search != "":
            if check_date_str(search) == True:
                queryset = queryset.filter(date=search)
            else:
                queryset = queryset.filter(Q(customer__name__icontains=search) | Q(car_number=search) |Q(driver_phone=search))
        else:
            queryset = Order.objects.filter(baskets__id__in=checked_basket_ids).distinct().order_by('-id')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class TurnofCarsViewset(viewsets.ModelViewSet):
    queryset = TurnofCars.objects.all()
    serializer_class = TurnofCarsSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        search = request.GET.get('item')
        queryset = self.queryset.filter(status=2)
        def check_date_str(search):
            try:
                datetime.strptime(search, "%d-%m-%Y")
                return True
            except ValueError:
                return False
        if search != "":
            if check_date_str(search) == True:
                queryset = queryset.filter(order__date=search)
            else:
                queryset = queryset.filter(Q(order__customer__name__icontains=search) | Q(order__car_number=search) |Q(order__driver_phone=search))
        else:
            queryset = TurnofCars.objects.filter(status=2)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def load_basket(request):
    bask = Basket.objects.all()
    for i in bask:
        i.load = True
        i.save()
    return Response({"data": "boldi"})


@api_view(['GET'])
def get_order(request):
    # sourcery skip: for-append-to-extend, merge-duplicate-blocks, merge-nested-ifs, merge-repeated-ifs, swap-nested-ifs, switch
    try:
        user_id = request.GET.get("user_id")
        user = Employee.objects.get(id=user_id)
        if user.type in [6,20]:
            orders = Order.objects.filter(status__in=[1, 2], date__gte=datetime.now() - timedelta(days=30), tegirmon=user.tegirmon)
        else:
            orders = Order.objects.filter(status=2, date__gte=datetime.now() - timedelta(days=30), tegirmon=user.tegirmon)
        checked_basket_ids = []
        for order in orders:
            for basket in order.baskets.all():
                if user.type == 15: #yem
                    if basket.product:
                        if basket.product.product.type.name == 'Yem':
                            checked_basket_ids.append(basket.pk)
                if user.type == 16: #un
                    if basket.product:
                        if basket.product.product.type.name == 'Un':
                                    checked_basket_ids.append(basket.pk)
                if user.type in [6, 20] :# asosiy un
                    if basket.product:
                            checked_basket_ids.append(basket.pk)

        queryset = Order.objects.filter(baskets__in=checked_basket_ids, baskets__product__tegirmon=user.tegirmon, tegirmon=user.tegirmon).distinct()
        dat = []
        for i in queryset:
            dt = {
                'id': i.id,
                "mijoz": i.customer.name,
                "status": i.status,
                "mashina nomeri": i.car_number,
                "tel nomer": i.driver_phone,
                "sana": timezone.localtime(i.date_time, pytz.timezone('Asia/Tashkent')).strftime("%d-%m-%Y %H:%M:%S"),
            }
            dat.append(dt)
        data = {
            "success": True,
            "data": dat,
        }

    except Exception as err:
        data = {"success": False, "error": f"{err}"}

    return Response(data)


@api_view(['GET'])
def get_basket(request):
    try:
        user_id = request.GET.get("user_id")
        order_id = request.GET.get("order_id")
        user = Employee.objects.get(id=user_id)

        order = Order.objects.get(id=order_id)
        if user.type == 15:
            baskets = order.baskets.filter(load=False, product__product__type__name__icontains="Yem")
            dat = []
            for i in baskets:
                dt = {
                    'id': i.id,
                    'maxsulot': i.product.product.name,
                    'maxsulot kodi': i.product.product.pr_code,
                    'qop soni': float(i.hajmi),
                    'umumiy summasi': float(i.price) * float(i.hajmi)
                }
                dat.append(dt)
            data = {
                "success": True,
                "data": dat,
            }
        if user.type == 16:
            baskets = order.baskets.filter(load=False, product__product__type__name__icontains="Un")
            dat = []
            for i in baskets:
                dt = {
                    'id': i.id,
                    'maxsulot': i.product.product.name,
                    'maxsulot kodi': i.product.product.pr_code,
                    'qop soni': float(i.hajmi),
                    'umumiy summasi': float(i.price) * float(i.hajmi)
                }
                dat.append(dt)
            data = {
                "success": True,
                "data": dat,
            }
        if user.type in [6, 20]: #asosiy omborchi
            baskets = order.baskets.filter(load=False)
            dat = []
            for i in baskets:
                dt = {
                    'id': i.id,
                    'maxsulot': i.product.product.name,
                    'maxsulot kodi': i.product.product.pr_code,
                    'qop soni': float(i.hajmi),
                    'umumiy summasi': float(i.price) * float(i.hajmi)
                }
                dat.append(dt)
            data = {
                "success": True,
                "data": dat,
            }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(['GET'])
def get_basket_product(request):
    try:
        user_id = request.GET.get("user_id")
        order_id = request.GET.get("order_id")
        user = Employee.objects.get(id=user_id)
        order = Order.objects.get(id=order_id)

        if user.type == 15:
            baskets = order.baskets.filter(product__product__type__name__icontains="Yem", tegirmon=user.tegirmon)
            dat = []
            for i in baskets:
                dt = {
                    'id': i.id,
                    'maxsulot': i.product.product.name,
                    'maxsulot kodi': i.product.product.pr_code,
                    "status": i.load,
                    'qop soni': float(i.hajmi),
                    'umumiy miqdori': float(i.miqdori) * float(i.hajmi)
                }
                dat.append(dt)
            data = {
                "success": True,
                "data": dat,
            }
        if user.type == 16:
            baskets = order.baskets.filter(product__product__type__name__icontains="Un", tegirmon=user.tegirmon)
            dat = []
            for i in baskets:
                dt = {
                    'id': i.id,
                    'maxsulot': i.product.product.name,
                    'maxsulot kodi': i.product.product.pr_code,
                    "status": i.load,
                    'qop soni': float(i.hajmi),
                    'umumiy miqdori': float(i.miqdori) * float(i.hajmi)
                }
                dat.append(dt)
            data = {
                "success": True,
                "data": dat,
            }
        if user.type in [6, 20]:
            baskets = order.baskets.filter(tegirmon=user.tegirmon)
            dat = []
            for i in baskets:
                dt = {
                    'id': i.id,
                    'maxsulot': i.product.product.name,
                    'maxsulot kodi': i.product.product.pr_code,
                    "status": i.load,
                    'qop soni': float(i.hajmi),
                    'umumiy miqdori': float(i.miqdori) * float(i.hajmi)
                }
                dat.append(dt)
            data = {
                "success": True,
                "data": dat,
            }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(['GET'])
def get_qaytuv(request):
    try:
        user_id = request.GET.get("user_id")
        user = Employee.objects.get(id=user_id)
        baskets_ids = Qaytuv.objects.filter(status=1).values_list(
            'baskets').distinct()
        basket_list = [basket_id[0] for basket_id in baskets_ids]
        qaytuvs = Qaytuv.objects.filter(baskets__in=basket_list, baskets__product__tegirmon=user.tegirmon).distinct()
        ser = QaytuvSerializer(qaytuvs, many=True)

        dat = []
        for i in qaytuvs:
            dt = {
                'id': i.id,
                "mijoz": i.customer.name,
                # "mashina nomeri": i.car_number,
                "tel nomer": i.customer.phone,
                "sana": i.date.strftime("%d-%m-%Y"),
            }
            dat.append(dt)
        data = {
            "success": True,
            "data": dat,
        }

    except Exception as err:
        data = {'success': False, 'error': f'{err}'}
    return Response(data)

@api_view(['GET'])
def get_qaytuv_basket(request):
    try:
        user_id = request.GET.get("user_id")
        qaytuv_id = request.GET.get("qaytuv_id")
        user = Employee.objects.get(id=user_id)

        qaytuv = Qaytuv.objects.get(id=qaytuv_id)
        baskets = qaytuv.baskets.filter(load=False)
        basket = BasketQaytuvSerializer(baskets, many=True)

        dat = []
        for i in baskets:
            dt = {
                'id': i.id,
                'maxsulot': i.product.product.name,
                # 'miqdori': i.miqdori,
                'hajmi': i.hajmi,
                'umumiy miqdori': i.miqdori * i.hajmi
            }
            dat.append(dt)
        data = {
            "success": True,
            "data": dat,
        }


    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(['GET'])
def get_load_qaytuv_basket(request):
    try:
        user_id = request.GET.get("user_id")
        qaytuv_id = request.GET.get("qaytuv_id")
        user = Employee.objects.get(id=user_id)

        qaytuv = Qaytuv.objects.get(id=qaytuv_id)
        baskets = qaytuv.baskets.filter(load=True)

        basket = BasketQaytuvSerializer(baskets, many=True)

        dat = []
        for i in baskets:
            dt = {
                'id': i.id,
                'maxsulot': i.product.product.name,
                'tegirmon': user.tegirmon.name,
                'qopsoni': float(i.hajmi),
                'sana': qaytuv.date.strftime("%d-%m-%Y"),
            }
            dat.append(dt)
        data = {
            "success": True,
            "data": dat,
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(["POST"])
def load_qaytuv_basket(request):
    try:
        bask_id = request.data.getlist("bask_id")
        qaytuv_id = request.data.get("qaytuv_id")
        yuklovchi = request.data.get("brigada")

        qaytuv = Qaytuv.objects.get(id=qaytuv_id)

        brigada = Brigada.objects.get(id=yuklovchi)

        for i in bask_id:
            bask = BasketQaytuv.objects.get(id=i)
            bask.load = True
            bask.brigada = brigada
            bask.save()

        if qaytuv.baskets.filter(load=True).count() == qaytuv.baskets.all().count():
            qaytuv.status = '2'
            qaytuv.save()

        data = {
            "success": True,
            "message": "Muvaffaqiyatli yuklandi!",
        }

    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

# Basketlarni Mashinaga yuklash uchun
@api_view(["POST"])
def load_order_basket(request):
    try:
        bask_id = request.data.get("bask_id")
        order_id = request.data.get("order_id")
        bask = Basket.objects.get(id=bask_id)
        logger.info(f'{bask} load trued')
        order = Order.objects.get(id=order_id)
        counter = BaskCounter.objects.get(basket=bask)
        counter.miqdori -= bask.hajmi
        counter.save()

        if counter.miqdori <= 0:
            bask.load = True
            bask.save()

        status = order.baskets.filter(load=True).count() == order.baskets.all().count()
        data = {
            "success": True,
            "message": "Muvaffaqiyatli yuklandi!",
            "status": status,
            "counter": counter.miqdori,
        }

    except Exception as err:
        data = {'success': False, 'error': f'{err}'}
    return Response(data)

@api_view(['POST'])
def add_brigada_tobasket(request):
    try:
        bask_id = request.data.get('bask_id')
        brigada = request.data.get('brigada')
        basket = Basket.objects.get(id=bask_id)
        br = Brigada.objects.get(id=brigada)
        basket.brigada = br
        basket.save()
        data = {
            "success": True,
            "message": "Muvaffaqiyatli qoshildi!",
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(['POST'])
def send_order(request):
    try:
        order_id = request.data.get("id")
        img = request.FILES['img']
        order = Order.objects.get(id=order_id)
        if order.baskets.filter(load=False).count() == 0:
            order.img = img
            order.status = 3
            order.save()
            data = {
                "success": True,
                "message": "Muvaffaqiyatli yuklandi!",
            }
        else:
            data = {
                "success": True,
                "message": "Buyurtma to'liq yuklanmadi!",
            }

    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(['GET'])
def get_brigada(request):
    try:
        brigada = Brigada.objects.all()
        bri = BrigadaSerializer(brigada, many=True)

        data = {
            "success": True,
            "data": bri.data,
        }

    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

# Security
@api_view(["GET"])
def get_order_to_give_turn(request):  # sourcery skip: use-named-expression
    try:
        user_id = request.GET.get('user_id')
        if user_id:
            user = Employee.objects.get(id=user_id)
            order = Order.objects.filter(status=1, tegirmon_id=user.tegirmon.id)
        else:
            order = Order.objects.filter(status=1)

        ord = OrderIdMijozSanaSerializer(order, many=True)

        dat = []
        for i in order:
            dt = {
                'id': i.id,
                'mijoz': i.customer.name,
                'sana':timezone.localtime(i.date_time, pytz.timezone('Asia/Tashkent')).strftime("%d-%m-%Y %H:%M:%S"),
            }
            dat.append(dt)

        data = {
            "success": True,
            "data": dat,
        }

    except Exception as err:
        data = {"success": False, "error": f"{err}"}

    return Response(data)

# reject order
@api_view(["GET"])
def reject_order(request):
    try:
        order_id = request.GET.get("order_id")
        order = Order.objects.get(id=order_id)
        order.status = 5
        order.save()

        data = {
            "success": True,
            "message": "Muvaffaqiyatli qaytarildi!",
        }

    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

# reject turned order
@api_view(["POST"])
def reject_turned_order(request):
    try:
        tash = request.data['status']
        turn_id = request.data['turn_id']
        if tash == 0:
            turn = TurnofCars.objects.get(id=turn_id)
        if tash == 1:
            turn = TurnofCarsofTashkent.objects.get(id=turn_id)
        turn.status = 4
        order = turn.order
        turn.waiting = True
        turn.save()
        order.status = 4
        order.save()
        turn.save()
        data = {"success": True, "message": "Mashinasi qaytarildi!"}

    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(['GET'])
def get_basketforsecurity(request):
    try:
        order_id = request.GET.get("order_id")
        order = Order.objects.get(id=order_id)
        baskets = order.baskets.filter(load=False)
        basket = BasketSerializer(baskets, many=True)
        dat = []
        for i in baskets:
            dt = {
                'basket_id': i.id,
                'maxsulot': i.product.product.name,
                'maxsulot_turi': i.product.product.type.name,
                'qop_soni': float(i.hajmi),
                'umumiy_massa': float(i.miqdori)
            }
            dat.append(dt)
        data = {
            "success": True,
            "data": dat,
        }

    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(['POST'])
def add_turn(request):
    try:
        tash = request.data.get('status')
        order_id = request.data.get("order_id")
        turn = request.data.get("turn")
        car_number = request.data.get("car_number")
        driver_phone = request.data.get("driver_phone")
        order = Order.objects.get(id=order_id)
        order.turned_date = timezone.now()
        order.driver_phone = driver_phone
        order.car_number = car_number
        order.status = 2
        order.save()
        if tash == 0:
            TurnofCars.objects.create(order=order, turn=turn, status=1)
        if tash == 1:
            TurnofCarsofTashkent.objects.create(order=order, turn=turn, status=1)
        sendSmsOneContact(
            f'+998{driver_phone}',
            f"Aссалому алайкум! Турон cомпанйга хуш келибсиз! Мувоффақиятли навбатга олинди. Навбат рақамингиз: {turn}",
        )


        data = {
            "success": True,
            "message": "Muvoffaqiyatli navbatga olindi"
        }

    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(['POST'])
def add_turn_and_enter_car(request):
    try:
        tash = request.data.get('status')
        order_id = request.data.get("order_id")
        turn = request.data.get("turn")
        car_number = request.data.get("car_number")
        driver_phone = request.data.get("driver_phone")
        order = Order.objects.get(id=order_id)
        order.turned_date = timezone.now()
        order.entered_date = timezone.now()
        order.driver_phone = driver_phone
        order.car_number = car_number
        order.status = 2
        order.save()
        if tash == 0:
            turn = TurnofCars.objects.create(order=order, turn=turn, status=1)
        if tash == 1:
            turn = TurnofCarsofTashkent.objects.create(order=order, turn=turn, status=1)
        turn.status = 2
        turn.waiting = False
        turn.save()
        driver_phone = turn.order.driver_phone
        sendSmsOneContact(
            f'+998{driver_phone}',
            "Aссалом алайкум! Сизнинг навбатингиз келди. Турон cомпанй ",
        )

        data = {
            "success": True,
            "message": "Muvoffaqiyatli navbatga olindi"
        }

    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(['POST'])
def enter_car(request):
    try:
        tash = request.data['status']
        turn_id = request.data['turn_id']
        if tash == 0:
            turn = TurnofCars.objects.get(id=turn_id)
        if tash == 1:
            turn = TurnofCarsofTashkent.objects.get(id=turn_id)
        order = turn.order
        turn.status = 2
        turn.waiting = False
        turn.save()
        order.entered_date = timezone.now()
        order.save()
        driver_phone = turn.order.driver_phone
        sendSmsOneContact(
            f'+998{driver_phone}',
            "Aссалом алайкум! Сизнинг навбатингиз келди. Турон cомпанй ",
        )

        data = {
            "success": True,
            "message": "Aссалом алайкум! Сизнинг навбатингиз келди. Турон cомпанй "
        }

    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(['GET'])
def get_turns(request):
    try:
        turnsactive = TurnofCars.objects.filter(status=1)
        turnsoftashkentactive = TurnofCarsofTashkent.objects.filter(status=1)
        datactive = []
        dataactoshkent = []

        turnsload = TurnofCars.objects.filter(status=2)
        turnsoftashkentload = TurnofCarsofTashkent.objects.filter(status=2)

        dataload = []
        dataloadtoshkent = []

        for i in turnsactive:
            dt = {
                'id': i.id,
                'mijoz': i.order.customer.name,
                'car_number': i.order.car_number,
                'driver_phone': i.order.driver_phone,
                'date': i.date.strftime("%d-%m-%Y"),
                'turn': i.turn,
            }
            datactive.append(dt)
        for i in turnsoftashkentactive:
            dt = {
                'id': i.id,
                'mijoz': i.order.customer.name,
                'car_number': i.order.car_number,
                'driver_phone': i.order.driver_phone,
                'date': i.date.strftime("%d-%m-%Y"),
                'turn': i.turn,
            }
            dataactoshkent.append(dt)

        for i in turnsload:
            dt = {
                'id': i.id,
                'mijoz': i.order.customer.name,
                'car_number': i.order.car_number,
                'driver_phone': i.order.driver_phone,
                'date': i.date.strftime("%d-%m-%Y"),
                'turn': i.turn,
            }
            dataload.append(dt)
        for i in turnsoftashkentload:
            dt = {
                'id': i.id,
                'mijoz': i.order.customer.name,
                'car_number': i.order.car_number,
                'driver_phone': i.order.driver_phone,
                'date': i.date.strftime("%d-%m-%Y"),
                'turn': i.turn,
            }
            dataloadtoshkent.append(dt)

        query = {
            "activeviloyat": datactive,
            "activetashkent": dataactoshkent,
            "loadingviloyat": dataload,
            "loadingtashkent": dataloadtoshkent,
        }
        data = {
            "success": True,
            "data": query
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}

    return Response(data)

@api_view(['GET'])
def get_active_turn(request):
    try:
        if user_id := request.GET.get('user_id'):
            user = Employee.objects.get(id=user_id)
            turnsactive = TurnofCars.objects.filter(status=1, order__tegirmon_id = user.tegirmon.id)
            turnsoftashkentactive = TurnofCarsofTashkent.objects.filter(status=1, order__tegirmon_id = user.tegirmon.id)
        else:
            turnsactive = TurnofCars.objects.filter(status=1)
            turnsoftashkentactive = TurnofCarsofTashkent.objects.filter(status=1)
        datactive = []
        dataactoshkent = []

        for i in turnsactive:
            dt = {
                'id': i.id,
                'mijoz': i.order.customer.name,
                'car_number': i.order.car_number,
                'driver_phone': i.order.driver_phone,
                'date': timezone.localtime(i.date, pytz.timezone('Asia/Tashkent')).strftime("%d-%m-%Y %H:%M:%S"),
                'turn': i.turn,
                'status': 0,
            }
            datactive.append(dt)
        for i in turnsoftashkentactive:
            dt = {
                'id': i.id,
                'mijoz': i.order.customer.name,
                'car_number': i.order.car_number,
                'driver_phone': i.order.driver_phone,
                'date': timezone.localtime(i.date, pytz.timezone('Asia/Tashkent')).strftime("%d-%m-%Y %H:%M:%S"),
                'turn': i.turn,
                'status': 1,
            }
            dataactoshkent.append(dt)


        query = {
            "activeviloyat": datactive,
            "activetashkent": dataactoshkent,
        }
        data = {
            "success": True,
            "data": query
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}

    return Response(data)

@api_view(['GET'])
def get_loading_turn(request):
    try:
        user_id = request.GET.get('user_id')
        user = Employee.objects.get(id=user_id)
        turnsload = TurnofCars.objects.filter(status=2, order__tegirmon_id = user.tegirmon.id)
        turnsoftashkentload = TurnofCarsofTashkent.objects.filter(status=2, order__tegirmon_id = user.tegirmon.id)


        dataload = []
        dataloadtoshkent = []

        for i in turnsload:
            dt = {
                'id': i.id,
                'mijoz': i.order.customer.name,
                'car_number': i.order.car_number,
                'driver_phone': i.order.driver_phone,
                'date': timezone.localtime(i.date, pytz.timezone('Asia/Tashkent')).strftime("%d-%m-%Y %H:%M:%S"),
                'turn': i.turn,
                'status': 0,
            }
            dataload.append(dt)
        for i in turnsoftashkentload:
            dt = {
                'id': i.id,
                'mijoz': i.order.customer.name,
                'car_number': i.order.car_number,
                'driver_phone': i.order.driver_phone,
                'date': timezone.localtime(i.date, pytz.timezone('Asia/Tashkent')).strftime("%d-%m-%Y %H:%M:%S"),
                'turn': i.turn,
                'status': 1,
            }
            dataloadtoshkent.append(dt)

        query = {
            "loadingviloyat": dataload,
            "loadingtashkent": dataloadtoshkent,
        }
        data = {
            "success": True,
            "data": query
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(['GET'])
def get_passive_turn(request):
    try:
        user_id = request.GET.get('user_id')
        user = Employee.objects.get(id=user_id)
        one_month_ago = timezone.now() - timedelta(days=30)
        turnsload = TurnofCars.objects.filter(status=3, order__tegirmon_id = user.tegirmon.id, date__gt=one_month_ago.date()).order_by('-date')
        turnsoftashkentload = TurnofCarsofTashkent.objects.filter(status=3, order__tegirmon_id = user.tegirmon.id, date__gt=one_month_ago.date()).order_by('-date')


        dataload = []
        dataloadtoshkent = []

        for i in turnsload:
            dt = {
                'id': i.id,
                'mijoz': i.order.customer.name,
                'car_number': i.order.car_number,
                'driver_phone': i.order.driver_phone,
                'date': i.date.strftime("%d-%m-%Y %H:%M:%S"),
                'turn': i.turn,
                'status': 0,
            }
            dataload.append(dt)
        for i in turnsoftashkentload:
            dt = {
                'id': i.id,
                'mijoz': i.order.customer.name,
                'car_number': i.order.car_number,
                'driver_phone': i.order.driver_phone,
                'date': i.date.strftime("%d-%m-%Y %H:%M:%S"),
                'turn': i.turn,
                'status': 1,
            }
            dataloadtoshkent.append(dt)

        query = {
            "loadingviloyat": dataload,
            "loadingtashkent": dataloadtoshkent,
        }
        data = {
            "success": True,
            "data": query
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}

    return Response(data)

@api_view(['GET'])
def get_turn(request):
    try:
        turnoftash = TurnofCarsofTashkent.objects.filter(status=2).first()
        turns = TurnofCars.objects.filter(status=2).first()
        if turns is None:
            data = {
                "message": "Hozirda navbatda mashina yoq"
            }
        else:
            data = {
                'id': turns.id,
                'mijoz': turns.order.customer.name,
                'car_number': turns.order.car_number,
                'driver_phone': turns.order.driver_phone,
                'date': turns.date.strftime("%d-%m-%Y"),
                'turn': turns.turn,
            }
        if turnoftash is None:
            datatashkent = {
                "message": "Hozirda navbatda mashina yoq"
            }
        else:
            datatashkent = {
                'id': turnoftash.id,
                'mijoz': turnoftash.order.customer.name,
                'car_number': turnoftash.order.car_number,
                'driver_phone': turnoftash.order.driver_phone,
                'date': turnoftash.date.strftime("%d-%m-%Y"),
                'turn': turnoftash.turn,
            }
        query = {
            "data": data,
            "datatashkent": datatashkent,
        }
        data = {
            "success": True,
            "data": query,
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }

    return Response(data)

@api_view(['GET'])
def get_all_turn(request):
    try:
        turnoftash = TurnofCarsofTashkent.objects.filter(waiting=False)
        turns = TurnofCars.objects.filter(waiting=False)
        if turns is None:
            data = {
                "message": "Hozirda navbatda mashina yoq"
            }
        else:
            data = [{
                    'id': turn.id,
                    'mijoz': turn.order.customer.name,
                    'car_number': turn.order.car_number,
                    'driver_phone': turn.order.driver_phone,
                    'date': turn.date.strftime("%d-%m-%Y"),
                    'turn': turn.turn,
                } for turn in turns]
        if turnoftash is None:
            datatashkent = {
                "message": "Hozirda navbatda mashina yoq"
            }
        else:
            datatashkent = [{
                    'id': turn.id,
                    'mijoz': turn.order.customer.name,
                    'car_number': turn.order.car_number,
                    'driver_phone': turn.order.driver_phone,
                    'date': turn.date.strftime("%d-%m-%Y"),
                    'turn': turn.turn,
                } for turn in turnoftash]
        query = {
            "data": data,
            "datatashkent": datatashkent,
        }
        data = {
            "success": True,
            "data": query,
        }
    except Exception as err:
        data = {'success': False, 'error': '{}'.format(err)}
    return Response(data)

@api_view(['GET'])
def get_all_waiting(request):
    try:
        turnoftash = TurnofCarsofTashkent.objects.filter(waiting=True)
        turns = TurnofCars.objects.filter(waiting=True)
        if turns is None:
            data = {
                "message": "Hozirda navbatda mashina yoq"
            }
        else:
            data = [{
                    'id': turn.id,
                    'mijoz': turn.order.customer.name,
                    'car_number': turn.order.car_number,
                    'driver_phone': turn.order.driver_phone,
                    'date': turn.date.strftime("%d-%m-%Y"),
                    'turn': turn.turn,
                } for turn in turns]
        if turnoftash is None:
            datatashkent = {
                "message": "Hozirda navbatda mashina yoq"
            }
        else:
            datatashkent = [{
                    'id': turn.id,
                    'mijoz': turn.order.customer.name,
                    'car_number': turn.order.car_number,
                    'driver_phone': turn.order.driver_phone,
                    'date': turn.date.strftime("%d-%m-%Y"),
                    'turn': turn.turn,
                } for turn in turnoftash]
        query = {
            "data": data,
            "datatashkent": datatashkent,
        }
        data = {
            "success": True,
            "data": query,
        }
    except Exception as err:
        data = {'success': False, 'error': '{}'.format(err)}
    return Response(data)

@api_view(["POST"])
def car_leave(request):
    try:
        tash = request.data['status']
        turn_id = request.data["turn_id"]
        if tash == 0:
            turn = TurnofCars.objects.get(id=turn_id)
        elif tash == 1:
            turn = TurnofCarsofTashkent.objects.get(id=turn_id)
        if tash == '0':
            turn = TurnofCars.objects.get(id=turn_id)
        elif tash == '1':
            turn = TurnofCarsofTashkent.objects.get(id=turn_id)
        order = turn.order
        turn.status = 3
        turn.save()
        order.status = 4
        order.left_date = timezone.now()
        order.save()
        sum = order.summa_total
        # add customer debt
        customer = Customer.objects.get(id=order.customer.id)
        customer.debt += Decimal(sum)
        customer.save()

        data = {
                "success": True,
                "message": "Mashina muvaffaqiyatli chiqib ketdi",
            }

    except Exception as err:
        data = {"success": False, "error": f"{err}"}

    return Response(data)

class TurnofCarsViewset(viewsets.ModelViewSet):
    queryset = TurnofCars.objects.all()
    serializer_class = TurnofCarsSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        search = request.GET.get('item', '')
        queryset = self.queryset.filter(status=3)
        def check_date_str(search):
            try:
                datetime.strptime(search, "%d-%m-%Y")
                return True
            except Exception:
                return False
        if search != "":
            if check_date_str(search) == True:
                queryset = queryset.filter(order__date=search)
            else:
                queryset = queryset.filter(Q(order__customer__name__icontains=search) | Q(order__car_number=search) |Q(order__driver_phone=search))
        else:
            if user_id := request.GET.get('user_id'):
                user = Employee.objects.get(id=user_id)
                queryset = TurnofCars.objects.filter(status=3, order__tegirmon_id = user.tegirmon.id).order_by('-id')
            else:
                queryset = TurnofCars.objects.filter(status=3).order_by('-id')
                
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class TurnofCarsofTashkentViewset(viewsets.ModelViewSet):
    queryset = TurnofCarsofTashkent.objects.all()
    serializer_class = TurnofCarsofTashkentSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        search = request.GET.get('item', '')
        queryset = self.queryset.filter(status=3)
    
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        month_ago = datetime.today()-timedelta(days=30)
       
        
        
        def check_date_str(search):
            try:
                datetime.strptime(search, "%d-%m-%Y")
                return True
            except Exception:
                return False
        if search != "":
            if check_date_str(search) == True:
                queryset = queryset.filter(order__date=search)
            else:
                queryset = queryset.filter(Q(order__customer__name__icontains=search) | Q(order__car_number=search) |Q(order__driver_phone=search))
        else:
            if user_id := request.GET.get('user_id'):
                user = Employee.objects.get(id=user_id)
                
                if from_date and to_date:
                    queryset = self.queryset.filter(date__range=[from_date, to_date], status=3, order__tegirmon_id = user.tegirmon.id).order_by('-id')
                elif from_date:
                    queryset = self.queryset.filter(date__range=[from_date, to_date], status=3, order__tegirmon_id = user.tegirmon.id).order_by('-id')
                elif to_date:
                    queryset = self.queryset.filter(Q(date__lte=to_date),status=3, order__tegirmon_id = user.tegirmon.id).order_by('-id')
                else:
                    queryset = self.queryset.filter(status=3, order__tegirmon_id = user.tegirmon.id).order_by('-id')
            else:
                queryset = self.queryset.filter(status=3).order_by('-id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
