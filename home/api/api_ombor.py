from datetime import timedelta, datetime
from django.utils import timezone
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from home.models import *
from .serializers import *
from rest_framework import viewsets
from django.db.models import Q
from asyncio.log import logger

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000


class StoreHistoryViewset(viewsets.ModelViewSet):
    queryset = StoreHistory.objects.all()
    serializer_class = StoreHistorySerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        data = []
        queryset = self.queryset.all()
        for i in queryset:
            dt = {
                'product': i.product.name,
                'date': i.date.strftime('%Y.%m.%d'),
                'tegirmon': i.tegirmon.name,
                'qop soni': i.qopsoni
            }
            data.append(dt)
        page = self.paginate_queryset(data)
        if page is not None:
            # serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(data)

        # serializer = self.get_serializer(queryset, many=True)
        return Response(data)

    @action(methods=['GET'], detail=False)
    def accepted(self, request):
        user_id = request.GET['user_id']
        user = Employee.objects.get(id=user_id)
        if user.type == 15:
            queryset = self.queryset.filter(product__type__name__icontains="Yem", status=2, tegirmon=user.tegirmon)
        elif user.type == 16:
            queryset = self.queryset.filter(product__type__name__icontains="Un", status=2, tegirmon=user.tegirmon)
        else:
            queryset = self.queryset.filter(status=2, tegirmon=user.tegirmon)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductionHistoryViewset(viewsets.ModelViewSet):
    queryset = ProductionHistory.objects.all()
    serializer_class = ProductionHistorySerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        user_id = request.GET['user_id']
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
        user = Employee.objects.get(id=user_id)
        if date_start is not None and date_end is not None:
            if user.type == 13:
                queryset = self.queryset.filter(product__type__name__icontains="Yem", tegirmon=user.tegirmon,date__gte=date_start, date__lte=date_end)
            if user.type == 14:
                queryset = self.queryset.filter(product__type__name__icontains="Un", tegirmon=user.tegirmon, date__gte=date_start, date__lte=date_end)
        else:
            if user.type == 13:
                queryset = self.queryset.filter(product__type__name__icontains="Yem", tegirmon=user.tegirmon)
            if user.type == 14:
                queryset = self.queryset.filter(product__type__name__icontains="Un", tegirmon=user.tegirmon)
                
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class Return_productViewset(viewsets.ModelViewSet):
    queryset = Return_product.objects.all()
    serializer_class = Return_productSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        user_id = request.GET['user_id']
        user = Employee.objects.get(id=user_id)
        if user.type == 15:
            queryset = self.queryset.filter(product__type__name__icontains="Yem", tegirmon=user.tegirmon)
        if user.type == 16:
            queryset = self.queryset.filter(product__type__name__icontains="Un", tegirmon=user.tegirmon)
        if user.type == 6 or user.type == 20:
            queryset = self.queryset.filter(tegirmon=user.tegirmon)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class QaytuvViewset(viewsets.ModelViewSet):
    queryset = Qaytuv.objects.all()
    serializer_class = QaytuvSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        user_id = request.GET['user_id']
        user = Employee.objects.get(id=user_id)
        baskets_ids = Qaytuv.objects.filter(status=2).values_list(
            'baskets').distinct()
        basket_list = []
        for basket_id in baskets_ids:
            if user.type == 15:
                bask = BasketQaytuv.objects.get(id=basket_id[0])
                if bask.product.product.type.name == 'Yem':
                    basket_list.append(basket_id[0])
            if user.type == 16:
                bask = BasketQaytuv.objects.get(id=basket_id[0])
                if bask.product.product.type.name == 'Un':
                    basket_list.append(basket_id[0])
            if user.type in [6, 20]:
                basket_list.append(basket_id[0])

        qaytuvs = Qaytuv.objects.filter(baskets__in=basket_list).distinct()
        page = self.paginate_queryset(qaytuvs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qaytuvs, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def products(request):
    product = Product.objects.all()
    ser = ProductSerializer(product, many=True)

    return Response(ser.data)


@api_view(['GET'])
def get_product(request):
    try:
        user_id = request.GET.get("user_id")
        user = Employee.objects.get(id=user_id)

        if user.type == 15:
            product = Product.objects.filter(type__name__icontains="Yem")
        elif user.type == 16:
            product = Product.objects.filter(type__name__icontains="Un")
        else:
            product = Product.objects.filter(store_product__tegirmon_id=user.tegirmon.id)
        dat = []
        for i in product:
            dt = {
                'id': i.id,
                'name': i.name,
                'maxsulot codi': i.pr_code,
            }
            dat.append(dt)
        data = {
            "success": True,
            "data": dat
        }
    except Exception as err:
        data = {'success': False, 'error': f'{err}'}
    return Response(data)


@api_view(['GET'])
def get_store_history(request):
    try:
        user_id = request.GET.get("user_id")
        user = Employee.objects.get(id=user_id)

        if user.type == 15:
            store = StoreHistory.objects.filter(product__type__name__icontains="Yem", status=1, tegirmon=user.tegirmon)
        elif user.type == 16:
            store = StoreHistory.objects.filter(product__type__name__icontains="Un", status=1, tegirmon=user.tegirmon)
        else:
            store = StoreHistory.objects.filter(status=1, tegirmon=user.tegirmon)
        dat = []
        for i in store:
            dt = {
                'id': i.id,
                'maxsulot_nomi': i.product.name,
                'maxsulot_turi': i.product.type.name,
                'sana': i.date.strftime("%Y-%m-%d"),
                'tegirmon': i.tegirmon.name,
                'qopsoni': i.qopsoni,
            }
            dat.append(dt)
        data = {
            "success": True,
            "data": dat
        }
    except Exception as err:
        data = {'success': False, 'error': f'{err}'}
    return Response(data)


@api_view(['POST'])
def add_store(request):
    try:
        user_id = request.data.get("user_id")
        user = Employee.objects.get(id=user_id)
        code = request.data.get("code")
        logger.info(f'{user_id} yangiladi')
        for i in code:
            barcode = Barcodes.objects.get(code=i)

            if StoreHistory.objects.filter(product=barcode.product, tegirmon=user.tegirmon, date=barcode.date, status=1).count() > 0:
                st = StoreHistory.objects.get(product=barcode.product, tegirmon=user.tegirmon, date=barcode.date, status=1)
                st.qopsoni += 1
                st.save()
            else:
                StoreHistory.objects.create(product=barcode.product, tegirmon=user.tegirmon,
                                    date=barcode.date, status=1, qopsoni=1)

            if ProductionHistory.objects.filter(product=barcode.product, tegirmon=user.tegirmon, date=barcode.date).count() > 0:
                pr = ProductionHistory.objects.get(product=barcode.product, tegirmon=user.tegirmon, date=barcode.date)
                pr.qopsoni += 1
                pr.save()
            else:
                ProductionHistory.objects.create(product=barcode.product, tegirmon=user.tegirmon,
                                    date=barcode.date, qopsoni=1)

        data = {
            "success": True,
            "data": "Muvaffaqiyatli qo'shildi!",
        }

    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(["POST"])
def accept_store(request):
    try:
        # store_id = request.data.getlist("store_id")
        code = request.data.get("code")
        user_id = request.data.get('user_id')
        user = Employee.objects.get(id=user_id)
        for i in code:
            cod = Barcodes.objects.get(code=i)
            if Store.objects.filter(product=cod.product, tegirmon=user.tegirmon):
                st = Store.objects.get(product=cod.product, tegirmon=user.tegirmon)
                st.miqdori += 1
                st.save()
            else:
                Store.objects.craete(product=cod.product, tegirmon=user.tegirmon, miqdori=1)

        data = {
            "success": True,
            "data": "Muvaffaqiyatli qo'shildi!",
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

#user firebase token
@api_view(["POST"])
def user_firebase_token(request):
    try:
        user_id = request.data.get("user_id")
        token = request.data.get('token')
        user = Employee.objects.get(id=user_id)
        user.firebase_token = token
        user.save()
        data = {
            "success": True,
            "data": f"Muvaffaqiyatli {user_id} token belgilandi!",
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(["POST"])
def changestatusofhistory(request):
    try:
        store_id = request.data.get("store_id")
        user_id = request.data.get('user_id')

        st = StoreHistory.objects.get(id=store_id)
        st.status = 2
        st.save()


        store = Store.objects.get(product=st.product, tegirmon=st.tegirmon)

        store.miqdori += st.qopsoni
        store.save()

        data = {
            "success": True,
            "data": "Muvaffaqiyatli qo'shildi!",
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)


@api_view(["POST"])
def return_product(request):
    try:
        date = timezone.now().date()
        code = request.data.get("code")
        izoh = request.data.get("izoh")
        image = request.data.get("image")
        user_id = request.data.get("user")
        user = Employee.objects.get(id=user_id)
        for i in code:
            product = Barcodes.objects.get(code=i)
            count = Return_product.objects.filter(product=product.product, date=date, izoh=izoh, tegirmon=user.tegirmon).count()
            if count > 0:
                ret = Return_product.objects.get(product=product.product, date=date, izoh=izoh, tegirmon=user.tegirmon)
                ret.qopsoni += 1
                ret.save()
            else:
                Return_product.objects.create(product=product.product, date=date, izoh=izoh, image=image, tegirmon=user.tegirmon, qopsoni=1)

        data = {
            "success": True,
            "data": "Muvaffaqiyatli qo'shildi!"
        }

    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(["GET"])
def get_store_product(request):
    try:
        if user_id := request.GET.get("user_id"):
            user = Employee.objects.get(id=user_id)
            store = Store.objects.filter(tegirmon=user.tegirmon)
        else:
            store = Store.objects.all()
        dat = []
        for i in store:
            dt = {
                'id': i.id,
                'maxsulot nomi': i.product.name,
                'zavod': i.tegirmon.name,
                'qoplar soni': i.miqdori,
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
def edit_store_product(request):
    try:
        un_id = request.data["un_id"]
        soni = request.data["soni"]
        if user_id := request.data.get("user_id"):
            user = Employee.objects.get(id=user_id)
            logger.info(f'{user} - {user.username} foydalanuvchi {un_id} id mahsulotni {soni} ga yangiladi')
        else:
            logger.info(f'{un_id} mahsulot  yangiladi')

        store = Store.objects.get(id=un_id)
        store.miqdori = float(soni)
        store.save()


        data = {
            "success": True,
            "data": 'Store yangilandi!',
        }

    except Exception as err:
        data = {"success": False, "error": f"{err}"}
        logger.error(data)
    return Response(data)



@api_view(["POST"])
def add_barcode(request):
    product_id = request.data['product']
    date = request.data['date']
    quantity = int(request.data['quantity'])
    # BarcodesHistory.objects.create(product_id=product_id, date=date, quantity=quantity)
    dat = []
    for _ in range(quantity):
        product = Product.objects.get(id=product_id)
        barcode = Barcodes.objects.create(product=product, date=date)
        dt = {
            'barcode': barcode.code
        }
        dat.append(dt)
    return Response(dat)

@api_view(["POST"])
def add_client_tin(request):
    try:
        compony = request.data['compony']
        name = request.data['name']
        phone = request.data['phone']
        address = request.data['address']
        comment = request.data['comment']
        debt = int(request.data['debt'])
        ClientTin.objects.create(compony=compony, name=name, phone=phone, address=address, comment=comment, debt=debt)
        data = {
            "success": True,
            "error": "Qob taminotchisi yaratildi!"
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)

#qop
@api_view(["GET"])
def get_clients_qop(request):
    try:
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        time = request.GET.get('time')
        if from_date and to_date:
            query = ClientTin.objects.filter(date_start__range=[from_date, to_date]).order_by('-id')
        elif from_date:
            query = ClientTin.objects.filter(date_start__gte=from_date).order_by('-id')
        elif to_date:
            query = ClientTin.objects.filter(date_start__lte=to_date).order_by('-id')
        elif time == 'kun':
            query = ClientTin.objects.filter(
                date_start__gte=timezone.now() - timedelta(days=1)
            ).order_by('-id')

        elif time == 'hafta':
            query = ClientTin.objects.filter(
                date_start__gte=timezone.now() - timedelta(days=7)
            ).order_by('-id')

        else:
            query = ClientTin.objects.filter(
                date_start__gte=timezone.now() - timedelta(days=30)
            ).order_by('-id')

        ser = ClientTinSerializer(query, many=True)
        data = {
            "success": True,
            "clients": ser.data
        }
    except Exception as err:

        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)

#qop qoldiq
@api_view(["GET"])
def get_tin_qoldiq(request):
    try:
        queryset = Tin.objects.all()
        ser = TinSerializer(queryset, many=True)
        data = {
            "success": True,
            "qoblar": ser.data
        }
    except Exception as err:

        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)

@api_view(["GET"])
def get_history_of_tin(request):
    try:
        user_id = request.GET['user_id']
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        time = request.GET.get('time')
        emp = Employee.objects.get(id=user_id)

        if from_date and to_date:
            query = Tinhistory.objects.filter(Q(tegirmon=emp.tegirmon) & Q(
                date__range=[from_date, to_date])).order_by('-id')
        elif from_date:
            query = Tinhistory.objects.filter(
                Q(tegirmon=emp.tegirmon) & Q(date__gte=from_date)).order_by('-id')
        elif to_date:
            query = Tinhistory.objects.filter(
                Q(tegirmon=emp.tegirmon) & Q(date__lte=to_date)).order_by('-id')
        elif time == 'kun':
            query = Tinhistory.objects.filter(
                (
                    Q(tegirmon=emp.tegirmon)
                    & Q(date__gte=timezone.now() - timedelta(days=1))
                )
            ).order_by('-id')

        elif time == 'hafta':
            query = Tinhistory.objects.filter(
                (
                    Q(tegirmon=emp.tegirmon)
                    & Q(date__gte=timezone.now() - timedelta(days=7))
                )
            ).order_by('-id')

        else:
            query = Tinhistory.objects.filter(
                (
                    Q(tegirmon=emp.tegirmon)
                    & Q(date__gte=timezone.now() - timedelta(days=30))
                )
            ).order_by('-id')

        ser = TinhistorySerializer(query, many=True)
        data = {
            "success": True,
            "qop_history": ser.data
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(["GET"])
def get_type_of_tin(request):
    try:
        queryset = TypeofTin.objects.filter()
        ser = TypeofTinSerializer(queryset, many=True)
        data = {
            "success": True,
            "qop_history": ser.data
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(["POST"])
def create_tin(request):
    try:
        user_id = request.data['user_id']
        emp = Employee.objects.get(id=user_id)
        taminotchi = request.data['taminotchi']
        type = request.data['type']
        soni = request.data['soni']
        izoh = request.data['izoh']
        Tinhistory.objects.create(client_id=taminotchi, type_id=type, quantity=soni, izoh=izoh, tegirmon=emp.tegirmon)
        tin = Tin.objects.filter(type_id=type)
        if tin.count() > 0:
            qop = Tin.objects.get(type_id=type)
            qop.quantity += int(soni)
            qop.save()
        else:
            Tin.objects.create(type_id=type, quantity=soni)

        data = {
            "success": True,
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

#kirim bulgan qopni qaytarish
@api_view(["POST"])
def return_income_qop(request):
    try:
        user_id = request.data['user_id']
        emp = Employee.objects.get(id=user_id)
        income_qop_type = request.data['income_qop_type_id']
        soni = request.data['soni']
        izoh = request.data['izoh']
        qop = Tin.objects.get(type_id=income_qop_type)
        qop.quantity -= int(soni)
        qop.save()
        ReturnedIncomeTinHistory.objects.create(type_id=income_qop_type, quantity=soni, izoh=izoh, tegirmon=emp.tegirmon)
        data = {
            "success": True,
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)

#kirim bulgan qopni qaytarish
@api_view(["POST"])
def return_expanse_qop(request):
    try:
        user_id = request.data['user_id']
        emp = Employee.objects.get(id=user_id)
        expanse_qop_type = request.data['expanse_qop_type_id']
        soni = request.data['soni']
        izoh = request.data['izoh']
        
        qop = Tin.objects.get(type_id=expanse_qop_type)
        qop.quantity += int(soni)
        qop.save()
        ReturnedExpanseTinHistory.objects.create(type_id=expanse_qop_type, quantity=soni, izoh=izoh, tegirmon=emp.tegirmon)
        data = {
            "success": True,
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)

@api_view(["GET"])
def get_qop_ombor(request):
    try:
        user_id = request.GET['user_id']
        emp = Employee.objects.get(id=user_id)
        query = Tin.objects.filter(tegirmon=emp.tegirmon)
        ser = TinSerializer(query, many=True)
        data = {
            "success": True,
            "qop": ser.data
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

#qob chiqim
@api_view(["POST"])
def expance_qop(request):
    try:
        user_id = request.data['user_id']
        emp = Employee.objects.get(id=user_id)
        qop = request.data['qop_id']
        soni = request.data['soni']
        izoh = request.data['izoh']
        tin = Tin.objects.get(type_id=qop)
        if tin.quantity < int(soni):
            data = {
                "success": False,
                "error": "Miqdor yetarli emas"
            }
            return Response(data)
        else:
            tin.quantity -= int(soni)
            tin.save()
        ExpanceTin.objects.create(type=tin.type, quantity=int(soni), izoh=izoh, tegirmon=emp.tegirmon)
        data = {
            "success": True,
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)
from django.db import transaction



@api_view(["GET"])
def qop_chiqim_tarixi(request):
    try:
        user_id = request.GET.get('user_id')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        time = request.GET.get('time')
        emp = Employee.objects.get(id=user_id)
        if from_date and to_date:
            query = ExpanceTin.objects.filter(Q(tegirmon=emp.tegirmon) & Q(date__range=[from_date, to_date])).order_by('-id')
        elif from_date:
            query = ExpanceTin.objects.filter(Q(tegirmon=emp.tegirmon) & Q(date__gte=from_date)).order_by('-id')
        elif to_date:
            query = ExpanceTin.objects.filter(
                Q(tegirmon=emp.tegirmon) & Q(date__lte=to_date)).order_by('-id')
        elif time == 'kun':
            query = ExpanceTin.objects.filter(
                (
                    Q(tegirmon=emp.tegirmon)
                    & Q(date__gte=timezone.now() - timedelta(days=1))
                )
            ).order_by('-id')

        elif time == 'hafta':
            query = ExpanceTin.objects.filter(
                (
                    Q(tegirmon=emp.tegirmon)
                    & Q(date__gte=timezone.now() - timedelta(days=7))
                )
            ).order_by('-id')

        else:
            query = ExpanceTin.objects.filter(
                (
                    Q(tegirmon=emp.tegirmon)
                    & Q(date__gte=timezone.now() - timedelta(days=30))
                )
            ).order_by('-id')


        ser = ExpanceTinSerializer(query, many=True)
        data = {
            "success": True,
            "qop_chiqim": ser.data
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

#qaytarilgan kirim qoplar tarixi
@api_view(["GET"])
def get_returned_income_qop(request):
    try:
        user_id = request.GET.get('user_id')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        time = request.GET.get('time')
        emp = Employee.objects.get(id=user_id)
        if from_date and to_date:
            query = ReturnedIncomeTinHistory.objects.filter(Q(tegirmon=emp.tegirmon) & Q(date__range=[from_date, to_date])).order_by('-id')
        elif from_date:
            query = ReturnedIncomeTinHistory.objects.filter(Q(tegirmon=emp.tegirmon) & Q(date__gte=from_date)).order_by('-id')
        elif to_date:
            query = ReturnedIncomeTinHistory.objects.filter(
                Q(tegirmon=emp.tegirmon) & Q(date__lte=to_date)).order_by('-id')
        elif time == 'kun':
            query = ReturnedIncomeTinHistory.objects.filter(
                (
                    Q(tegirmon=emp.tegirmon)
                    & Q(date__gte=timezone.now() - timedelta(days=1))
                )
            ).order_by('-id')

        elif time == 'hafta':
            query = ReturnedIncomeTinHistory.objects.filter(
                (
                    Q(tegirmon=emp.tegirmon)
                    & Q(date__gte=timezone.now() - timedelta(days=7))
                )
            ).order_by('-id')

        else:
            query = ReturnedIncomeTinHistory.objects.filter(
                (
                    Q(tegirmon=emp.tegirmon)
                    & Q(date__gte=timezone.now() - timedelta(days=30))
                )
            ).order_by('-id')


        ser = ReturnedIncomeTinHistoryTinSerializer(query, many=True)
        data = {
            "success": True,
            "qop_kirimlaridan_qaytarilgan": ser.data
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)

#qaytarilgan chiqim qoplar tarixi
@api_view(["GET"])
def get_returned_expanse_qop(request):
    try:
        user_id = request.GET.get('user_id')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        time = request.GET.get('time')
        emp = Employee.objects.get(id=user_id)
        if from_date and to_date:
            query = ReturnedExpanseTinHistory.objects.filter(Q(tegirmon=emp.tegirmon) & Q(date__range=[from_date, to_date])).order_by('-id')
        elif from_date:
            query = ReturnedExpanseTinHistory.objects.filter(Q(tegirmon=emp.tegirmon) & Q(date__gte=from_date)).order_by('-id')
        elif to_date:
            query = ReturnedExpanseTinHistory.objects.filter(
                Q(tegirmon=emp.tegirmon) & Q(date__lte=to_date)).order_by('-id')
        elif time == 'kun':
            query = ReturnedExpanseTinHistory.objects.filter(
                (
                    Q(tegirmon=emp.tegirmon)
                    & Q(date__gte=timezone.now() - timedelta(days=1))
                )
            ).order_by('-id')

        elif time == 'hafta':
            query = ReturnedExpanseTinHistory.objects.filter(
                (
                    Q(tegirmon=emp.tegirmon)
                    & Q(date__gte=timezone.now() - timedelta(days=7))
                )
            ).order_by('-id')

        else:
            query = ReturnedExpanseTinHistory.objects.filter(
                (
                    Q(tegirmon=emp.tegirmon)
                    & Q(date__gte=timezone.now() - timedelta(days=30))
                )
            ).order_by('-id')


        ser = ReturnedExpanseTinHistoryTinSerializer(query, many=True)
        data = {
            "success": True,
            "qop_chiqimlaridan_qaytarilgan": ser.data
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)


@api_view(["GET"]) 
def filter_statistics(request):
    try:
        user_id = request.GET['user_id']
        emp = Employee.objects.get(id=user_id)
        qop_turi = request.GET.get('qop_turi')
        kun = request.GET.get('kun')
        hafta = request.GET.get('hafta')
        oy = request.GET.get('oy')
        start = request.GET.get('start')
        end = request.GET.get('end')
        sana = datetime.today()
        bugun = sana.date()
        current_week = timezone.now().isocalendar()[1]
        current_month = bugun.strftime("%m")
        if qop_turi == "" and kun == "" and hafta == "" and oy == "" and start == "" and end == "":
            query = Tinhistory.objects.filter(tegirmon=emp.tegirmon)
        if qop_turi != "" and kun == "" and hafta == "" and oy == "" and start == "" and end == "":
            qop = TypeofTin.objects.get(id=qop_turi)
            query = Tinhistory.objects.filter(type=qop, tegirmon=emp.tegirmon)
        if qop_turi != "" and kun != "" and hafta == "" and oy == "" and start == "" and end == "":
            qop = TypeofTin.objects.get(id=qop_turi)
            query = Tinhistory.objects.filter(type=qop, date=bugun, tegirmon=emp.tegirmon)
        if qop_turi != "" and kun == "" and hafta != "" and oy == "" and start == "" and end == "":
            qop = TypeofTin.objects.get(id=qop_turi)
            query = Tinhistory.objects.filter(type=qop, date__week=current_week, tegirmon=emp.tegirmon)
        if qop_turi != "" and kun == "" and hafta == "" and oy != "" and start == "" and end == "":
            qop = TypeofTin.objects.get(id=qop_turi)
            query = Tinhistory.objects.filter(type=qop, date__month=current_month, tegirmon=emp.tegirmon)
        if qop_turi != "" and kun == "" and hafta == "" and oy == "" and start != "" and end != "":
            qop = TypeofTin.objects.get(id=qop_turi)
            query = Tinhistory.objects.filter(type=qop, date__gte=start, date__lte=end, tegirmon=emp.tegirmon)

        if qop_turi == "" and kun != "" and hafta == "" and oy == "" and start == "" and end == "":
            query = Tinhistory.objects.filter(date=bugun, tegirmon=emp.tegirmon)
        if qop_turi == "" and kun == "" and hafta != "" and oy == "" and start == "" and end == "":
            query = Tinhistory.objects.filter(date__week=current_week, tegirmon=emp.tegirmon)
        if qop_turi == "" and kun == "" and hafta == "" and oy != "" and start == "" and end == "":
            query = Tinhistory.objects.filter(date__month=current_month, tegirmon=emp.tegirmon)
        if qop_turi == "" and kun == "" and hafta == "" and oy == "" and start != "" and end != "":
            query = Tinhistory.objects.filter(date__gte=start, date__lte=end, tegirmon=emp.tegirmon)

        ser = TinhistorySerializer(query, many=True)
        data = {
            "success": True,
            "filtered": ser.data
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)

@api_view(["GET"])
def ReturnedProducts(request):
    try:
        if user_id := request.GET.get('user_id'):
            user = Employee.objects.get(id=user_id)
            products = Return_product.objects.filter(status=1, tegirmon=user.tegirmon)
        else:
            products = Return_product.objects.filter(status=1)
        data = []
        for i in products:
            dt = {
                'id': i.id,
                'product': i.product.name,
                'date': i.date,
                'izoh': i.izoh,
                'tegirmon': i.tegirmon.name,
                'qopsoni': i.qopsoni,
                "image": i.image.url,
            }
            data.append(dt)
        data = {
            "success": True,
            'data': data,
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)

@api_view(["GET"])
def ReturnedProductsHistory(request):
    try:
        products = Return_product.objects.filter(status=2)
        data = []
        for i in products:
            dt = {
                'id': i.id,
                'product': i.product.name,
                'product_id': i.product.id,
                'date': i.date,
                'izoh': i.izoh,
                'tegirmon': i.tegirmon.name,
                'qopsoni': i.qopsoni,
                "image": i.image.url,
            }
            data.append(dt)
        data = {
            "success": True,
            'data': data,
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)

@api_view(["POST"])
def ConfirmReturned(request):
    id = request.data['id']
    ret = Return_product.objects.get(id=id)
    ret.status = 2
    ret.save()
    store = Store.objects.get(product=ret.product, tegirmon=ret.tegirmon)
    store.miqdori -= ret.qopsoni
    store.save()
    try:
        data = {
            "success": True,
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)

@api_view(["GET"])
def filter_returned(request):
    try:
        user_id = request.GET['user_id']
        emp = Employee.objects.get(id=user_id)
        maxsulot_turi = request.GET.get('maxsulot_turi')
        kun = request.GET.get('kun')
        hafta = request.GET.get('hafta')
        oy = request.GET.get('oy')
        start = request.GET.get('start')
        end = request.GET.get('end')
        sana = timezone.today()
        bugun = sana.date()
        current_week = timezone.now().isocalendar()[1]
        current_month = bugun.strftime("%m")
        if maxsulot_turi == "" and kun == "" and hafta == "" and oy == "" and start == "" and end == "":
            query = Return_product.objects.filter(tegirmon=emp.tegirmon, status=2)
        if maxsulot_turi != "" and kun == "" and hafta == "" and oy == "" and start == "" and end == "":
            qop = Product.objects.get(id=maxsulot_turi)
            query = Return_product.objects.filter(product=qop, tegirmon=emp.tegirmon, status=2)
        if maxsulot_turi != "" and kun != "" and hafta == "" and oy == "" and start == "" and end == "":
            qop = Product.objects.get(id=maxsulot_turi)
            query = Return_product.objects.filter(product=qop, date=bugun, tegirmon=emp.tegirmon, status=2)
        if maxsulot_turi != "" and kun == "" and hafta != "" and oy == "" and start == "" and end == "":
            qop = Product.objects.get(id=maxsulot_turi)
            query = Return_product.objects.filter(product=qop, date__week=current_week, tegirmon=emp.tegirmon, status=2)
        if maxsulot_turi != "" and kun == "" and hafta == "" and oy != "" and start == "" and end == "":
            qop = Product.objects.get(id=maxsulot_turi)
            query = Return_product.objects.filter(product=qop, date__month=current_month, tegirmon=emp.tegirmon, status=2)
        if maxsulot_turi != "" and kun == "" and hafta == "" and oy == "" and start != "" and end != "":
            qop = Product.objects.get(id=maxsulot_turi)
            query = Return_product.objects.filter(product=qop, date__gte=start, date__lte=end, tegirmon=emp.tegirmon, status=2)

        if maxsulot_turi == "" and kun != "" and hafta == "" and oy == "" and start == "" and end == "":
            query = Return_product.objects.filter(date=bugun, tegirmon=emp.tegirmon, status=2)
        if maxsulot_turi == "" and kun == "" and hafta != "" and oy == "" and start == "" and end == "":
            query = Return_product.objects.filter(date__week=current_week, tegirmon=emp.tegirmon, status=2)
        if maxsulot_turi == "" and kun == "" and hafta == "" and oy != "" and start == "" and end == "":
            query = Return_product.objects.filter(date__month=current_month, tegirmon=emp.tegirmon, status=2)
        if maxsulot_turi == "" and kun == "" and hafta == "" and oy == "" and start != "" and end != "":
            query = Return_product.objects.filter(date__gte=start, date__lte=end, tegirmon=emp.tegirmon, status=2)

        ser = Return_productSerializer(query, many=True)
        data = {
            "success": True,
            "filtered": ser.data
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)

@api_view(["GET"])
def delete_order(request):
    try:
        three_day_ago = timezone.now() - timedelta(days=3)
        print(three_day_ago)
        order = Order.objects.filter(date__lte=three_day_ago, status__in = [2,3])
        for i in order:
            i.status = 4
            i.left_date = timezone.now()
            i.save()
        print(order)
        logger.info(f"{order}")
        data = {
            "success": True,
            
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)