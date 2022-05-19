from datetime import datetime
from django.db.models import F, Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.template import context
from django.views.generic import TemplateView, DetailView
from django.http import JsonResponse
#model
from home.models import *
from django.db.models import Avg, Max, Min, Sum
from django.contrib import messages

class Dashboard(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'director/dashboard.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 1:
            return redirect('logout')
        return super(Dashboard, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):  # sourcery no-metrics
        super(Dashboard, self).get_context_data(**kwargs)
        dollar = Currency.objects.last()
        clients = Client.objects.all()
        cash = Cash.objects.last()
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
        
        akt_debt = Client.objects.aggregate(Sum('debt'))['debt__sum']
        
        customer = Customer.objects.all()
        customer_debt = 0
        our_debt = 0
        for i in customer:
            if i.debt > 0:
                customer_debt += i.debt
            else:
                our_debt -= i.debt
                
        neworder = Order.objects.filter(status__in=[1, 2, 3], date__month=month).aggregate(Sum('summa_total'))['summa_total__sum']
        oldorder = Order.objects.filter(status=4, date__month=month).aggregate(Sum('summa_total'))['summa_total__sum']
            
        newqaytuv = Qaytuv.objects.filter(status=1, date__month=month).aggregate(Sum('summa_total'))['summa_total__sum']
        oldqaytuv = Qaytuv.objects.filter(status=2, date__month=month).aggregate(Sum('summa_total'))['summa_total__sum']
            
        nw_layout = AktOutlay.objects.filter(status=1, date__month=month).aggregate(Sum('summa'))['summa__sum']
        old_layout = AktOutlay.objects.filter(status=2, date__month=month).aggregate(Sum('summa'))['summa__sum']
        
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
                
        un_new = 0
        unnew = UnAkt.objects.filter(status=1)
        for un in unnew:
            un_new += un.wagons.all().count()

        unold = UnAkt.objects.filter(status=2)
        un_old = sum(un.wagons.all().count() for un in unold)
        client_un_yem = Customer.objects.all()
        client_un = ClientUn.objects.all()
        client_bugdoy = Client.objects.all()
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
            "cash":cash,
            "expansebank": expansebank,
            "expanseplastik": expanseplastik,
            "expansenaqd": expansenaqd,
            "incomebank": incomebank,
            "incomeplastik": incomeplastik,
            "incomenaqd": incomenaqd,
            'client_un_yem': client_un_yem.count(),
            'client_un': client_un.count(),
            'client_bugdoy': client_bugdoy.count(),
            "un_new": un_new,
            "un_old": un_old,
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
            'nw_layout': nw_layout,
            'old_layout': old_layout,
            'customers': customer,
            'akt_debt': akt_debt,
            'customer_debt': customer_debt,
            'our_debt': our_debt,
            'neworder': neworder,
            'oldorder': oldorder,
            'newqaytuv': newqaytuv,
            'oldqaytuv': oldqaytuv,
            'dollar': dollar,
        }

def getchangechartdashbug(request):
    day = datetime.now()
    month = day.month
    year = day.year
    client_id = request.GET.get('client')
    client = Client.objects.get(id=client_id)

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
        monthly = Akt.objects.filter(client=client, date_start__month=i, date_start__year=year)
        for income in monthly:
            wg = income.wagons.all()
            incom = sum(w.netto_fakt * income.price for w in wg)
            bugdoykirim_oylar[i].append(incom)

    dt = {
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
    }
    return JsonResponse(dt)

def getchangechartdash(request):
    day = datetime.now()
    month = day.month
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
    dollar = Currency.objects.last()
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
        # "dollar": dollar,

    }
    return JsonResponse(dt)


class Customers(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'director/customers.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [1, 4, 17]:
            return redirect('logout')
        return super(Customers, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Customers, self).get_context_data(**kwargs)
        user = self.request.user
        if user.type == 4:
            # customer = Customer.objects.filter(
            #     Q(employe=user)).order_by('-id')
            customer= Customer.objects.filter(Q(employe=user)).annotate(ordering=F('limit') - F('debt')).order_by('ordering')
        else:
            customer= Customer.objects.annotate(ordering=F('limit') - F('debt')).order_by('ordering')
            # customer = Customer.objects.all().order_by('-id')
        haqdorlik = sum(i.debt for i in customer if i.debt > 0)
        qarzdorlik = sum(i.debt for i in customer if i.debt < 0)
        categories = Category.objects.all()
        dollar = Currency.objects.last()

        return {
            'haqdorlik': haqdorlik,
            'qarzdorlik': qarzdorlik,
            'customer': customer,
            'categories': categories,
            'dollar': dollar,
        }

#mijoz detail
def mijoz_detail(request,id):
    try:
        # if not request.user.is_authenticated:
        #     return redirect('login')
        # if request.user.type not in [1, 4, 18]:
        #     return redirect('logout')
        customer = get_object_or_404(Customer, pk=id)
        if request.user.type == 4:
            orders = Order.objects.filter(customer__name=customer, seller__type=request.user.type)
        else:
            orders = Order.objects.filter(customer__name=customer)
        payments = PaymentHistory.objects.filter(customer=customer)
        dollar = Currency.objects.last()
            
        context = {
            'orders':orders,
            'customer':customer,
            'payments': payments,
            'dollar': dollar,
            
        }
        return render(request,'director/customers_detail.html',context)

    except Exception as e:
        print(e)
        return redirect('customers')
#block customer who debt more than limit
def blocked(request,id):
    try:
        if request.user.type == 1:  
            customer = get_object_or_404(Customer, pk=id)
            customer.is_active = customer.is_active == False
            customer.save()
            messages.success(request, 'Bajarildi')
            return redirect('customers')
    except Exception as e:
        print(e)
        messages.error(request, 'Xatolik')
        return redirect('customers')

class Clients(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'director/clients.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 1:
            return redirect('logout')
        return super(Clients, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Clients, self).get_context_data(**kwargs)
        clients = Client.objects.all()
        summ = clients.aggregate(Sum('debt'))['debt__sum']
        dollar = Currency.objects.last()
        return {
            'clients': clients,
            'summ': summ,
            'dollar': dollar,
        }

class Clientsun(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'director/clientun.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 1:
            return redirect('logout')
        return super(Clientsun, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Clientsun, self).get_context_data(**kwargs)
        clients = ClientUn.objects.all()
        summ = clients.aggregate(Sum('debt'))['debt__sum']
        dollar = Currency.objects.last()
        return {
            'clients': clients,
            'summ': summ,
            'dollar': dollar,
        }
