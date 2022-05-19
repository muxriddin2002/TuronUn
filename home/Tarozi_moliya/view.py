from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import TemplateView, DetailView

from home.models import *


class Dashboard(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_moliya/dashboard.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 9:
            return redirect('logout')
        return super(Dashboard, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        clients = Client.objects.all()
        oakt = Akt.objects.filter(status=2)
        old_wagons = sum(wg.wagons.count() for wg in oakt)
        nakt = Akt.objects.filter(status=1)
        new_wagons = sum(wg.wagons.count() for wg in nakt)
        un = Order.objects.filter(status=4)
        total_yem = 0
        total_un = 0
        for i in un:
            un_bask = i.baskets.filter(product__product__type__name="Un")
            for bk in un_bask:
                total_un += bk.hajmi
            yem_bask = i.baskets.filter(product__product__type__name="Yem")
            for bk in yem_bask:
                total_yem += bk.hajmi
        day = datetime.now()
        month = day.month
        year = day.year
        akt_oylar = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
            10: [],
            11: [],
            12: [],
        }
        for i in range(1, 13):
            monthly = Akt.objects.filter(status=2, date_start__month=i, date_start__year=year)
            for income in monthly:
                wg = income.wagons.all()
                for w in wg:
                    akt_oylar[i].append(w.netto_fakt)
        chiqimakt_oylar = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
            10: [],
            11: [],
            12: [],
        }
        for i in range(1, 13):
            monthly = Akt.objects.filter(status=2, date_start__month=i, date_start__year=year)
            price = sum(income.total for income in monthly)
            chiqimakt_oylar[i].append(price)
        un_new = 0
        unnew = UnAkt.objects.filter(status=1, date_start__month=month, date_start__year=year)
        for un in unnew:
            un_new += un.wagons.all().count()
        un_old = 0
        unold = UnAkt.objects.filter(status=2, date_start__month=month, date_start__year=year)
        for un in unold:
            un_old += un.wagons.all().count()
        return {
            "un_new": un_new,
            "un_old": un_old,
            "jan": sum(akt_oylar[1]),
            "feb": sum(akt_oylar[2]),
            "mar": sum(akt_oylar[3]),
            "apr": sum(akt_oylar[4]),
            "may": sum(akt_oylar[5]),
            "jun": sum(akt_oylar[6]),
            "jul": sum(akt_oylar[7]),
            "aug": sum(akt_oylar[8]),
            "sep": sum(akt_oylar[9]),
            "oct": sum(akt_oylar[10]),
            "nov": sum(akt_oylar[11]),
            "dec": sum(akt_oylar[12]),
            "janch": sum(chiqimakt_oylar[1]),
            "febch": sum(chiqimakt_oylar[2]),
            "march": sum(chiqimakt_oylar[3]),
            "aprch": sum(chiqimakt_oylar[4]),
            "maych": sum(chiqimakt_oylar[5]),
            "junch": sum(chiqimakt_oylar[6]),
            "julch": sum(chiqimakt_oylar[7]),
            "augch": sum(chiqimakt_oylar[8]),
            "sepch": sum(chiqimakt_oylar[9]),
            "octch": sum(chiqimakt_oylar[10]),
            "novch": sum(chiqimakt_oylar[11]),
            "decch": sum(chiqimakt_oylar[12]),
            'clients': clients,
            'old_wagons': old_wagons,
            'new_wagons': new_wagons,
            'total_yem': int(total_yem),
            'total_un': int(total_un),
        }

def changekgofclient(request):
    client_id = request.GET.get('client')
    print(client_id)
    client = Client.objects.get(id=client_id)
    day = datetime.now()
    month = day.month
    year = day.year

    akt_oylar = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
        10: [],
        11: [],
        12: [],
    }
    for i in range(1, 13):
        monthly = Akt.objects.filter(client=client, status=2, date_start__month=i, date_start__year=year)

        for income in monthly:
            wg = income.wagons.all()
            for w in wg:
                akt_oylar[i].append(w.netto_fakt)

    dt = {
            "jan": sum(akt_oylar[1]),
            "feb": sum(akt_oylar[2]),
            "mar": sum(akt_oylar[3]),
            "apr": sum(akt_oylar[4]),
            "may": sum(akt_oylar[5]),
            "jun": sum(akt_oylar[6]),
            "jul": sum(akt_oylar[7]),
            "aug": sum(akt_oylar[8]),
            "sep": sum(akt_oylar[9]),
            "oct": sum(akt_oylar[10]),
            "nov": sum(akt_oylar[11]),
            "dec": sum(akt_oylar[12]),
    }
    return JsonResponse(dt)


def Getdashdetailmoliya(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    oakt = Akt.objects.filter(date_start__gte=start, date_end__lte=end, status=2)
    nakt = Akt.objects.filter(date_start__gte=start, date_end__lte=end, status=1)
    old_wagons = sum(wg.wagons.count() for wg in oakt)
    new_wagons = sum(wg.wagons.count() for wg in nakt)
    un = Order.objects.filter(date__gte=start, date__lte=end, status=4)
    total_yem = 0
    total_un = 0
    for i in un:
        un_bask = i.baskets.filter(product__product__type__name="Un")
        for bk in un_bask:
            total_un += bk.hajmi
        yem_bask = i.baskets.filter(product__product__type__name="Yem")
        for bk in yem_bask:
            total_yem += bk.hajmi

    un_new = 0
    unnew = UnAkt.objects.filter(status=1, date_start__gte=start, date_start__lte=end)
    for un in unnew:
        un_new += un.wagons.all().count()

    un_old = 0
    unold = UnAkt.objects.filter(status=2, date_start__gte=start, date_start__lte=end)
    for un in unold:
        un_old += un.wagons.all().count()


    dt = {
        "un_new": un_new,
        "un_old": un_old,
        'old_wagons': old_wagons,
        'new_wagons': new_wagons,
        'total_yem': total_yem,
        'total_un': total_un,
    }
    return JsonResponse(dt)


class AktView(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_moliya/aktlar.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 9:
            return redirect('logout')
        return super(AktView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(AktView, self).get_context_data(**kwargs)
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        if date_start is not None and date_end is not None:
            d_st = datetime.strptime(date_start, "%m/%d/%Y")
            d_en = datetime.strptime(date_end, "%m/%d/%Y")
            akts = Akt.objects.filter(
                date_start__gte=d_st.date(),
                date_start__lte=d_en.date()
            )[:30]
        else:
            akts = Akt.objects.all().order_by("-id")[:30]
        return {
            'akts': akts,
        }


class UnAktView(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_moliya/unaktlar.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 9:
            return redirect('logout')
        return super(UnAktView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(UnAktView, self).get_context_data(**kwargs)
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        if date_start is not None and date_end is not None:
            d_st = datetime.strptime(date_start, "%m/%d/%Y")
            d_en = datetime.strptime(date_end, "%m/%d/%Y")
            akts = UnAkt.objects.filter(
                date_start__gte=d_st.date(),
                date_start__lte=d_en.date()
            )[:30]
        else:
            akts = UnAkt.objects.all().order_by("-id")[:30]
        return {
            'akts': akts,
        }


class QopView(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_moliya/qop_ombor.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super(QopView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(QopView, self).get_context_data(**kwargs)
        qops = Tin.objects.all()
        return {
            "qops":qops
        }


class QopViewActive(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_moliya/qop_ombor_active.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 9:
            return redirect('logout')
        return super(QopViewActive, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(QopViewActive, self).get_context_data(**kwargs)
        qops = Tinhistory.objects.filter(status=1).order_by('-id')
        return {
            "qops":qops
        }


class AktChiqimDetail(DetailView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_moliya/akt_chiqim_detail.html'
    context_object_name = 'akt'
    model = Akt

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [8, 9]:
            return redirect('logout')
        return super(AktChiqimDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AktChiqimDetail, self).get_context_data(**kwargs)
        total_netto = self.get_object().wagons.all().aggregate(total=Sum('netto_fakt')).get('total')
        types_outlay = TypeOutlay.objects.all()
        if total_netto is None:
            total_netto = 0
        context['total_netto'] = total_netto
        context['types'] = types_outlay
        context['dollar'] = Currency.objects.last()
        return context


class UnAktChiqimDetail(DetailView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_moliya/unakt_chiqim_detail.html'
    context_object_name = 'akt'
    model = UnAkt

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [8, 9]:
            return redirect('logout')
        return super(UnAktChiqimDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UnAktChiqimDetail, self).get_context_data(**kwargs)
        total_netto = self.get_object().wagons.all().aggregate(total=Sum('netto_fakt')).get('total')
        types_outlay = TypeOutlay.objects.all()
        if total_netto is None:
            total_netto = 0
        context['total_netto'] = total_netto
        context['types'] = types_outlay
        context['dollar'] = Currency.objects.last()

        return context


def add_type_outlay(request):
    akt_id = request.POST.get('akt_id')
    name = request.POST.get('name')
    TypeOutlay.objects.create(
        name=name
    )
    return redirect('tarozi-moliya-aktlar-chiqim',pk=akt_id)

def add_untype_outlay(request):
    akt_id = request.POST.get('akt_id')
    name = request.POST.get('name')
    TypeOutlay.objects.create(
        name=name
    )
    return redirect('tarozi-moliya-unaktlar-chiqim',pk=akt_id)

#error
def add_qop(request):
    
    try:
        name = request.POST.get('name')
        Qop.objects.create(
            name=name
        )
        return redirect('tarozi-molia-qop-ombor')
    except Exception as err:
        print(err)
        return redirect('tarozi-molia-qop-ombor')

def set_price_qop(request):
    price = request.POST.get('price')
    id = request.POST.get('id')
    qop = Tinhistory.objects.get(id=id)
    qop.price = price
    qop.status = 2
    qop.save()
    tin = Tin.objects.filter(id=id)
    tin.price = price
    tin.save()
    client = ClientTin.objects.get(id=qop.client.id)
    client.debt += qop.price * qop.quantity
    client.save()
    return JsonResponse({})

def add_outlay(request):
    try:
        akt_id = request.POST.get('akt_id')
        type_id = request.POST.get('type_id')
        summa = request.POST.get('summa')
        currency = request.POST.get("currency")
        dollar_narxi = request.POST.get("dollar_narxi1")
        sum = 0
        sum += int(summa) if currency == "usd" else int(summa) / int(dollar_narxi)
        akt = Akt.objects.get(id=akt_id)
        outlay = AktOutlay.objects.create(
            type_id=type_id,
            summa=sum
        )
        akt.total += float(sum)
        akt.save()
        akt.outlay.add(outlay)
        return redirect('tarozi-moliya-aktlar-chiqim', pk=akt_id)
    except Exception as err:
        print(err)
        return redirect('tarozi-moliya-aktlar')

def add_unoutlay(request):
    try:
        akt_id = request.POST.get('akt_id')
        type_id = request.POST.get('type_id')
        summa = request.POST.get('summa')
        currency = request.POST.get("currency")
        dollar_narxi = request.POST.get("dollar_narxi1")
        sum = 0
        sum += int(summa) if currency == "usd" else int(summa) / int(dollar_narxi)
        akt = UnAkt.objects.get(id=akt_id)
        outlay = AktUnOutlay.objects.create(
            type_id=type_id,
            summa=sum
        )
        akt.total += float(sum)
        akt.save()
        akt.outlay.add(outlay)
        return redirect('tarozi-moliya-unaktlar-chiqim',pk=akt_id)
    except Exception as err:
        return redirect('tarozi-moliya-unaktlar')



def set_price(request):
    try:
        akt_id = request.POST.get('akt_id')
        price = request.POST.get('price')
        akt = Akt.objects.get(id=akt_id)
        total_netto = akt.wagons.all().aggregate(total=Sum('netto_fakt')).get('total')
        if total_netto is None:
            total_netto = 0
        client = akt.client
        summa = float(price)*total_netto
        old_sum = akt.price*total_netto
        akt.price = price
        akt.total = float(price)*total_netto
        outlay = akt.outlay.all()
        for i in outlay:
            akt.total += i.summa
        client.debt -= old_sum
        client.debt = client.debt+summa
        akt.save()
        client.save()
        return redirect('tarozi-moliya-aktlar-chiqim', pk=akt_id)
    except:
        return redirect('tarozi-moliya-aktlar')

def set_unprice(request):
    try:
        akt_id = request.POST.get('akt_id')
        price = request.POST.get('price')
        akt = UnAkt.objects.get(id=akt_id)
        total_netto = akt.wagons.all().aggregate(total=Sum('netto_fakt')).get('total')
        if total_netto is None:
            total_netto = 0
        client = akt.client
        summa = float(price)*total_netto
        old_sum = akt.price*total_netto
        akt.price = price
        akt.total = float(price)*total_netto
        outlay = akt.outlay.all()
        for i in outlay:
            akt.total += i.summa
        client.debt -= old_sum
        client.debt = client.debt+summa
        akt.save()
        client.save()
        return redirect('tarozi-moliya-unaktlar-chiqim', pk=akt_id)
    except:
        return redirect('tarozi-moliya-unaktlar')
