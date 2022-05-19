from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib import messages
from home.models import *
from django.db.models import Sum
#import timezone
from django.utils import timezone
class Dashboard(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'kassir/dashboard.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 12:
            return redirect('logout')
        return super(Dashboard, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Dashboard, self).get_context_data(**kwargs)
        dollar = Currency.objects.last()
        clients = Client.objects.all()
        cash = Cash.objects.last()
        cash2 = SecondCash.objects.last()
        cash3 = QozoqCash.objects.last()
        day = datetime.now()
        
        today = datetime.today()
        thirty_days_ago = today - timedelta(days=20)
        month = thirty_days_ago.month
        # month = day.month
        year = day.year
        if month == 12:
            month2 = 1
            year2 = year + 1
        else:
            month2 = month + 1
            year2 = year
        
        akt_debt = Client.objects.all().aggregate(Sum('debt'))['debt__sum']
        customer = Customer.objects.all()
        customer_debt = 0
        our_debt = 0
        for i in customer:
            if i.debt > 0:
                customer_debt += i.debt
            else:
                our_debt -= i.debt
        neworder = Order.objects.filter(status__in=[1, 2, 3], date__month=month).aggregate(Sum('summa_total'))['summa_total__sum']
        oldorder = Order.objects.filter(status = 4, date__month=month).aggregate(Sum('summa_total'))['summa_total__sum']
        newqaytuv =Qaytuv.objects.filter(status=1, date__month=month).aggregate(Sum('summa_total'))['summa_total__sum']
        oldqaytuv = Qaytuv.objects.filter(status=2, date__month=month).aggregate(Sum('summa_total'))['summa_total__sum']
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
        payment_chiqim = PaymentHistory.objects.filter(type=2)
        expansebank = 0
        expanseplastik = 0
        expansenaqd = 0
        for i in payment_chiqim:
            if i.turi == '1':
                expansebank += int(i.payment)
            elif i.turi == '2':
                expanseplastik += int(i.payment)
            elif i.turi == '3':
                expansenaqd += int(i.payment)
        return {
            'dollar': dollar,
            "cash": cash,
            "cash2": cash2,
            "cash3": cash3,
            "expansebank": expansebank,
            "expanseplastik": expanseplastik,
            "expansenaqd": expansenaqd,
            "incomebank": incomebank,
            "incomeplastik": incomeplastik,
            "incomenaqd": incomenaqd,
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
            'akt_debt': akt_debt,
            'customer_debt': int(customer_debt),
            'our_debt': int(our_debt),
            'neworder': neworder,
            'oldorder': oldorder,
            'newqaytuv': newqaytuv,
            'oldqaytuv': oldqaytuv
        }

def getdashdetailkassa(request):
    date_start = request.GET.get('start')
    date_end = request.GET.get('end')
    start = datetime.strptime(date_start, "%Y-%m-%d")
    end = datetime.strptime(date_end, "%Y-%m-%d")
    ac_order = Order.objects.filter(status__in=[1, 2, 3], date__gte=start, date__lte=end)
    suc_order = Order.objects.filter(status=4, date__gte=start, date__lte=end)
    neworder = sum(i.summa_total for i in ac_order)
    oldorder = sum(i.summa_total for i in suc_order)
    aqaytuv = Qaytuv.objects.filter(status=1, date__gte=start, date__lte=end)
    newqaytuv = sum(i.summa_total for i in aqaytuv)
    dqaytuv = Qaytuv.objects.filter(status=2, date__gte=start, date__lte=end)
    oldqaytuv = sum(i.summa_total for i in dqaytuv)
    unnew = UnAkt.objects.filter(status=1, date_start__gte=start, date_start__lte=end)
    un_new = sum(un.wagons.all().count() for un in unnew)
    unold = UnAkt.objects.filter(status=2, date_start__gte=start, date_start__lte=end)
    un_old = sum(un.wagons.all().count() for un in unold)
    dt = {
        'un_new': un_new,
        'un_old': un_old,
        'neworder': neworder,
        'oldorder': oldorder,
        'newqaytuv': newqaytuv,
        'oldqaytuv': oldqaytuv,
    }
    return JsonResponse(dt)


def expance(request):
    try:
        dollar = Currency.objects.last()
        type = TypeExpanse.objects.all()
        expance = Expanse.objects.all().order_by('-id')
        context = {
            "dollar": dollar,
            "type": type,
            "expance": expance,
        }
    except Exception as e:
        print(e)
        context = {}
    return render(request, 'kassir/expance.html', context)

def addtypeexpanse(request):
    try:
        if request.method == "POST":
            name = request.POST.get('name')
            categories = request.POST.get('categories')
            cat = ChiqimCategory.objects.get(id=categories)
            ChiqimSubCategory.objects.create(name = name, category=cat)
            TypeExpanse.objects.create(name=name)
            messages.success(request, 'Category qo\'shildi')
            return redirect('kassa')
    except Exception as e:
        return redirect('kassa')

def addexpanse(request):
    if request.method == "POST":
        type_id = request.POST.get('type_id')
        summa = request.POST.get('summa')
        currency = request.POST.get("currency")
        dollar_narxi = request.POST.get("dollar_narxi1")
        izoh = request.POST.get("izoh")
        sum = 0
        sum += int(summa) if currency == "usd" else int(summa) / int(dollar_narxi)
        Expanse.objects.create(type_id=type_id, summa=sum, izoh=izoh)
        return redirect('expance')
