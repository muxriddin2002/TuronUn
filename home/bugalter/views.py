from asyncio.log import logger
from datetime import  datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Avg, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from home.models import *
from django.contrib import messages
import json
from decimal import Decimal
import requests
from .functions import sendSmsOneContact
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Sum, Q
from rest_framework.serializers import ModelSerializer
from django.views.generic import TemplateView, ListView
from home.sms_template import *

class Dashboard(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'bugalter/dashboard.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 2:
            return redirect('logout')
        return super(Dashboard, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):  # sourcery no-metrics
        super(Dashboard, self).get_context_data(**kwargs)
        cash = Cash.objects.last()
        cash2 = SecondCash.objects.last()
        qozoq_cash = QozoqCash.objects.last()
        clients = Client.objects.all()
        day = datetime.now()
        month = day.month
        year = day.year
        if month == 12:
            month2 = 1
            year2 = year + 1
        else:
            month2 = month + 1
            year2 = year

        gte = datetime(year, month, 1)
        lte = datetime(year2, month2, 1)
        client_bug = Client.objects.all()
        akt_debt_bug = sum(i.debt for i in client_bug)
        client_un = ClientUn.objects.all()
        akt_debt_un = sum(i.debt for i in client_un)
        customer = Customer.objects.all()
        customer_debt = 0
        our_debt = 0
        for i in customer:
            if i.debt > 0:
                customer_debt += i.debt
            else:
                our_debt -= i.debt
        ac_order = Order.objects.filter(status__in=[1, 2, 3], date__month=month)
        suc_order = Order.objects.filter(status=4, date__month=month)
        neworder = sum(i.summa_total for i in ac_order)
        oldorder = sum(i.summa_total for i in suc_order)
        aqaytuv = Qaytuv.objects.filter(status=1, date__month=month)
        newqaytuv = sum(i.summa_total for i in aqaytuv)
        dqaytuv = Qaytuv.objects.filter(status=2, date__month=month)
        oldqaytuv = sum(i.summa_total for i in dqaytuv)
        dollar = Currency.objects.last()

        nlayout = AktOutlay.objects.filter(status=1, date__month=month)
        olayout = AktOutlay.objects.filter(status=2, date__month=month)
        nw_layout = sum(i.summa for i in nlayout)
        old_layout = sum(i.summa for i in olayout)
        kirim_oylar = {
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
            monthly = Order.objects.filter(date__month=i, date__year=year)
            for income in monthly:
                kirim_oylar[i].append(income.summa_total)
        bugdoykirim_oylar = {
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
            monthly = Akt.objects.filter(date_start__month=i, date_start__year=year)
            for income in monthly:
                wg = income.wagons.all()
                incom = sum(w.netto_fakt * income.price for w in wg)
                bugdoykirim_oylar[i].append(incom)
        chiqim_oylar = {
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
            monthly = Qaytuv.objects.filter(date__month=i, date__year=year)
            for income in monthly:
                chiqim_oylar[i].append(income.summa_total)

        payment = PaymentHistory.objects.filter(type=1)
        incomebank = 0
        incomeplastik = 0
        incomenaqd = 0
        for i in payment:
            if i.turi == '1':
                incomebank += int(i.payment)
            elif i.turi == '2':
                incomeplastik += int(i.payment)
            elif i.turi == '3':
                incomenaqd += int(i.payment)
        payment = PaymentHistory.objects.filter(type=2)
        expansebank = 0
        expanseplastik = 0
        expansenaqd = 0
        for i in payment:
            if i.turi == '1':
                expansebank += int(i.payment)
            elif i.turi == '2':
                expanseplastik += int(i.payment)
            elif i.turi == '3':
                expansenaqd += int(i.payment)

        return {
            'cash': cash,
            'cash2': cash2,
            "expansebank": expansebank,
            "expanseplastik": expanseplastik,
            "expansenaqd": expansenaqd,
            "incomebank": incomebank,
            "incomeplastik": incomeplastik,
            "incomenaqd": incomenaqd,
            "clients": clients,
            "janb": sum(bugdoykirim_oylar[1]),
            "febb": sum(bugdoykirim_oylar[2]),
            "marb": sum(bugdoykirim_oylar[3]),
            "aprb": sum(bugdoykirim_oylar[4]),
            "mayb": sum(bugdoykirim_oylar[5]),
            "junb": sum(bugdoykirim_oylar[6]),
            "julb": sum(bugdoykirim_oylar[7]),
            "augb": sum(bugdoykirim_oylar[8]),
            "sepb": sum(bugdoykirim_oylar[9]),
            "octb": sum(bugdoykirim_oylar[10]),
            "novb": sum(bugdoykirim_oylar[11]),
            "decb": sum(bugdoykirim_oylar[12]),

            "janch": sum(chiqim_oylar[1]),
            "febch": sum(chiqim_oylar[2]),
            "march": sum(chiqim_oylar[3]),
            "aprch": sum(chiqim_oylar[4]),
            "maych": sum(chiqim_oylar[5]),
            "junch": sum(chiqim_oylar[6]),
            "julch": sum(chiqim_oylar[7]),
            "augch": sum(chiqim_oylar[8]),
            "sepch": sum(chiqim_oylar[9]),
            "octch": sum(chiqim_oylar[10]),
            "novch": sum(chiqim_oylar[11]),
            "decch": sum(chiqim_oylar[12]),

            "jank": sum(kirim_oylar[1]),
            "febk": sum(kirim_oylar[2]),
            "mark": sum(kirim_oylar[3]),
            "aprk": sum(kirim_oylar[4]),
            "mayk": sum(kirim_oylar[5]),
            "junk": sum(kirim_oylar[6]),
            "julk": sum(kirim_oylar[7]),
            "augk": sum(kirim_oylar[8]),
            "sepk": sum(kirim_oylar[9]),
            "octk": sum(kirim_oylar[10]),
            "novk": sum(kirim_oylar[11]),
            "deck": sum(kirim_oylar[12]),
            'nw_layout': int(nw_layout),
            'old_layout': int(old_layout),
            'customers': customer,
            'dollar': dollar,
            'akt_debt_bug': akt_debt_bug,
            'akt_debt_un': akt_debt_un,
            'customer_debt': int(customer_debt),
            'our_debt': int(our_debt),
            'neworder': int(neworder),
            'oldorder': int(oldorder),
            'newqaytuv': int(newqaytuv),
            'oldqaytuv': int(oldqaytuv)
        }

def getdashdetailbug(request):
    try:
        start = request.GET.get('start')
        end = request.GET.get('end')
        ac_order = Order.objects.filter(status__in=[1, 2, 3], date__gte=start, date__lte=end)
        suc_order = Order.objects.filter(status=4, date__gte=start, date__lte=end)
        neworder = sum(i.summa_total for i in ac_order)
        oldorder = sum(i.summa_total for i in suc_order)
        aqaytuv = Qaytuv.objects.filter(status=1, date__gte=start, date__lte=end)
        newqaytuv = sum(i.summa_total for i in aqaytuv)
        dqaytuv = Qaytuv.objects.filter(status=2, date__gte=start, date__lte=end)
        oldqaytuv = sum(i.summa_total for i in dqaytuv)
        dt = {
            'neworder': neworder,
            'oldorder': oldorder,
            'newqaytuv': newqaytuv,
            'oldqaytuv': oldqaytuv,

        }
        return JsonResponse(dt)
    except Exception as e:
        logger.error(e)
        return HttpResponse(e)

def getchangechart(request):
    try:
        day = datetime.now()
        year = day.year
        customer_id = request.GET.get('customer')
        customer = Customer.objects.get(id=customer_id)
        kirim_oylar = {
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
            monthly = Order.objects.filter(customer=customer, date__month=i, date__year=year)

            for income in monthly:
                kirim_oylar[i].append(income.summa_total)
        chiqim_oylar = {
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
            monthly = Qaytuv.objects.filter(customer=customer, date__month=i, date__year=year)

            for income in monthly:
                chiqim_oylar[i].append(income.summa_total)

        dt = {
            "jank": sum(kirim_oylar[1]),
            "febk": sum(kirim_oylar[2]),
            "mark": sum(kirim_oylar[3]),
            "aprk": sum(kirim_oylar[4]),
            "mayk": sum(kirim_oylar[5]),
            "junk": sum(kirim_oylar[6]),
            "julk": sum(kirim_oylar[7]),
            "augk": sum(kirim_oylar[8]),
            "sepk": sum(kirim_oylar[9]),
            "octk": sum(kirim_oylar[10]),
            "novk": sum(kirim_oylar[11]),
            "deck": sum(kirim_oylar[12]),

            "janch": sum(chiqim_oylar[1]),
            "febch": sum(chiqim_oylar[2]),
            "march": sum(chiqim_oylar[3]),
            "aprch": sum(chiqim_oylar[4]),
            "maych": sum(chiqim_oylar[5]),
            "junch": sum(chiqim_oylar[6]),
            "julch": sum(chiqim_oylar[7]),
            "augch": sum(chiqim_oylar[8]),
            "sepch": sum(chiqim_oylar[9]),
            "octch": sum(chiqim_oylar[10]),
            "novch": sum(chiqim_oylar[11]),
            "decch": sum(chiqim_oylar[12]),
        }
        return JsonResponse(dt)
    except Exception as e:
        logger.error(e)
        return HttpResponse(e)

class Clients(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'bugalter/bugalter_clients.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [1, 2, 12, 18, 21]:
            return redirect('logout')
        return super(Clients, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Clients, self).get_context_data(**kwargs)
        clients = Customer.objects.all()
        dollar = Currency.objects.last()
        haqdorlik = sum(i.debt for i in clients if i.debt > 0)
        qarzdorlik = sum(i.debt for i in clients if i.debt < 0)
        dollarjs = json.dumps(list(Currency.objects.values('sotish_sum')))
        bank_numbers = BankShots.objects.all()
        return {
            "clients": clients,
            'dollarjs': dollarjs,
            "dollar": dollar,
            "haqdorlik": haqdorlik,
            "qarzdorlik": qarzdorlik,
            'bank_numbers': bank_numbers,
        }

class Bugdoy_hisob(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'bugalter/bugdoy_hisobi.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 2:
            return redirect('logout')
        return super(Bugdoy_hisob, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Bugdoy_hisob, self).get_context_data(**kwargs)
        bugdoy_new = Akt.objects.filter(status=1)
        bugdoy_in_store = Akt.objects.filter(status=2)
        customers = Customer.objects.all()
        dollar = Currency.objects.last()
        akts = []
        akt = Akt.objects.all()
        for akt in akt:
            outlay = akt.outlay.all()
            if paid := [out for out in outlay if out.status == '1']:
                akts.append(akt)
        new_total = 0
        for i in bugdoy_new:
            new = i.wagons.all()
            for wag in new:
                new_total += wag.netto_fakt
        old_total = 0
        for i in bugdoy_in_store:
            old = i.wagons.all()
            for wag in old:
                old_total += wag.netto_fakt
        expenses = 0
        for i in bugdoy_new:
            ex = i.outlay.all()
            for each in ex:
                expenses += each.summa
        return {
            'akts': akts,
            'expenses': int(expenses),
            "bugdoy_in_store": bugdoy_in_store,
            "bugdoy_new": bugdoy_new,
            "customers": customers,
            "dollar": dollar,
            "new_total": new_total,
            "old_total": old_total,
        }

def wheatexpances(request):
    try:
        akts = []
        akt = Akt.objects.all()
        for akt in akt:
            outlay = akt.outlay.all()
            if paid := [out for out in outlay if out.status == '1']:
                akts.append(akt)
        bugdoy_new = Akt.objects.filter(status=1)
        expenses = 0
        for i in bugdoy_new:
            ex = i.outlay.all()
            for each in ex:
                expenses += each.summa
        dollar = Currency.objects.last()

        context = {
            "dollar": dollar,
            'akts': akts,
            'expenses': int(expenses),
        }
        return render(request, 'bugalter/wheatexpances.html', context)
    except Exception as e:
        logger.error(e)
        return HttpResponse(e)

def unexpances(request):
    try:
        akts = []
        akt = UnAkt.objects.all()
        for akt in akt:
            outlay = akt.outlay.all()
            if paid := [out for out in outlay if out.status == '1']:
                akts.append(akt)
        un_new = UnAkt.objects.filter(status=1)
        expenses = 0
        for i in un_new:
            ex = i.outlay.all()
            for each in ex:
                expenses += each.summa
        dollar = Currency.objects.last()
        context = {
            'dollar': dollar,
            'akts': akts,
            'expenses': int(expenses),
        }
        return render(request, 'bugalter/unexpances.html', context)
    except Exception as e:
        logger.error(e)
        return HttpResponse(e)

class Bugdoy_clients(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'bugalter/bugdoy_clients.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [1, 2, 12]:
            return redirect('logout')
        return super(Bugdoy_clients, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Bugdoy_clients, self).get_context_data(**kwargs)

        dollar = Currency.objects.last()
        clients = Client.objects.all()
        summ = clients.aggregate(Sum('debt'))['debt__sum']
        bank_numbers = BankShots.objects.all()
        return {
            'dollar': dollar,
            'clients': clients,
            'summ': summ,
            'bank_numbers':bank_numbers,
        }

class Un_clients(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'bugalter/un_clients.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [1, 2, 12]:
            return redirect('logout')
        return super(Un_clients, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Un_clients, self).get_context_data(**kwargs)
        dollar = Currency.objects.last()
        clients = ClientUn.objects.all()
        bank_numbers = BankShots.objects.all()
        summ = clients.aggregate(Sum('debt'))['debt__sum']
        return {
            'dollar': dollar,
            'clients': clients,
            'summ': summ,
            'bank_numbers':bank_numbers,
        }

class Qop_clients(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'bugalter/qop_clients.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [1, 2, 12]:
            return redirect('logout')
        return super(Qop_clients, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Qop_clients, self).get_context_data(**kwargs)
        dollar = Currency.objects.last()
        clients = ClientTin.objects.all()
        bank_numbers = BankShots.objects.all()
        summ = sum(i.debt for i in clients)
        return {
            'dollar': dollar,
            'clients': clients,
            'summ': summ,
            'bank_numbers':bank_numbers,
        }

class paymentakt(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'bugalter/paymentakt.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 2:
            return redirect('logout')
        return super(paymentakt, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(paymentakt, self).get_context_data(**kwargs)

        dollar = Currency.objects.last()
        akt = Akt.objects.all()
        summ = 0

        return {
            'dollar': dollar,
            'akt': akt,
            'summ':summ,
        }

class Bugalter_vozvrat(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'bugalter/bugalter_vozvrat.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 2:
            return redirect('logout')
        return super(Bugalter_vozvrat, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Bugalter_vozvrat, self).get_context_data(**kwargs)
        dollar = Currency.objects.last()
        client = Customer.objects.all()
        haqdorlik = sum(i.debt for i in client if i.debt > 0)
        qarzdorlik = sum(i.debt for i in client if i.debt < 0)
        qaytuv = Qaytuv.objects.all()
        return {
            "qaytuv": qaytuv,
            "dollar": dollar,
            'haqdorlik': haqdorlik,
            'qarzdorlik': qarzdorlik,

        }

def Bugdoy_akt(request, pk):
    try:
        akt = Akt.objects.get(id=pk)
        total_netto = akt.wagons.all().aggregate(total=Sum('netto_fakt')).get('total')
        types_outlay = TypeOutlay.objects.all()
        if total_netto is None:
            total_netto = 0
        dollar = Currency.objects.last()
        bank_shots = BankShots.objects.all()
        context = {
            'akt':akt,
            'total_netto': total_netto,
            'types': types_outlay,
            'dollar': dollar,
            'bank_numbers': bank_shots,
        }
        return render(request, 'bugalter/bugdoy_akt.html', context)
    except Exception as e:
        logger.error(e)
        return HttpResponse(e)

def Un_akt(request, pk):
    try:
        akt = UnAkt.objects.get(id=pk)
        total_netto = akt.wagons.aggregate(total=Sum('netto_fakt')).get('total')
        types_outlay = TypeOutlay.objects.all()
        if total_netto is None:
            total_netto = 0
        dollar = Currency.objects.last()
        context = {
            'akt':akt,
            'total_netto': total_netto,
            'types': types_outlay,
            'dollar': dollar,
        }
        return render(request, 'bugalter/un_akt.html', context)
    except Exception as e:
        logger.error(e)
        return HttpResponse(e)

def client_informations(request, pk):
    try:
        qaytuv = Qaytuv.objects.get(id=pk)
        dollar = Currency.objects.last()

        context = {
            'qaytuv': qaytuv,
            'dollar': dollar,
        }

        return render(request, 'bugalter/client_informations.html', context)
    except Exception as e:
        logger.error(e)
        return HttpResponse(e)

def paymentclients(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
        payment = PaymentHistory.objects.filter(customer=customer).order_by('-id')
        dollar = Currency.objects.last()
        orders = Order.objects.filter(customer=customer, status = 4).order_by('-id')
        context = {
            'payment': payment,
            'customer':customer,
            'dollar': dollar,
            'orders': orders,
        }

        return render(request, 'bugalter/paymentclients.html', context)
    except Exception as e:
        logger.error(e)
        return HttpResponse(e)

def paymentwheathistory(request, pk):
    try:
        client = Client.objects.get(id=pk)
        payment = PaymentHistory.objects.filter(client=client).order_by('-id')
        dollar = Currency.objects.last()
        context = {
            'payment': payment,
            'client': client,
            'dollar': dollar,
        }
        return render(request, 'bugalter/paymentwheathistory.html', context)
    except Exception as e:
        logger.error(e)
        return HttpResponse(e)

def paymentunhistory(request, pk):
    try:
        client = ClientUn.objects.get(id=pk)
        payment = PaymentHistory.objects.filter(clientun=client).order_by('-id')
        dollar = Currency.objects.last()
        context = {
            'payment': payment,
            'client': client,
            'dollar': dollar,
        }
        return render(request, 'bugalter/paymentunhistory.html', context)
    except Exception as e:
        logger.error(e)
        return HttpResponse(e)

def paymentqophistory(request, pk):
    try:
        client = ClientTin.objects.get(id=pk)
        payment = PaymentHistory.objects.filter(clienttin=client).order_by('-id')
        dollar = Currency.objects.last()
        context = {
            'payment': payment,
            'client': client,
            'dollar': dollar,
        }
        return render(request, 'bugalter/paymentqophistory.html', context)
    except Exception as e:
        logger.error(e)
        return HttpResponse(e)
#kirim
def paymentclient(request): 
    try:
        if request.method == "POST":
            turi = request.POST.get("turi")
            price = request.POST.get("price")
            currency = request.POST.get("currency")
            dollar_narxi = request.POST.get("dollar_narxi1")
            id = request.POST.get("id")
            izoh = request.POST.get("izoh")
            user = request.user
            client = Customer.objects.get(id=id)
            sum = Decimal(0)
            sum += Decimal(price)
            w_kassa = ''
            if user.type == 12: #kassir
                date = request.POST.get("date")

                kassa = request.POST.get("kassa")
                print(kassa, '//////////////////')
                if kassa == 'kassa1':
                    cash = Cash.objects.last()
                    w_kassa = 'Asosiy kassa'
                    if currency == 'usd':
                        client.debt -= Decimal(sum)
                        cash.naqd_pull_dollor += Decimal(sum)
                    else:
                        debt_dollor = Decimal(price) / Decimal(dollar_narxi)
                        client.debt -= Decimal(debt_dollor)
                        cash.naqd_pull_sum += Decimal(sum)
                    cash.save()
                    PaymentHistory.objects.create(customer=client, payment=sum, by_user=user, type=1, turi=turi, currency=dollar_narxi,comment = izoh, cash=cash,  custom_date=date)
                elif kassa == 'kassa3':
                    cash3 = QozoqCash.objects.last()
                    w_kassa = 'Qozoq kassa'
                    if currency == 'usd':
                        client.debt -= Decimal(sum)
                        cash3.naqd_pull_dollor += Decimal(sum)
                    else:
                        debt_dollor = Decimal(price) / Decimal(dollar_narxi)
                        client.debt -= Decimal(debt_dollor)
                        cash3.naqd_pull_sum += Decimal(sum)
                    cash3.save()
                    PaymentHistory.objects.create(customer=client, payment=sum, by_user=user, type=1, turi=turi,currency=dollar_narxi,comment = izoh, cash=cash3,  custom_date=date)
                else: #kassa2
                    cash2 = SecondCash.objects.last()
                    w_kassa = 'Ikkinchi kassa'
                    if currency == 'usd':
                        client.debt -= Decimal(sum)
                        cash2.naqd_pull_dollor += Decimal(sum)
                    else:
                        debt_dollor = Decimal(price) / Decimal(dollar_narxi)
                        client.debt -= Decimal(debt_dollor)
                        cash2.naqd_pull_sum += Decimal(sum)
                    cash2.save()
                    PaymentHistory.objects.create(customer=client, payment=sum, by_user=user, type=1, turi=turi,currency=dollar_narxi,comment = izoh, cash=cash2, custom_date=date)
                client.save()
                #sms kirim
                payment_clint_sms(request, client=client, summa=sum, currency=currency, kassa=w_kassa)

                # format_tuladi = '{:,}'.format(int(sum))
                # user = f'{request.user.first_name} - {request.user.last_name}'
                # if currency == 'usd' and sum >= 1000:
                #     sendSmsOneContact(+998901300444, client.name + " mijozdan: " + format_tuladi  + " $ kirim " + user +" tomondan  "+ w_kassa +" kassaga to'lov qabul qilindi!")
                # elif currency == 'usz' and sum >= 10000000:
                #     sendSmsOneContact(+998901300444, client.name + " mijozdan: " + format_tuladi  + " so'm kirim "+ user +" tomondan "+ w_kassa +" kassaga to'lov qabul qilindi!")
            elif user.type in [2, 21]: #bugalter & yordamchi
                date = request.POST.get("date")
                shot_number = request.POST.get("shot_number")
                bank = BankShots.objects.get(id=shot_number)
                debt_dollor = Decimal(price) / Decimal(dollar_narxi)
                client.debt -= Decimal(debt_dollor)
                bank.bank_sum += Decimal(sum)
                bank.save()
                client.save()
                PaymentHistory.objects.create(customer=client, payment=sum, turi=turi, by_user=user, type=1,  currency=dollar_narxi, comment = izoh, bank_shot = bank.shot_numbers, custom_date=date)
                #sms kirim
                payment_clint_sms(request, client=client, summa=sum, currency=currency, bank=bank)
                # if sum >= 10000000:
                #     format_tuladi = '{:,}'.format(int(sum))
                #     user = f'{request.user.first_name} - {request.user.last_name}'
                #     sendSmsOneContact(+998901300444, client.name + " mijozdan: " + format_tuladi  + " so'm kirim "+ user +" tomondan "+str(bank.bank_name) +" "+ str(bank.shot_numbers) +" bank hisob raqamidan to'lov qabul qilindi!")
            messages.success(request, "To'lov qabul qilindi")
            if user.type == 2:
                return redirect("bugalter_clients")
            else:
                return redirect("yordamchi_bugalter_dashboard")
    except Exception as e:
        logger.error(e)
        messages.error(request, "To'lov qabul qilinmadi")
        return redirect("bugalter_clients")
    
def outincomepayment(request):
    try:
        if request.method == "POST":
            kassa = request.POST.get("kassa")
            turi = request.POST.get("turi")
            money = request.POST.get("money")
            comment = request.POST.get("comment")
            user = request.user
            
            sum = 0
            sum += Decimal(money)
            w_kassa = ''
            if turi == "1": #dollor
                if kassa == "kassa1": #assoiy
                    cash = Cash.objects.last()
                    w_kassa = 'Asosiy kassa'
                    cash.naqd_pull_dollor += Decimal(sum)
                    cash.save()
                    PaymentHistory.objects.create(payment=sum, by_user=request.user, type=1, turi=3, comment=comment, cash = cash)

                elif kassa == "kassa3": #Qozoq kassa
                    cash3 = QozoqCash.objects.last()
                    w_kassa = 'Qozoq kassa'
                    cash3.naqd_pull_dollor += Decimal(sum)
                    cash3.save()
                    PaymentHistory.objects.create(payment=sum, by_user=request.user, type=1, turi=3, comment=comment, cash = cash3)
                else: #2chi kassa
                    cash2 = SecondCash.objects.last()
                    w_kassa = 'Ikkinchi kassa'
                    cash2.naqd_pull_dollor += Decimal(sum)
                    cash2.save()
                    PaymentHistory.objects.create(payment=sum, by_user=request.user, type=1, turi=3, comment=comment, cash = cash2)
                
            else: #sum
                if kassa == "kassa1": #assoiy
                    cash = Cash.objects.last()
                    w_kassa = 'Asosiy kassa'
                    cash.naqd_pull_sum += Decimal(sum)
                    cash.save()
                    PaymentHistory.objects.create(payment=sum, by_user=request.user, type=1, turi=3, comment=comment, cash = cash)
                elif kassa == "kassa3": #assoiy
                    cash3 = QozoqCash.objects.last()
                    w_kassa = 'Qozoq kassa'
                    cash3.naqd_pull_sum += Decimal(sum)
                    cash3.save()
                    PaymentHistory.objects.create(payment=sum, by_user=request.user, type=1, turi=3, comment=comment, cash = cash3)
                else: #2chi kassa
                    cash2 = SecondCash.objects.last()
                    w_kassa = 'Ikkinchi kassa'
                    cash2.naqd_pull_sum += Decimal(sum)
                    cash2.save()
                    PaymentHistory.objects.create(payment=sum, by_user=request.user, type=1, turi=3, comment=comment, cash = cash2)
            messages.success(request, "To'lov qabul qilindi")
            #SMS
            outincomepayment_sms(request, summa=sum, turi=turi, kassa=w_kassa)
            # format_tuladi = '{:,}'.format(int(sum))
            # user = f'{request.user.first_name} - {request.user.last_name}'
            # if turi == '1' and sum >= 1000:
            #     sendSmsOneContact(+998901300444, " Tashqi kirimda:  " + format_tuladi  + " $ kirim " + user +" tomondan  "+ w_kassa +" kassaga to'lov qabul qilindi!")
            # elif turi == '2' and sum >= 10000000:
            #     sendSmsOneContact(+998901300444, "Tashqi kirimda" + format_tuladi  + " so'm kirim "+ user +" tomondan "+ w_kassa +" kassaga to'lov qabul qilindi!")
            return redirect("kassa")
    except Exception as e:
        logger.error(e)
        return HttpResponse(e)


#chiqim
def chiqimpayment(request):
    try:
        if request.method == "POST":
            kassa = request.POST.get("kassa")
            turi = request.POST.get("turi")
            money = request.POST.get("money")
            subcategory = request.POST.get("subcategory")
            comment = request.POST.get("comment")
            user = request.user
            sub_category = ChiqimSubCategory.objects.get(id=subcategory)
            sum = 0
            sum += Decimal(money)
            w_kassa = ''
            if turi == "1": #dollor
                if kassa == "kassa1": #assoiy
                    cash = Cash.objects.last()
                    w_kassa = 'Asosiy kassa'
                    cash.naqd_pull_dollor -= Decimal(sum)
                    cash.save()
                    PaymentHistory.objects.create(payment=sum, by_user=request.user, type=2, turi=3, comment=comment, sub_category=sub_category, cash = cash)

                elif kassa == "kassa3": #Qozoq kassa
                    cash3 = QozoqCash.objects.last()
                    w_kassa = 'Qozoq kassa'
                    cash3.naqd_pull_dollor -= Decimal(sum)
                    cash3.save()
                    PaymentHistory.objects.create(payment=sum, by_user=request.user, type=2, turi=3, comment=comment, sub_category=sub_category, cash = cash3)
                else: #2chi kassa
                    cash2 = SecondCash.objects.last()
                    w_kassa = 'Ikkinchi kassa'
                    cash2.naqd_pull_dollor -= Decimal(sum)
                    cash2.save()
                    PaymentHistory.objects.create(payment=sum, by_user=request.user, type=2, turi=3, comment=comment, sub_category=sub_category, cash = cash2)
            else: #sum
                if kassa == "kassa1": #assoiy
                    cash = Cash.objects.last()
                    w_kassa = 'Asosiy kassa'
                    cash.naqd_pull_sum -= Decimal(sum)
                    cash.save()
                    PaymentHistory.objects.create(payment=sum, by_user=request.user, type=2, turi=3, comment=comment, sub_category=sub_category, cash = cash)
                elif kassa == "kassa3": #assoiy
                    cash3 = QozoqCash.objects.last()
                    w_kassa = 'Qozoq kassa'
                    cash3.naqd_pull_sum -= Decimal(sum)
                    cash3.save()
                    PaymentHistory.objects.create(payment=sum, by_user=request.user, type=2, turi=3, comment=comment, sub_category=sub_category, cash = cash3)
                else: #2chi kassa
                    cash2 = SecondCash.objects.last()
                    w_kassa = 'Ikkinchi kassa'
                    cash2.naqd_pull_sum -= Decimal(sum)
                    cash2.save()
                    PaymentHistory.objects.create(payment=sum, by_user=request.user, type=2, turi=3, comment=comment, sub_category=sub_category, cash = cash2)
            Expanse.objects.create(summa=sum, type=sub_category, izoh=comment)
            
            messages.success(request, "Chiqim qabul qilindi")
            #SMS
            chiqim_payment_sms(request, summa=sum, turi=turi, kassa=w_kassa)
            # format_tuladi = '{:,}'.format(int(sum))
            # user = f'{request.user.first_name} - {request.user.last_name}'
            # if turi == '1' and sum >= 1000:
            #     sendSmsOneContact(+998901300444, " Tashqi chiqimda : " + format_tuladi  + " $ chiqim " + user +" tomondan  "+ w_kassa +" kassadan   qilindi!")
            # elif turi == '2' and sum >= 10000000:
            #     sendSmsOneContact(+998901300444, "Tashqi chiqimda " + format_tuladi  + " so'm chiqim "+ user +" tomondan "+ w_kassa +" kassadan qilindi!")
            return redirect("kassa")
    except Exception as e:
        messages.error(request, "Chiqim qabul qilinmadi!")
        logger.error(e)
        return redirect("kassa")


# convert  sum 2 dollar
def sum_to_dollor(request):  # sourcery skip: last-if-guard
    try:
        if request.method == "POST":
            current_dollor = request.POST.get("current_dollor_sotish_sum")
            suma = request.POST.get("sum_to_dollor")
            kassa = request.POST.get("kassa")

            converted_dollor = Decimal(suma) / Decimal(current_dollor)
            
            if kassa == "kassa1":
                cash = Cash.objects.last()
                if cash.naqd_pull_sum < Decimal(suma):
                    raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                cash.naqd_pull_dollor += Decimal(converted_dollor)
                cash.naqd_pull_sum -= Decimal(suma)
                cash.save()
                ConvertHistory.objects.create(som=converted_dollor,  converter = request.user, to_dollor=True, cash=cash)
            elif kassa == "kassa3":
                cash3 = QozoqCash.objects.last()
                if cash3.naqd_pull_sum < Decimal(suma):
                    raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                cash3.naqd_pull_dollor += Decimal(converted_dollor)
                cash3.naqd_pull_sum -= Decimal(suma)
                cash3.save()
                ConvertHistory.objects.create(som=converted_dollor,  converter = request.user, to_dollor=True, cash=cash3)
            else:
                cash2 = SecondCash.objects.last()
                if cash2.naqd_pull_sum < Decimal(suma):
                    raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                cash2.naqd_pull_dollor += Decimal(converted_dollor)
                cash2.naqd_pull_sum -= Decimal(suma)
                cash2.save()
                ConvertHistory.objects.create(som=converted_dollor,   converter = request.user, to_dollor=True, cash=cash2)


            messages.success(request, f"{suma} dollarga convert  qilindi")
            return redirect("kassa")
    except Exception as e:
        logger.error(e)
        messages.error(request, "Convert amalga oshmadi ")
        return redirect("kassa")
    
# convert  dollor 2 sum
def dollor_to_sum(request):  # sourcery skip: last-if-guard
    try:
        if request.method == "POST":
            current_dollor_olish_sum = request.POST.get("current_dollor_olish_sum")
            dollor = request.POST.get("dollor_to_sum")
            kassa = request.POST.get("kassa")
            
            converted_sum = Decimal(dollor) * Decimal(current_dollor_olish_sum)
            if kassa == "kassa1":
                cash = Cash.objects.last()
                if cash.naqd_pull_dollor < Decimal(dollor):
                    raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                cash.naqd_pull_sum += Decimal(converted_sum)
                cash.naqd_pull_dollor -= Decimal(dollor)
                cash.save()
                ConvertHistory.objects.create(som=converted_sum,   converter = request.user, to_som=True , cash=cash)
            elif kassa == "kassa3":
                cash3 = QozoqCash.objects.last()
                if cash3.naqd_pull_dollor < Decimal(dollor):
                    raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                cash3.naqd_pull_sum += Decimal(converted_sum)
                cash3.naqd_pull_dollor -= Decimal(dollor)
                cash3.save()
                ConvertHistory.objects.create(som=converted_sum,   converter = request.user, to_som=True , cash=cash3)
            else:
                cash2 = SecondCash.objects.last()
                if cash2.naqd_pull_dollor < Decimal(dollor):
                    raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                cash2.naqd_pull_sum += Decimal(converted_sum)
                cash2.naqd_pull_dollor -= Decimal(dollor)
                cash2.save()
                ConvertHistory.objects.create(som=converted_sum,  converter = request.user, to_som=True , cash=cash2)
            messages.success(request, f"{dollor} so'mga convert  qilindi")
            return redirect("kassa")
    except Exception as e:
        logger.error(e)
        messages.error(request, "Convert amalga oshmadi ")
        return redirect("kassa")


def kassa_converts(request):
    try:
        if request.method == "POST":
            from_kassa = request.POST.get("from_kassa")
            to_kassa = request.POST.get("to_kassa")
            currency = request.POST.get("currency")
            summa = request.POST.get("summa")
            izoh = request.POST.get("izoh")
            cash1 = Cash.objects.last()
            cash2 = SecondCash.objects.last()
            cash3 = QozoqCash.objects.last()
            #if 1
            if from_kassa == "kassa1" and to_kassa == "kassa2":
                if currency == "usd":
                    if cash1.naqd_pull_dollor < Decimal(summa):
                        raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                    cash1.naqd_pull_dollor -= Decimal(summa)
                    cash1.save()
                    cash2.naqd_pull_dollor += Decimal(summa)
                    cash2.save()
                    CashConvertHistory.objects.create(som=summa, usd_or_uzs = 1, comment=izoh, converter = request.user, from_cash=cash1.name, to_cash=cash2.name)
                else: #sum
                    if cash1.naqd_pull_sum < Decimal(summa):
                        raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                    cash1.naqd_pull_sum -= Decimal(summa)
                    cash1.save()
                    cash2.naqd_pull_sum += Decimal(summa)
                    cash2.save()
                    CashConvertHistory.objects.create(som=summa, comment=izoh, converter = request.user, usd_or_uzs = 2 , from_cash=cash1.name, to_cash=cash2.name)
            #if 2
            if from_kassa == "kassa1" and to_kassa == "kassa3":
                if currency == "usd":
                    if cash1.naqd_pull_dollor < Decimal(summa):
                        raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                    cash1.naqd_pull_dollor -= Decimal(summa)
                    cash1.save()
                    cash3.naqd_pull_dollor += Decimal(summa)
                    cash3.save()
                    CashConvertHistory.objects.create(som=summa, comment=izoh, converter = request.user, usd_or_uzs = 1 , from_cash=cash1.name, to_cash=cash3.name)
                else: #sum
                    if cash1.naqd_pull_sum < Decimal(summa):
                        raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                    cash1.naqd_pull_sum -= Decimal(summa)
                    cash1.save()
                    cash3.naqd_pull_sum += Decimal(summa)
                    cash3.save()
                    CashConvertHistory.objects.create(som=summa, comment=izoh, converter = request.user, usd_or_uzs = 2 , from_cash=cash1.name, to_cash=cash3.name)
                    #if 3
            if from_kassa == "kassa2" and to_kassa == "kassa1":
                if currency == "usd":
                    if cash2.naqd_pull_dollor < Decimal(summa):
                        raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                    cash2.naqd_pull_dollor -= Decimal(summa)
                    cash2.save()
                    cash1.naqd_pull_dollor += Decimal(summa)
                    cash1.save()
                    CashConvertHistory.objects.create(som=summa, comment=izoh, converter = request.user, usd_or_uzs = 1 , from_cash=cash2.name, to_cash=cash1.name)
                else: #sum
                    if cash2.naqd_pull_sum < Decimal(summa):
                        raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                    cash2.naqd_pull_sum -= Decimal(summa)
                    cash2.save()
                    cash1.naqd_pull_sum += Decimal(summa)
                    cash1.save()
                    CashConvertHistory.objects.create(som=summa, comment=izoh, converter = request.user,usd_or_uzs = 2 , from_cash=cash2.name, to_cash=cash1.name)
            #if 4
            if from_kassa == "kassa2" and to_kassa == "kassa3":
                if currency == "usd":
                    if cash2.naqd_pull_dollor < Decimal(summa):
                        raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                    cash2.naqd_pull_dollor -= Decimal(summa)
                    cash2.save()
                    cash3.naqd_pull_dollor += Decimal(summa)
                    cash3.save()
                    CashConvertHistory.objects.create(som=summa, comment=izoh, converter = request.user, usd_or_uzs = 1 , from_cash=cash2, to_cash=cash3)
                else: #sum
                    if cash2.naqd_pull_sum < Decimal(summa):
                        raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                    cash2.naqd_pull_sum -= Decimal(summa)
                    cash2.save()
                    cash3.naqd_pull_sum += Decimal(summa)
                    cash3.save()
                    CashConvertHistory.objects.create(som=summa, comment=izoh, converter = request.user, usd_or_uzs = 2, from_cash=cash2, to_cash=cash3)
                    
                #if 5
            if from_kassa == "kassa3" and to_kassa == "kassa1":
                if currency == "usd":
                    if cash3.naqd_pull_dollor < Decimal(summa):
                        raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                    cash3.naqd_pull_dollor -= Decimal(summa)
                    cash3.save()
                    cash1.naqd_pull_dollor += Decimal(summa)
                    cash1.save()
                    CashConvertHistory.objects.create(som=summa, comment=izoh, converter = request.user,  usd_or_uzs = 1 , from_cash=cash3.name, to_cash=cash1.name)
                else: #sum
                    if cash3.naqd_pull_sum < Decimal(summa):
                        raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                    cash3.naqd_pull_sum -= Decimal(summa)
                    cash3.save()
                    cash1.naqd_pull_sum += Decimal(summa)
                    cash1.save()
                    CashConvertHistory.objects.create(som=summa, comment=izoh, converter = request.user,  usd_or_uzs = 2 , from_cash=cash3.name, to_cash=cash1.name)
            #if 6
            if from_kassa == "kassa3" and to_kassa == "kassa2":
                if currency == "usd":
                    if cash3.naqd_pull_dollor < Decimal(summa):
                        raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                    cash3.naqd_pull_dollor -= Decimal(summa)
                    cash3.save()
                    cash2.naqd_pull_dollor += Decimal(summa)
                    cash2.save()
                    CashConvertHistory.objects.create(som=summa, comment=izoh, converter = request.user,  usd_or_uzs = 1 , from_cash=cash3, to_cash=cash2)
                else: #sum
                    if cash3.naqd_pull_sum < Decimal(summa):
                        raise Exception("Kiritilgan Dollor, kassadagi dollardan kam")
                    cash3.naqd_pull_sum -= Decimal(summa)
                    cash3.save()
                    cash2.naqd_pull_sum += Decimal(summa)
                    cash2.save()
                    CashConvertHistory.objects.create(som=summa, comment=izoh, converter = request.user,  usd_or_uzs = 2, from_cash=cash3, to_cash=cash2)
        messages.success(request, "Muvaffaqiyatli ko'chirildi")
        return redirect("kassa")
    except Exception as e:
        logger.error(e)
        messages.error(request, "Convert amalga oshmadi ")
        return redirect("kassa")
    
def givepaymentclient(request):
    try:
        if request.method == "POST":
            turi = request.POST.get("turi")
            price = request.POST.get("price")
            currency = request.POST.get("currency")
            dollar_narxi = request.POST.get("dollar_narxi")
            id = request.POST.get("id")
            user = request.user
            sum = 0
            client = Customer.objects.get(id=id)
            cash = Cash.objects.last()
        
            sum += Decimal(price)
            if currency == "usd":
                client.debt += Decimal(sum)
                
                cash.naqd_pull_dollor -=  Decimal(sum)
            else:
                debt_dollor = Decimal(price) / Decimal(dollar_narxi)
                client.debt += Decimal(debt_dollor)
                cash.naqd_pull_sum -=  Decimal(sum)
                
            cash.save()
            client.save()

            PaymentHistory.objects.create(customer=client, payment=sum, by_user=user, type=2, turi=turi)
            
            messages.success(request, "Muvofaqiyatli To'landi")
            # format_tuladi = '{:,}'.format(int(sum))
            #user = f'{request.user.first_name} - {request.user.last_name}'
            # if currency == 'usd' and sum >= 1000:
            #     sendSmsOneContact(+998901300444, "Taminotchisi to'lovi uchun: " + format_tuladi + " $ chiqim amalga oshirildi!")
            # elif currency == 'usz' and sum >= 10000000:
            #     sendSmsOneContact(+998901300444, "Taminotchisi to'lovi uchun: " + format_tuladi + " so'm chiqim amalga oshirildi!")
            return redirect("bugalter_clients")
    except Exception as e:
        logger.error(e)
        messages.error(request, "To'lov qabul qilinmadi")
        return redirect("bugalter_clients")

def paymentoutlay(request):  # sourcery skip: last-if-guard
    if request.method == "POST":
        id = request.POST.get("id")
        turi = request.POST.get("turi")
        user = request.user
        outlay = AktOutlay.objects.get(id=id)
        outlay.status = 2
        outlay.save()
        sum = Decimal(outlay.summa)
        w_kassa = ''
        format_tuladi = '{:,}'.format(int(sum))
        if user.type == 2:
            bank_id = request.POST.get("shot_number")
            bank = BankShots.objects.get(id=bank_id)
            bank.bank_sum -= Decimal(outlay.summa)
            bank.save()

            PaymentHistory.objects.create(payment=outlay.summa, by_user=user, type=2, turi=turi, for_expance=True, bank_shot=bank.shot_numbers)
            #SMS
            paymentoutlay_sms(request, summa=sum, bank=bank)
            # user = f'{request.user.first_name} - {request.user.last_name}'
            # if sum >= 1000:
            #     sendSmsOneContact(+998901300444, " AktOutlay uchun: " + format_tuladi  + " $ chiqim summasi " + user +" tomondan  "+ bank.shot_numbers +" bank hisob raqamidan to'lov  qilindi!")
        else: #kassir
            kassa = request.POST.get("kassa")
            if kassa == 'kassa1':
                cash = Cash.objects.last()
                w_kassa = cash.name
                cash.naqd_pull_dollor -= Decimal(outlay.summa)
                cash.save()
                PaymentHistory.objects.create(payment=outlay.summa, by_user=user, type=2, turi=turi, for_expance=True, cash = cash)
            elif kassa == 'kassa2':
                cash2 = SecondCash.objects.last()
                w_kassa = cash2.name
                cash2.naqd_pull_dollor -= Decimal(outlay.summa)
                cash2.save()
                PaymentHistory.objects.create(payment=outlay.summa, by_user=user, type=2, turi=turi, for_expance=True, cash = cash2)
            else:
                cash3 = QozoqCash.objects.last()
                w_kassa = cash3.name
                cash3.naqd_pull_dollor -= Decimal(outlay.summa)
                cash3.save()
                PaymentHistory.objects.create(payment=outlay.summa, by_user=user, type=2, turi=turi, for_expance=True, cash = cash3)

            paymentoutlay_sms(request, summa=sum, kassa=w_kassa)
            # user = f'{request.user.first_name} - {request.user.last_name}'
            # if sum >= 1000:
            #     sendSmsOneContact(
            #         +998901300444,
            #         f" AktOutlay: {format_tuladi} $ chiqim {user} tomondan  {w_kassa}"
            #         + " kassadan chiqim qilindi!",
            #     )

        messages.success(request, "Muvofaqiyatli to'landi")


        return redirect("wheatexpances")

def paymentunoutlay(request):
    if request.method == "POST":
        id = request.POST.get("id")
        turi = request.POST.get("turi")
        outlay = AktUnOutlay.objects.get(id=id)
        user = request.user
        outlay.status = 2
        outlay.save()
        
        PaymentHistory.objects.create(payment=outlay.summa, by_user=user, type=2, turi=turi, for_expance=True)
        
        cash = Cash.objects.last()
        cash.naqd_pull_dollor -= Decimal(outlay.summa)
        cash.save()
        messages.success(request, "Muvofaqiyatli to'landi")
        return redirect("unexpances")

def paymentforwheat(request):
    '''Function for bugdoy payment(chiqim)'''
    try:
        if request.method == "POST":
            price = request.POST.get("price")
            dollar_narxi = request.POST.get("dollar_narxi")
            id = request.POST.get("id")
            turi = request.POST.get("turi")
            izoh = request.POST.get("izoh")
            currency = request.POST.get("currency")
            user = request.user
            client = Client.objects.get(id=id)
            
            sum = 0
            sum += Decimal(price)
            w_kassa = ''
            if user.type == 12: #kassir
                kassa = request.POST.get("kassa")
                if kassa == 'kassa1':
                    cash = Cash.objects.last()
                    w_kassa = cash.name
                    if currency == 'usd':
                        client.debt -= Decimal(sum)
                        cash.naqd_pull_dollor -= Decimal(sum)
                    else:
                        debt_dollor = Decimal(price) / Decimal(dollar_narxi)
                        client.debt -= Decimal(debt_dollor)
                        cash.naqd_pull_sum -= Decimal(sum)
                    cash.save()
                    PaymentHistory.objects.create(client=client, payment=sum, turi=turi, by_user=user, type=2,  currency=dollar_narxi, comment = izoh, cash = cash)
                elif kassa == 'kassa3':
                    cash3 = QozoqCash.objects.last()
                    w_kassa = cash3.name
                    if currency == 'usd':
                        client.debt -= Decimal(sum)
                        cash3.naqd_pull_dollor -= Decimal(sum)
                    else:
                        debt_dollor = Decimal(price) / Decimal(dollar_narxi)
                        client.debt -= Decimal(debt_dollor)
                        cash3.naqd_pull_sum -= Decimal(sum)
                    cash3.save()
                    PaymentHistory.objects.create(client=client, payment=sum, turi=turi, by_user=user, type=2,  currency=dollar_narxi, comment = izoh, cash = cash3)
                else: #kassa2
                    cash2 = SecondCash.objects.last()
                    w_kassa = cash2.name
                    if currency == 'usd':
                        client.debt -= Decimal(sum)
                        cash2.naqd_pull_dollor -= Decimal(sum)
                    else: #som
                        debt_dollor = Decimal(price) / Decimal(dollar_narxi)
                        client.debt -= Decimal(debt_dollor)
                        cash2.naqd_pull_sum -= Decimal(sum)
                    cash2.save()
                    PaymentHistory.objects.create(client=client, payment=sum, turi=turi, by_user=user, type=2,  currency=dollar_narxi, comment = izoh, cash = cash2)
                client.save()
                #SMS
                paymentforwheat_sms(request, client=client, summa=sum, kassa=w_kassa, currency=currency)
                # format_tuladi = '{:,}'.format(int(sum))
                # user = f'{request.user.first_name} - {request.user.last_name}'
                # if currency == 'usd' and sum >= 1000:
                #     sendSmsOneContact(+998901300444, client.name + " Taminotchiga: " + format_tuladi  + " $ chiqim " + user +" tomondan  "+ w_kassa +" kassadan chiqim qilindi!")
                # elif currency == 'usz' and sum >= 10000000:
                #     sendSmsOneContact(+998901300444, client.name + " Taminotchiga: " + format_tuladi  + " so'm chiqim "+ user +" tomondan "+ w_kassa +" kassadan chiqim qilindi!")
            elif user.type == 2: # bugalter
                shot_number = request.POST.get("shot_number")

                bank = BankShots.objects.get(id=shot_number)
                
                debt_dollor = Decimal(price) / Decimal(dollar_narxi)
                client.debt -= Decimal(debt_dollor)
                bank.bank_sum -= Decimal(sum)
                bank.save()
                client.save()
                PaymentHistory.objects.create(client=client, payment=sum, turi=turi, by_user=user, type=2,  currency=dollar_narxi, comment = izoh, bank_shot = bank.shot_numbers )

                paymentforwheat_sms(request, summa=sum, bank=bank, currency=currency, client=client)
                # user = f'{request.user.first_name} - {request.user.last_name}'
                # format_tuladi = '{:,}'.format(int(sum))
                # if sum >= 1000:
                #     sendSmsOneContact(+998901300444, client.name + " Taminotchiga: " + format_tuladi  + " so'm chiqim "+ user +" tomondan "+str(bank.bank_name) +" "+ str(bank.shot_numbers) +" bank hisob raqamidan to'lov chiqim qilindi!")
            
            messages.success(request, "Muvofaqiyatli to'landi")
            return redirect("bugdoy_clients")
    except Exception as e:
        logger.error(e)
        messages.error(request, "Xatolik")
        return redirect("bugdoy_clients")

def paymentforun(request):
    try:
        if request.method == "POST":
            price = request.POST.get("price")
            dollar_narxi = request.POST.get("dollar_narxi")
            id = request.POST.get("id")
            turi = request.POST.get("turi")
            currency = request.POST.get("currency")
            client = ClientUn.objects.get(id=id)
            user = request.user
            izoh = request.POST.get("izoh")
            sum = 0
            sum += Decimal(price)
            format_tuladi = '{:,}'.format(int(sum))
            
            if user.type == 12:
                kassa = request.POST.get("kassa")
                if kassa == 'kassa1':
                    cash = Cash.objects.last()
                    w_kassa = cash.name
                    if currency == 'usd':
                        client.debt -= Decimal(sum)
                        cash.naqd_pull_dollor -= Decimal(sum)
                    else: #sum
                        debt_dollor = Decimal(price) / Decimal(dollar_narxi)
                        client.debt -= Decimal(debt_dollor)
                        cash.naqd_pull_sum -= Decimal(sum)
                    cash.save()
                    client.save()
                    PaymentHistory.objects.create(clientun=client, payment=sum, turi=turi, by_user=user, type=2,  currency=dollar_narxi, comment = izoh, cash = cash)
                elif kassa == 'kassa3':
                    cash3 = QozoqCash.objects.last()
                    w_kassa = cash3.name
                    if currency == 'usd':
                        client.debt -= Decimal(sum)
                        cash3.naqd_pull_dollor -= Decimal(sum)
                    else: #sum
                        debt_dollor = Decimal(price) / Decimal(dollar_narxi)
                        client.debt -= Decimal(debt_dollor)
                        cash3.naqd_pull_sum -= Decimal(sum)
                    cash3.save()
                    client.save()
                    PaymentHistory.objects.create(clientun=client, payment=sum, turi=turi, by_user=user, type=2,  currency=dollar_narxi, comment = izoh, cash = cash3)
                else: #kassa 2
                    cash2 = SecondCash.objects.last()
                    w_kassa = cash2.name
                    if currency == 'usd':
                        client.debt -= Decimal(sum)
                        cash2.naqd_pull_dollor -= Decimal(sum)
                    else:
                        debt_dollor = Decimal(price) / Decimal(dollar_narxi)
                        client.debt -= Decimal(debt_dollor)
                        cash2.naqd_pull_sum -= Decimal(sum)
                    cash2.save()
                    client.save()
                    PaymentHistory.objects.create(clientun=client, payment=sum, turi=turi, by_user=user, type=2,  currency=dollar_narxi, comment = izoh, cash = cash2)

                paymentforun_sms(request, summa=sum, kassa=w_kassa, currency=currency, client=client)
                # user = f'{request.user.first_name} - {request.user.last_name}'
                # if currency == 'usd' and sum >= 1000:
                #     sendSmsOneContact(+998901300444, client.name + " Taminotchiga: " + format_tuladi  + " $ chiqim " + user +" tomondan  "+ w_kassa +" kassadan chiqim qilindi!")
                # elif currency == 'usz' and sum >= 10000000:
                #     sendSmsOneContact(+998901300444, client.name + " Taminotchiga: " + format_tuladi  + " so'm chiqim "+ user +" tomondan "+ w_kassa +" kassadan chiqim qilindi!")
            elif user.type == 2:
                shot_number = request.POST.get("shot_number")

                bank = BankShots.objects.get(id=shot_number)
                
                debt_dollor = Decimal(price) / Decimal(dollar_narxi)
                client.debt -= Decimal(debt_dollor)
                bank.bank_sum -= Decimal(sum)
                bank.save()
                client.save()
                PaymentHistory.objects.create(clientun=client, payment=sum, turi=turi, by_user=user, type=2,  currency=dollar_narxi, comment = izoh, bank_shot = bank.shot_numbers )

                paymentforun_sms(request, summa=sum, currency=currency, bank=bank, client=client)
                # user = f'{request.user.first_name} - {request.user.last_name}'
                # format_tuladi = '{:,}'.format(int(sum))
                #
                # if sum >= 1000:
                #     sendSmsOneContact(+998901300444, client.name + " Taminotchiga: " + format_tuladi  + " so'm chiqim "+ user +" tomondan "+str(bank.bank_name) +" "+ str(bank.shot_numbers) +" bank hisob raqamidan chiqim qilindi!")
            
            messages.success(request, "Muvofaqiyatli to'landi")
            return redirect("un_clients")
    except Exception as e:
        logger.error(e)
        messages.error(request, "Xatolik")
        return redirect("un_clients")

def paymentforqop(request):
    try:
        if request.method == "POST":
            price = request.POST.get("price")
            dollar_narxi = request.POST.get("dollar_narxi")
            id = request.POST.get("id")
            shot_number = request.POST.get("shot_number")
            turi = request.POST.get("turi")
            currency = request.POST.get("currency")
            user = request.user

            client = ClientTin.objects.get(id=id)
            bank = BankShots.objects.get(id=shot_number)
            cash = Cash.objects.last()

            sum = 0
            sum += Decimal(price)

            if currency == 'usd':
                client.debt -= Decimal(sum)
                cash.naqd_pull_dollor -= sum
            else:
                debt_dollor = Decimal(price) / Decimal(dollar_narxi)
                client.debt -= Decimal(debt_dollor)
                bank.bank_sum -= Decimal(sum)
                cash.naqd_pull_sum -= sum
            bank.save()
            client.save()
            cash.save()
            PaymentHistory.objects.create(clienttin=client, payment=sum, turi=turi, by_user=user, type=2,bank_shot=bank.shot_numbers, currency=dollar_narxi)
            messages.success(request, "Muvofaqiyatli to'landi")
            if sum >= 10000000:
                paymentforqop_sms(request, bank=bank, summa=sum, client=client)
                # user = f'{request.user.first_name} - {request.user.last_name}'
                # format_tuladi = '{:,}'.format(int(sum))
                # sendSmsOneContact(+998901300444, client.name + " Taminotchiga: " + format_tuladi  + " so'm chiqim "+ user +" tomondan "+str(bank.bank_name) +" "+ str(bank.shot_numbers) +" bank hisob raqamidan chiqim qilindi!")
            return redirect("qop_clients")
    except Exception as e:
        logger.error(e)
        messages.error(request, "Xatolik")
        return redirect("qop_clients")

#kurs changer functions
def changekurs(request):  # sourcery skip: last-if-guard
    if request.method == "POST":
        user = request.user
        kurs_api = requests.get('https://nbu.uz/uz/exchange-rates/json/').json()
        api_usd_kurs = Decimal(kurs_api[-1]['cb_price'])
        cell_price = Decimal(kurs_api[-1]['nbu_cell_price'])
        buy_price = Decimal(kurs_api[-1]['nbu_buy_price'])
        currency = Currency.objects.all().last()
        if currency is None:
            Currency.objects.create(sotish_sum=cell_price, olish_sum=buy_price)
        else:
            currency.sotish_sum = cell_price
            currency.olish_sum = buy_price
            currency.save()
        messages.success(request, "Muvofaqiyatli o'zgartirildi")
        if user.type == 2:
            return redirect("bugalter_dashboard")
        elif user.type == 1:
            return redirect("director-dashboard")
        else:
            return redirect('kassir-dashboard')

def addlimit(request):
    try:
        if request.method == "POST":
            print(request.user.type,  '////////////////')

            if request.user.type == 17:
                limit = request.POST.get("limit", 0)
                id = request.POST.get("id")
                customer = Customer.objects.get(id=id)
                print(customer.limit, '(1)')
                customer.limit = limit
                customer.save()
                print(customer.limit, '(2)')
                messages.success(request, "Muvofaqiyatli limit belgilandi")
                return redirect("mijozlar")
            else:
                limit = request.POST['limit']
                client_id = request.POST['id']
                client = Customer.objects.get(id=client_id)
                client.limit = limit
                client.save()
                messages.success(request, "Muvofaqiyatli limit belgilandi")
            return redirect("bugalter_clients")
    except Exception as e:
        logger.error(e)
        if request.user.type == 17:
            return redirect("mijozlar")
        else:
            return redirect("bugalter_clients")

class Sms(LoginRequiredMixin, TemplateView):
    template_name = 'bugalter/sms.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [1, 2,17]:
            return redirect('logout')
        return super(Sms, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(Sms, self).get_context_data(**kwargs)
        context['mijoz'] = Customer.objects.all()
        context['client'] = Client.objects.all()
        context['dollar'] = Currency.objects.last()
        context['sms'] = 'active'
        context['sms_templates'] = SMSTemplate.objects.all()
        return context

def sms_template_status_change(request):
    try:
        pk = int(request.GET.get("pk"))
        val = int(request.GET.get("val"))
        obj = SMSTemplate.objects.get(id=pk)
        newV = val != 0
        obj.active = newV
        obj.save()
        return redirect('sms')
    except:
        return redirect('sms')

def checkPhone(phone):
    try:
        int(phone)
        return (True, phone) if len(phone) == 12 else (False, None)
    except:
        return False, None

def SmsGateway(request):
    if request.method == 'POST':
        sms = request.POST['sms']
        leads_id = request.POST.getlist('leads')
        user = request.user
        customer = Customer.objects.filter(id__in=leads_id)
        success_send_count = 0
        error_send_count = 0
        user = request.user
        for lead in customer:
            Sendedsms.objects.create(employee=user, customer=lead, sms=sms)
            can, phone = checkPhone(lead.phone)
            if can:
                result = sendSmsOneContact(phone, sms)
                if result.status_code == 200:
                    success_send_count += 1
                else:
                    error_send_count += 1
            else:
                error_send_count += 1
        if success_send_count > 0:
            messages.success(request, f"{success_send_count} ta sms jo'natildi!")
        if error_send_count > 0:
            messages.error(request, f"{error_send_count} ta sms jo'natilmadi!")
    return redirect('sms')

class NewSMSTemplate_class(LoginRequiredMixin, TemplateView):
    template_name = 'bugalter/newSmsTemplate.html'


    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [1, 2,17]:
            return redirect('logout')
        return super(NewSMSTemplate_class, self).dispatch(*args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super(NewSMSTemplate_class, self).get_context_data(**kwargs)
        context['customers'] = Customer.objects.all()
        context['dollar'] = Currency.objects.last()
        return context

def editbugclient(request):
    try:
        if request.method == "POST":
            id = request.POST['id']
         
            customer = Customer.objects.get(id=id)
            
            if request.user.type == 18 or request.user.type == 1:
                f_name = request.POST['f_name']
                phone = request.POST['phone']
                lacation = request.POST['address']
                hudud = request.POST['hudud']
                customer.name = f_name
                customer.phone = phone
                customer.location = lacation
                customer.hudud = hudud
                customer.save()
                messages.success(request, "Muvofaqiyatli o'zgartirildi")
                if request.user.type == 18 or request.user.type == 1:
                    return redirect("bugalter_clients")
                else:
                    return redirect("customers")
            else:
                bank = request.POST['bank']
                bank_number = request.POST['bank_number']
                inn = request.POST['inn']
                mfo = request.POST['mfo']
                customer.bank_name = bank
                customer.bank_number = bank_number
                customer.inn = inn
                customer.mfo = mfo
                customer.save()
                messages.success(request, "Muvofaqiyatli o'zgartirildi")
                return redirect("bugalter_clients")
    except Exception as e:
        logger.error(e)
        messages.error(request, "Xatolik")
        return redirect("bugalter_clients")

def edit_payhistory(request):
    try:
        if request.method == "POST":
            id = request.POST.get('id')
            mijoz_id = request.POST.get('mijoz')
            tulov = request.POST.get('tulov')
            date = request.POST.get('date')
            
            history = PaymentHistory.objects.get(id=id)
            history.customer = Customer.objects.get(id=mijoz_id)
            history.payment = tulov
            history.custom_date = date
            history.save()
            
            messages.success(request, "Muvofaqiyatli yangilandi!")
            return redirect("kassa")
    except Exception as e:
        logger.error(e)
        messages.error(request, "Xatolik")
        return redirect("bugalter_clients")


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'hudud', 'phone']

@api_view(['GET'])
def search_lead(request):
    try:
        text = request.GET['text']
        leads = Customer.objects.filter(Q(name__icontains=text) |Q(hudud__icontains=text) |Q(phone__icontains=text))
        return Response(CustomerSerializer(leads, many=True).data)
    except Exception as er:
        return Response([])

@api_view(['POST'])
def save_sms_template(request):
    try:
        name = request.data['name']
        text = request.data['smstext']
        smstype = request.data['sms_type']
        date = request.data['date']
        leads = json.loads(request.data['leads'])
        if request.data.get('pk'):
            pk = int(request.data.get('pk'))
            template = SMSTemplate.objects.get(id=pk)
            template.name = name
            template.text = text
            template.type = smstype
            template.save()
        else:
            template = SMSTemplate.objects. \
                create(name=name, text=text,
                       type=smstype,
                       active=True
                       )
        if smstype == "Bayram va boshqalar":
            template.customer.clear()
            template.customer.set(leads)
            template.date = date
            template.save()
        return Response({})
    except:
        return Response({}, status=500)

sms_special_name = "{{ism}}"
sms_special_phone = "{{tel}}"

def sms_text_replace(sms_text, customer):
    try:
        sms_text = str(sms_text).replace(sms_special_name, customer.name)
    except:
        pass
    try:
        sms_text = str(sms_text).replace(sms_special_phone, customer.phone)
    except:
        pass
    return sms_text

def schedular_sms_send():
    templates = SMSTemplate.objects.filter(
        active=True, type=2,
        date=datetime.now().date()
    )
    for template in templates:
        success_send_count = 0
        error_send_count = 0
        for customer in template.customer.all():
            text = sms_text_replace(template.text, customer)
            can, phone = checkPhone(customer.phone)
            if can:
                result = sendSmsOneContact(customer.phone, text)
                if result.status_code == 200:
                    success_send_count += 1
                else:
                    error_send_count += 1
            else:
                error_send_count += 1

        template.active = False

        is_success = success_send_count == template.customer.count()
        SMSHistory.objects.create(smstemplate=template,
                                  date=template.date,
                                  is_success=is_success,
                                  send_count=success_send_count,
                                  not_send_count=error_send_count
                                  )

def get_lead_template(templates, lead: Customer):  # sourcery skip: use-next
    for template in templates:
        for i in template.customer.all():
            if lead == i:
                return True, template
        return False, None

def birthday_sms_send():
    vaqt = datetime.now().date()
    leads = Customer.objects.filter(
        birthday__day=vaqt.day,
        birthday__month=vaqt.month,)

    templates = SMSTemplate.objects.filter(
        active=True, type=1
    )
    for lead in leads:
        isset, template = get_lead_template(templates, lead)
        if isset:
            can, phone = checkPhone(lead.phone)
            if can:
                text = sms_text_replace(template.text, lead)
                result = sendSmsOneContact(lead.phone, text)
                if result.status_code == 200:
                    lead.sms_send = True
                    lead.save()

#Kassa
class Kassa(LoginRequiredMixin, TemplateView):
    template_name = 'bugalter/kassa.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [1, 12]:
            return redirect('logout')
        return super(Kassa, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(Kassa, self).get_context_data(**kwargs)
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        day = datetime.now()
        # month = day.month
        year = day.year

        today = timezone.now()
        thirty_days_ago = today - timedelta(days=30)
        month = thirty_days_ago.month
        if month == 12:
            month2 = 1
            year2 = year + 1
        else:
            month2 = month + 1
            year2 = year
        gte = datetime(year, month, 1)
        lte = datetime(year2, month2, 1)
        context['dollar'] = Currency.objects.last()
        context['olish_sum'] = Currency.objects.values_list('olish_sum',flat=True).last()
        context['sotish_sum'] = Currency.objects.values_list('sotish_sum',flat=True).last()
        
        context['kassa_dollor'] = Cash.objects.values_list('naqd_pull_dollor',flat=True).last()
        context['kassa_sum'] = Cash.objects.values_list('naqd_pull_sum',flat=True).last()
        context['kassa_total_kirim_avg'] = PaymentHistory.objects.filter(type=1, date__month__gte = month, currency__gt = 1).aggregate(Avg('currency'))['currency__avg']
        
        context['kassa_sum_2'] = SecondCash.objects.values_list('naqd_pull_sum',flat=True).last()
        context['kassa_dollor_2'] = SecondCash.objects.values_list('naqd_pull_dollor',flat=True).last()
        
        context['kassa_sum_3'] = QozoqCash.objects.values_list('naqd_pull_sum',flat=True).last()
        context['kassa_dollor_3'] = QozoqCash.objects.values_list('naqd_pull_dollor',flat=True).last()
        
        context['categories'] = ChiqimCategory.objects.all()
        context['mijozlar'] = Customer.objects.filter(is_active=True).order_by('-name')
        if date_start is not None and date_end is not None:
            d_st = datetime.strptime(date_start, "%m/%d/%Y")
            d_en = datetime.strptime(date_end, "%m/%d/%Y")
            context['kirim_history'] = PaymentHistory.objects.filter(type=1, date__gte=d_st.date(),date__lte=d_en.date()).order_by('-id')
            context['kirim_history_total_sum'] = PaymentHistory.objects.filter(type=1, date__gte=d_st.date(),date__lte=d_en.date()).order_by('-id').aggregate(Sum('payment'))['payment__sum']
            context['chiqim_history'] = PaymentHistory.objects.filter(type=2, date__gte=d_st.date(),date__lte=d_en.date(),  by_user__type = 12).order_by('-id')
            context['chiqim_history_total_sum'] = PaymentHistory.objects.filter(type=2, date__gte=d_st.date(),date__lte=d_en.date(),  by_user__type = 12).order_by('-id').aggregate(Sum('payment'))['payment__sum']
            context['convertHistory'] = ConvertHistory.objects.filter(date__gte=d_st.date(), date__lte=d_en.date()).order_by('-id').aggregate
        else:
            context['kirim_history'] = PaymentHistory.objects.filter(type=1, date__month__gte = month).order_by('-id')
            context['kirim_history_total_sum'] = PaymentHistory.objects.filter(type=1, date__month__gte = month).order_by('-id').aggregate(Sum('payment'))['payment__sum']
            context['chiqim_history'] = PaymentHistory.objects.filter(type=2, date__month__gte = month,  by_user__type = 12).order_by('-id')
            context['chiqim_history_total_sum'] = PaymentHistory.objects.filter(type=2, date__month__gte = month,  by_user__type = 12).order_by('-id').aggregate(Sum('payment'))['payment__sum']
            context['convertHistory'] = ConvertHistory.objects.filter(date__month__gte = month).order_by('-id')
        return context

class BankKassa(ListView, LoginRequiredMixin):   
    login_url = '/login'
    template_name = 'bugalter/bankkassa_list.html'
    model = BankShots

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [1,2,21]:
            return redirect('logout')
        return super(BankKassa, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        super(BankKassa, self).get_context_data(**kwargs)
        dollar = Currency.objects.last()

        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        day = datetime.now()
        # month = day.month
        year = day.year

        today = datetime.today()
        thirty_days_ago = today - timedelta(days=30)
        month = thirty_days_ago.month
        if month == 12:
            month2 = 1
            year2 = year + 1
        else:
            month2 = month + 1
            year2 = year
        gte = datetime(year, month, 1)
        lte = datetime(year2, month2, 1)
        
        if date_start is not None and date_end is not None:
            d_st = datetime.strptime(date_start, "%m/%d/%Y")
            d_en = datetime.strptime(date_end, "%m/%d/%Y")
            orders = Order.objects.filter(
                date__gte=d_st.date(),
                date__lte=d_en.date(),
                status__in=[1, 2, 3]
            )
            passive_orders = Order.objects.filter(
                date__gte=d_st.date(),
                date__lte=d_en.date(),
                status = 4
            )
        else:
            orders = Order.objects.filter(date__month__gte=month, status__in=[1, 2, 3]).order_by('-id')
            passive_orders = Order.objects.filter(date__month=month, status=4).order_by('-id')
        
        hisoblar = BankShots.objects.all()
        
        return {
            'dollar':dollar,
            'hisoblar':hisoblar,
            'orders': orders,
            'passive_orders': passive_orders,
        }


# ajax
def ajax_bank_shots(request):
    try:
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.type not in [1,2,21]:
            return redirect('logout')
        if shot_id := request.GET.get('id'):
            bank_number = BankShots.objects.get(id=shot_id)
            shots = PaymentHistory.objects.filter(bank_shot=bank_number.shot_numbers,type=1).order_by('-id')
            shots_total_sum = PaymentHistory.objects.filter(bank_shot=bank_number.shot_numbers, type=1).order_by('-id').aggregate(Sum('payment'))['payment__sum']
            bank_summa = BankShots.objects.filter(shot_numbers=bank_number.shot_numbers).values_list('bank_sum',flat=True).last()
        context = {
            'shots': shots,
            'bank_summa': bank_summa,
            'shots_total_sum': shots_total_sum,
        }
        return render(request, 'bugalter/shots_ajax.html', context)
    except Exception as e:
        shots = PaymentHistory.objects.filter(type=1, bank_shot__gt = 1).order_by('-id')
        bank_summa = 0
        shots_total_sum = 0
        logger.error(e)
        context = {
            'shots': shots,
            'bank_summa': bank_summa,
            'shots_total_sum': shots_total_sum,
        }
        return render(request, 'bugalter/shots_ajax.html', context)

# ajax
def ajax_bank_chiqim_shots(request):
    try:
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.type not in [1,2,21]:
            return redirect('logout')
        shot_id = request.GET.get('id')
        bank_number = BankShots.objects.get(id=shot_id)
        shots = PaymentHistory.objects.filter(bank_shot=bank_number.shot_numbers,type=2)
        shots_total_sum = PaymentHistory.objects.filter(bank_shot=bank_number.shot_numbers,type=2).aggregate(Sum('payment'))['payment__sum']
    except Exception as e:
        logger.error(e)
        shots_total_sum = 0
        shots = PaymentHistory.objects.filter(type=2, bank_shot__gt = 1)

    context = {
        'shotlar': shots,
        'shots_total_sum': shots_total_sum,
    }
    return render(request, 'bugalter/shots_chiqm_ajax.html', context)

# income ajax
def ajax_bank_shots_data(request):
    try:
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.type not in [1,2,21]:
            return redirect('logout')
        payment = PaymentHistory.objects.filter(type=1, bank_shot__gt = 1 ).order_by('-id')
        shots_total_sum = PaymentHistory.objects.filter(type=1, bank_shot__gt = 1 ).order_by('-id').aggregate(Sum('payment'))['payment__sum']
    except Exception as e:
        logger.error(e)
        HttpResponse(e,status=500)

    context = {
        'payments': payment,
        'shots_total_sum':shots_total_sum
    }
    return render(request, 'bugalter/shots_data_ajax.html', context)

#chiqim ajax
def ajax_bank_shots_chiqim_data(request):
    try:
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.type not in [1,2,21]:
            return redirect('logout')
        payment = PaymentHistory.objects.filter(type=2, bank_shot__gt = 1).order_by('-id')
        shots_total_sum = PaymentHistory.objects.filter(type=2, bank_shot__gt = 1).order_by('-id').aggregate(Sum('payment'))['payment__sum']
    except Exception as e:
        logger.error(e)
        HttpResponse(e,status=500)

    context = {
        'chiqim_payments': payment,
        'shots_total_sum':shots_total_sum
    }
    return render(request, 'bugalter/shots_data_chiqim_ajax.html', context)


#ajax load categorty products yem type
def ajax_load_categories(request):
    try:
        if id := request.GET.get('id'):
            subcategory = ChiqimSubCategory.objects.filter(category_id=id)
        else:
            subcategory = ChiqimSubCategory.objects.all()
    except Exception as e:
        logger.error(e)
        HttpResponse(e, status=500)
    context = {'subcategory': subcategory}
    return render(request, 'kassir/ajax_subcategory.html', context)


#Detail function
def PassiveOrdersDetails(requests, id):
    try:
        dollar = Currency.objects.last()
        orders = Order.objects.filter(id=id)
        baskets = Basket.objects.filter(orderlar=id)
        return render(requests, 'bugalter/passive_orders_details.html', {'baskets': baskets, 'order': orders, 'dollar': dollar})
    except Exception as e:
        logger.error(e)
        HttpResponse(e,status=500)
