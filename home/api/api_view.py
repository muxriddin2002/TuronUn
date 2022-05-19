from django.db.models import Sum
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.models import Customer, Employee, Client, Branch, Akt, AktWagon, TypeOutlay, AktOutlay, Store, UnAkt, ClientUn, Tegirmon
from .serializers import EmployeeSerializer, ClientSerializerTarozi, BranchSerializer, AktSerializer, WagonSerializer, UnAktSerializer, UnWagonSerializer, ClientUnSerializerTarozi, TegirmonSerializer


@api_view(['GET'])
def get_akts(request):
    try:
        search = request.GET.get('search')
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
        if date_start is not None and search is not None and date_end is not None:
            akts = Akt.objects.filter(
                name__icontains=search,
                date_start__gte=date_start,
                date_start__lte=date_end,
                status=2
            ).order_by("-id")[:20]
        elif date_start is not None and date_end is not None:
            akts = Akt.objects.filter(
                date_start__gte=date_start,
                date_start__lte=date_end,
                status=2
            ).order_by("-id")[0:20]
        elif search is not None:
            akts = Akt.objects.filter(
                name__icontains=search,
                status=2
            ).order_by("-id")[:20]
        else:
            akts = Akt.objects.filter(status=2).order_by("-id")[:20]
        ser = AktSerializer(akts, many=True)
        data = {
            "success": True,
            "data": ser.data,
            "message": "success"
        }
    except Exception as err:
        data = {'success': False, 'error': '{}'.format(err)}
    return Response(data)


@api_view(['GET'])
def get_unakts(request):
    try:
        search = request.GET.get('search')
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')

        if date_start is not None and search is not None and date_end is not None:
            akts = UnAkt.objects.filter(
                name__icontains=search,
                date_start__gte=date_start,
                date_start__lte=date_end,
                status=2
            ).order_by("-id")[:20]
        elif date_start is not None and date_end is not None:
            akts = UnAkt.objects.filter(
                date_start__gte=date_start,
                date_start__lte=date_end,
                status=2
            ).order_by("-id")[:20]
        elif search is not None:
            akts = UnAkt.objects.filter(
                name__icontains=search,
                status=2
            ).order_by("-id")[:20]
        else:
            akts = UnAkt.objects.filter(status=2).order_by("-id")[:20]
        ser = UnAktSerializer(akts, many=True)
        data = {
            "success": True,
            "data": ser.data,
            "message": "success"
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)


@api_view(['GET'])
def get_akt_wagon(request):
    akt_id = request.GET.get('akt_id')
    try:
        akt = Akt.objects.get(id=akt_id)
        total_brutto = akt.wagons.all().aggregate(total_brutto=Sum('brutto_fakt')).get('total_brutto')
        total_tara = akt.wagons.all().aggregate(total_tara=Sum('tara_fakt')).get('total_tara')
        total_neto = akt.wagons.all().aggregate(total_netto=Sum('netto_fakt')).get('total_netto')
        if total_tara is None:
            total_tara = 0

        if total_brutto is None:
            total_brutto = 0

        if total_neto is None:
            total_neto = 0
        wagons = akt.wagons.all()
        ser = WagonSerializer(wagons, many=True)
        total = {
            "total_tara": total_tara,
            "total_brutto": total_brutto,
            "total_neto": total_neto,
            "vagon_soni": akt.wagons.all().count()
        }
        data = {
            "success": True,
            "message": "Ok",
            "data": {
                "total": total,
                "wagons": ser.data
            }
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)


@api_view(['GET'])
def get_unakt_wagon(request):
    akt_id = request.GET.get('akt_id')
    try:
        akt = UnAkt.objects.get(id=akt_id)
        total_brutto = akt.wagons.all().aggregate(total_brutto=Sum('brutto_fakt')).get('total_brutto')
        total_tara = akt.wagons.all().aggregate(total_tara=Sum('tara_fakt')).get('total_tara')
        total_neto = akt.wagons.all().aggregate(total_netto=Sum('netto_fakt')).get('total_netto')
        if total_tara is None:
            total_tara = 0

        if total_brutto is None:
            total_brutto = 0

        if total_neto is None:
            total_neto = 0
        wagons = akt.wagons.all()
        ser = UnWagonSerializer(wagons, many=True)
        total = {
            "total_tara": total_tara,
            "total_brutto": total_brutto,
            "total_neto": total_neto,
            "vagon_soni": akt.wagons.all().count()
        }
        data = {
            "success": True,
            "message": "Ok",
            "data": {
                "total": total,
                "wagons": ser.data
            }
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)


@api_view(['GET'])
def get_akt_wagon_all(request):
    akt_id = request.GET.get('akt_id')
    try:
        akt = Akt.objects.get(id=akt_id)
        total_brutto = akt.wagons.all().aggregate(total_brutto=Sum('brutto_fakt')).get('total_brutto')
        total_tara = akt.wagons.all().aggregate(total_tara=Sum('tara_fakt')).get('total_tara')
        total_neto = akt.wagons.all().aggregate(total_netto=Sum('netto_fakt')).get('total_netto')
        if total_tara is None:
            total_tara = 0

        if total_brutto is None:
            total_brutto = 0

        if total_neto is None:
            total_neto = 0
        wagons = akt.wagons.all()
        ser = WagonSerializer(wagons, many=True)
        total = {
            "total_tara": total_tara,
            "total_brutto": total_brutto,
            "total_neto": total_neto,
            "vagon_soni": akt.wagons.all().count()
        }
        data = {
            "success": True,
            "message": "Ok",
            "data": {
                "total": total,
                "wagons": ser.data
            }
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)


@api_view(['GET'])
def get_unakt_wagon_all(request):
    akt_id = request.GET.get('akt_id')
    try:
        akt = UnAkt.objects.get(id=akt_id)
        total_brutto = akt.wagons.all().aggregate(total_brutto=Sum('brutto_fakt')).get('total_brutto')
        total_tara = akt.wagons.all().aggregate(total_tara=Sum('tara_fakt')).get('total_tara')
        total_neto = akt.wagons.all().aggregate(total_netto=Sum('netto_fakt')).get('total_netto')
        if total_tara is None:
            total_tara = 0

        if total_brutto is None:
            total_brutto = 0

        if total_neto is None:
            total_neto = 0
        wagons = akt.wagons.all()
        ser = UnWagonSerializer(wagons, many=True)
        total = {
            "total_tara": total_tara,
            "total_brutto": total_brutto,
            "total_neto": total_neto,
            "vagon_soni": akt.wagons.all().count()
        }
        data = {
            "success": True,
            "message": "Ok",
            "data": {
                "total": total,
                "wagons": ser.data
            }
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)


@api_view(['POST'])
def wagon_edit(request):
    try:
        akt_id = request.data.get('akt_id')
        wagon = request.data.get('wagons')
        for i in wagon:
            akt = Akt.objects.get(id=akt_id)
            wg = akt.wagons.get(id=i['id'])
            wg.brutto_fakt = i['brutto_fakt']
            if i['tara_fakt'] > 0:
                wg.tara_fakt = i['tara_fakt']
                wg.netto_fakt = float(i['brutto_fakt']) - float(i['tara_fakt'])
            wg.save()
        total_brutto = akt.wagons.all().aggregate(total_brutto=Sum('brutto_fakt')).get('total_brutto')
        total_tara = akt.wagons.all().aggregate(total_tara=Sum('tara_fakt')).get('total_tara')
        total_neto = akt.wagons.all().aggregate(total_netto=Sum('netto_fakt')).get('total_netto')
        if total_tara is None:
            total_tara = 0

        if total_brutto is None:
            total_brutto = 0

        if total_neto is None:
            total_neto = 0

        if akt.status == 2 and akt.is_edited == False:
            akt.is_edited = True
            akt.save()

        if akt.wagons.filter(brutto_fakt__gt=0, tara_fakt__gt=0).count() == akt.wagons.all().count():
            akt.status = 2
            akt.save()

        total = {
            "total_tara": total_tara,
            "total_brutto": total_brutto,
            "total_neto": total_neto,
            "vagon_soni": akt.wagons.all().count()
        }

        data = {
            "success": True,
            "message": "Wagon qo'shildi!",
            "data": {
                "total": total
            }
        }

    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }

    return Response(data)


@api_view(['POST'])
def unwagon_edit(request):
    try:
        akt_id = request.data.get('akt_id')
        wagon = request.data.get('wagons')
        for i in wagon:
            akt = UnAkt.objects.get(id=akt_id)
            wg = akt.wagons.get(id=i['id'])
            wg.brutto_fakt = i['brutto_fakt']
            wg.tara_fakt = i['tara_fakt']
            wg.netto_fakt = float(i['brutto_fakt']) - float(i['tara_fakt'])
            wg.save()
        total_brutto = akt.wagons.all().aggregate(total_brutto=Sum('brutto_fakt')).get('total_brutto')
        total_tara = akt.wagons.all().aggregate(total_tara=Sum('tara_fakt')).get('total_tara')
        total_neto = akt.wagons.all().aggregate(total_netto=Sum('netto_fakt')).get('total_netto')
        if total_tara is None:
            total_tara = 0

        if total_brutto is None:
            total_brutto = 0

        if total_neto is None:
            total_neto = 0

        if akt.status == 2 and akt.is_edited == False:
            akt.is_edited = True
            akt.save()

        if akt.wagons.filter(brutto_fakt__gt=0, tara_fakt__gt=0).count() == akt.wagons.all().count():
            akt.status = 2
            akt.save()

        total = {
            "total_tara": total_tara,
            "total_brutto": total_brutto,
            "total_neto": total_neto,
            "vagon_soni": akt.wagons.all().count()
        }

        data = {
            "success": True,
            "message": "Wagon qo'shildi!",
            "data": {
                "total": total
            }
        }

    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }

    return Response(data)


@api_view(['GET'])
def get_akts_aktive(request):
    try:
        akts = Akt.objects.filter(status=1).order_by('-id')
        ser = AktSerializer(akts, many=True)
        data = {
            "success": True,
            "data": ser.data,
            "message": "success"
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)


@api_view(['GET'])
def get_unakts_aktive(request):
    try:
        akts = UnAkt.objects.filter(status=1).order_by('-id')
        ser = UnAktSerializer(akts, many=True)
        data = {
            "success": True,
            "data": ser.data,
            "message": "success"
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)


@api_view(['POST'])
def login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            employe = Employee.objects.get(username=username, is_active=True)
            token, created = Token.objects.get_or_create(user=employe)
            if created:
                token = created
            if employe.check_password(password):
                ser = EmployeeSerializer(employe)
                data = {
                    "success": True,
                    "status": 200,
                    "message": "user topildi",
                    "data": ser.data,
                    "token": token.key,
                }
            else:
                data = {
                    "success": False,
                    "error": "Login yoki Parol xato!!",
                    "message": "",
                    "status": 403,
                }
        except Employee.DoesNotExist:
            data = {
                "success": False,
                "error": "Bunday Foydalanuvchi mavjud emas!",
                "message": "",
                "status": 404,
            }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err),
            "message": ""
        }
    return Response(data)


@api_view(['GET'])
def get_client(request):
    try:
        clients = Client.objects.all()
        ser = ClientSerializerTarozi(clients, many=True)
        data = {
            "error": None,
            "data": ser.data
        }
    except Exception as err:
        data = {
            "error": "{}".format(err),
            "data": None
        }
    return Response(data)


@api_view(['GET'])
def get_unclient(request):
    try:
        clients = ClientUn.objects.all()
        ser = ClientUnSerializerTarozi(clients, many=True)
        data = {
            "error": None,
            "data": ser.data
        }
    except Exception as err:
        data = {
            "error": "{}".format(err),
            "data": None
        }
    return Response(data)


@api_view(['GET'])
def get_branch(request):
    try:
        branchs = Tegirmon.objects.all()
        ser = TegirmonSerializer(branchs, many=True)
        data = {
            "error": None,
            "data": ser.data
        }
    except Exception as err:
        data = {
            "error": "{}".format(err),
            "data": None
        }
    return Response(data)


@api_view(['POST'])
def add_wagons(request):
    try:
        akt_id = request.data.get('akt_id')
        vagon_raqami = request.data.get('vagon_raqami')
        brutto = request.data.get('brutto')
        tara = request.data.get('tara')
        try:
            akt = Akt.objects.get(id=akt_id)
            if akt.wagons.filter(number=vagon_raqami).count() > 0:
                wg = akt.wagons.get(number=vagon_raqami)
                wg.brutto_fakt = brutto
                wg.tara_fakt = tara
                wg.netto_fakt = float(brutto) - float(tara)
                wg.save()
                total_brutto = akt.wagons.all().aggregate(total_brutto=Sum('brutto_fakt')).get('total_brutto')
                total_tara = akt.wagons.all().aggregate(total_tara=Sum('tara_fakt')).get('total_tara')
                total_neto = akt.wagons.all().aggregate(total_netto=Sum('netto_fakt')).get('total_netto')
                if total_tara is None:
                    total_tara = 0

                if total_brutto is None:
                    total_brutto = 0

                if total_neto is None:
                    total_neto = 0
                wagons = akt.wagons.filter(brutto_fakt__gt=0, tara_fakt__gt=0)
                ser = WagonSerializer(wagons, many=True)
                total = {
                    "total_tara": total_tara,
                    "total_brutto": total_brutto,
                    "total_neto": total_neto,
                    "vagon_soni": akt.wagons.all().count()
                }
                data = {
                    "success": True,
                    "message": "Ok",
                    "data": {
                        "total": total,
                        "wagons": ser.data
                    }
                }

            else:
                data = {
                    "success": False,
                    "error": "Bunday vagon mavjud emas"
                }
        except Akt.DoesNotExist:
            data = {
                "success": False,
                "error": "Bunday akt mavjud emas!"
            }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)


@api_view(['POST'])
def add_unwagons(request):
    try:
        akt_id = request.data.get('akt_id')
        vagon_raqami = request.data.get('vagon_raqami')
        brutto = request.data.get('brutto')
        tara = request.data.get('tara')
        try:
            akt = UnAkt.objects.get(id=akt_id)
            if akt.wagons.filter(number=vagon_raqami).count() > 0:
                wg = akt.wagons.get(number=vagon_raqami)
                wg.brutto_fakt = brutto
                wg.tara_fakt = tara
                wg.netto_fakt = float(brutto) - float(tara)
                wg.save()
                total_brutto = akt.wagons.all().aggregate(total_brutto=Sum('brutto_fakt')).get('total_brutto')
                total_tara = akt.wagons.all().aggregate(total_tara=Sum('tara_fakt')).get('total_tara')
                total_neto = akt.wagons.all().aggregate(total_netto=Sum('netto_fakt')).get('total_netto')
                if total_tara is None:
                    total_tara = 0

                if total_brutto is None:
                    total_brutto = 0

                if total_neto is None:
                    total_neto = 0
                wagons = akt.wagons.filter(brutto_fakt__gt=0, tara_fakt__gt=0)
                ser = UnWagonSerializer(wagons, many=True)
                total = {
                    "total_tara": total_tara,
                    "total_brutto": total_brutto,
                    "total_neto": total_neto,
                    "vagon_soni": akt.wagons.all().count()
                }
                data = {
                    "success": True,
                    "message": "Ok",
                    "data": {
                        "total": total,
                        "wagons": ser.data
                    }
                }

            else:
                data = {
                    "success": False,
                    "error": "Bunday vagon mavjud emas"
                }
        except Akt.DoesNotExist:
            data = {
                "success": False,
                "error": "Bunday akt mavjud emas!"
            }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)
