from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.models import  Akt, UnAkt
from .serializers import  AktSerializer, WagonSerializer,UnAktSerializer


@api_view(['POST'])
def add_akt_detail_fakt(request):
    try:
        akt_id = request.data.get('akt_id')
        detail = request.data.get('detail')
        akt = Akt.objects.get(id=akt_id)
        for dt in detail:
            wg = akt.wagons.get(id=dt['id'])
            wg.brutto_fakt = dt['brutto']
            wg.tara_fakt = dt['tara']
            wg.netto_fakt = dt['netto']
            wg.save()
        akt.status = 2
        akt.save()
        data = {
            "success":True,
            "message":"Qo'shildi"
        }

    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)

@api_view(['get'])
def get_akt_aktive(request):
    try:
        search = request.GET.get('search')
        if search is not None:
            akts = Akt.objects.filter(
                name__icontains=search,status=1
            ).order_by("-id")[0:20]
        else:
            akts = Akt.objects.filter(status=1).order_by("-id")[:20]

        ser = AktSerializer(akts, many=True)
        data = {
            "success":True,
            "data":ser.data,
            "message":"success"
        }
    except Exception as err:
        data = {
            "success":False,
            "error":"{}".format(err)
        }
    return Response(data)


# un acts status = 1  & user.tegirmon=akt.branch (Created)
@api_view(['get'])
def get_unakts_ombors(request):
    try:
        search = request.GET.get('search')
        if search is not None:
            akts = UnAkt.objects.filter(
                name__icontains=search,status=1, ombor=request.user.tegirmon).order_by("-id")
        else:
            akts = UnAkt.objects.filter(status=1, ombor=request.user.tegirmon).order_by("-id")

        ser = UnAktSerializer(akts, many=True)
        data = {
            "success":True,
            "data":ser.data,
            "message":"success"
        }
    except Exception as err:
        data = {"success": False, "error": f"{err}"}
    return Response(data)


# get akt id via post set status = 2 (Edited)
@api_view(['post'])
def set_unakt_status(request):
    akt_id = request.data.get('akt_id')
    try:
        akt = UnAkt.objects.get(id=akt_id)
        if akt.ombor == request.user.tegirmon:
            akt.status = 2
            akt.save()
        ser = UnAktSerializer(akt)
        data = {
            "success": True,
            "message": "Ok",
            "data": {
                "data": ser.data
            }
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)
