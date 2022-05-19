from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import TemplateView

from home.models import *



class Dashboard(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'texnolog/dashboard.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 10:
            return redirect('logout')
        return super(Dashboard, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):  # sourcery no-metrics
        day = datetime.now()
        month = day.month
        year = day.year
        clients = Client.objects.all()
        clientsun = ClientUn.objects.all()
        customers = Customer.objects.all()
        neworders = Order.objects.filter(status=1, date__month=month, date__year=year)
        oldorders = Order.objects.filter(status=4, date__month=month, date__year=year)
        newqaytuvs = Qaytuv.objects.filter(status=1, date__month=month, date__year=year)
        oldqaytuvs = Qaytuv.objects.filter(status=2, date__month=month, date__year=year)
        soldedun = 0
        for bk in oldorders:
            basket = bk.baskets.filter(product__product__type__name__icontains='Un')
            for i in basket:
                soldedun += i.hajmi
        soldedyem = 0
        for bk in oldorders:
            basket = bk.baskets.filter(product__product__type__name__icontains='Yem')
            for i in basket:
                soldedyem += i.hajmi
        activeun = 0
        for bk in neworders:
            basket = bk.baskets.filter(product__product__type__name__icontains='Un')
            for i in basket:
                activeun += i.hajmi
        activeyem = 0
        for bk in neworders:
            basket = bk.baskets.filter(product__product__type__name__icontains='Yem')
            for i in basket:
                activeyem += i.hajmi
        ordersinware = Order.objects.filter(status__in=[2, 3])
        loadingun = 0
        for bk in ordersinware:
            basket = bk.baskets.filter(product__product__type__name__icontains='Un')
            for i in basket:
                loadingun += i.hajmi
        loadingyem = 0
        for bk in ordersinware:
            basket = bk.baskets.filter(product__product__type__name__icontains='Yem')
            for i in basket:
                loadingyem += i.hajmi
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
        return {

            "clientsun": clientsun.count(),
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

            'client': clients,
            'customer': customers,
            'clients': clients.count(),
            'customers': customers.count(),
            'neworders': neworders.count(),
            'oldorders': oldorders.count(),
            'newqaytuvs': newqaytuvs.count(),
            'oldqaytuvs': oldqaytuvs.count(),
            'soldedyem': int(soldedyem),
            'soldedun': int(soldedun),
            'activeun': int(activeun),
            'activeyem': int(activeyem),
            'ordersinware': ordersinware.count(),
            'loadingyem': int(loadingyem),
            'loadingun': int(loadingun),
        }

def getchangecharttex(request):
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


def getdashdetailtexnolog(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    neworders = Order.objects.filter(status=1, date__gte=start, date__lte=end)
    oldorders = Order.objects.filter(status=4, date__gte=start, date__lte=end)
    newqaytuvs = Qaytuv.objects.filter(status=1, date__gte=start, date__lte=end)
    oldqaytuvs = Qaytuv.objects.filter(status=2, date__gte=start, date__lte=end)

    soldedun = 0
    for bk in oldorders:
        basket = bk.baskets.filter(product__product__type__name__icontains='Un')
        for i in basket:
            soldedun += i.hajmi
    soldedyem = 0
    for bk in oldorders:
        basket = bk.baskets.filter(product__product__type__name__icontains='Yem')
        for i in basket:
            soldedyem += i.hajmi

    activeun = 0
    for bk in neworders:
        basket = bk.baskets.filter(product__product__type__name__icontains='Un')
        for i in basket:
            activeun += i.hajmi
    activeyem = 0
    for bk in neworders:
        basket = bk.baskets.filter(product__product__type__name__icontains='Yem')
        for i in basket:
            activeyem += i.hajmi

    ordersinware = Order.objects.filter(status__in=[2, 3], date__gte=start, date__lte=end)
    loadingun = 0
    for bk in ordersinware:
        basket = bk.baskets.filter(product__product__type__name__icontains='Un')
        for i in basket:
            loadingun += i.hajmi
    loadingyem = 0
    for bk in ordersinware:
        basket = bk.baskets.filter(product__product__type__name__icontains='Yem')
        for i in basket:
            loadingyem += i.hajmi
    dt = {
        'neworders': neworders.count(),
        'oldorders': oldorders.count(),
        'newqaytuvs': newqaytuvs.count(),
        'oldqaytuvs': oldqaytuvs.count(),
        'soldedun': int(soldedun),
        'soldedyem': int(soldedyem),
        'activeun': int(activeun),
        'activeyem': int(activeyem),
        'ordersinware': ordersinware.count(),
        'loadingun': loadingun,
        'loadingyem': loadingyem,
    }
    return JsonResponse(dt)



class AktSetQualityView(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'texnolog/aktlar.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [8, 9, 10]:
            return redirect('logout')
        return super(AktSetQualityView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(AktSetQualityView, self).get_context_data(**kwargs)
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        if date_start is not None and date_end is not None:
            d_st = datetime.strptime(date_start, "%m/%d/%Y")
            d_en = datetime.strptime(date_end, "%m/%d/%Y")
            akts = Akt.objects.filter(
                date_end__gt=d_st.date(),
                date_end__lte=d_en.date(),
                status=2
            )[:30]
        else:
            akts = Akt.objects.filter(status=2).order_by("-id")[:30]
            akts = akts.annotate(total_netto=Sum('wagons__netto_fakt'))
        return {
            'akts': akts,
        }

class WheatHistoryView(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'texnolog/bugdoy_history.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [8, 9, 10]:
            return redirect('logout')
        return super(WheatHistoryView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(WheatHistoryView, self).get_context_data(**kwargs)
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        if date_start is not None and date_end is not None:
            d_st = datetime.strptime(date_start, "%m/%d/%Y")
            d_en = datetime.strptime(date_end, "%m/%d/%Y")
            bugdoys = WheatHistory.objects.filter(
                date__gt=d_st.date(),
                date__lte=d_en.date(),
            )[:30]
        else:
            bugdoys = WheatHistory.objects.all().order_by("-id")[:30]
        return {
            'bugdoys': bugdoys,
        }

def akt_set_comment(request):
    try:
        akt_id = request.POST.get('akt_id')
        comment = request.POST.get('comment')
        akt = Akt.objects.get(id=akt_id)
        akt.comment = comment
        akt.save()
        return redirect('texnolog-akt-set-quality')
    except:
        return redirect('texnolog-akt-set-quality')


def add_wheat(request):
    try:
        kilo_1 = request.POST.get('kilo_1')
        WheatHistory.objects.create(
            kilo_1=kilo_1
        )
        return redirect('texnolog-wheats')
    except:
        return redirect('texnolog-wheats')

def edit_wheat(request):
    try:
        id = request.POST.get('id')
        kilo_1 = request.POST.get('kilo_1')
        kilo_2 = request.POST.get('kilo_2')
        kilo_3 = request.POST.get('kilo_3')
        wh = WheatHistory.objects.get(id=id)
        wh.kilo_1 = kilo_1
        wh.kilo_2 = kilo_2
        wh.kilo_3 = kilo_3
        wh.save()
        return redirect('texnolog-wheats')
    except:
        return redirect('texnolog-wheats')

def change_status_wheat(request):
    try:
        id = request.GET.get('id')
        wh = WheatHistory.objects.get(id=id)
        wh.status = True
        wh.save()
        return redirect('texnolog-wheats')
    except:
        return redirect('texnolog-wheats')


class CreateBarcodes(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'texnolog/create_barcodes.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [8, 9, 10]:
            return redirect('logout')
        return super(CreateBarcodes, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(CreateBarcodes, self).get_context_data(**kwargs)
        product = Product.objects.all()
        barcodes = Barcodes.objects.all().order_by('-id')
        return {
            'product': product,
            'barcodes':barcodes,
        }

def add_barcode(request):
    if request.method == "POST":
        pro_id = request.POST.get("pro_id")
        product = Product.objects.get(id=pro_id)
        date1 = request.POST.get("date")

        Barcodes.objects.create(product=product, date=date1)

        return redirect('create_barcodes')

def barcode(request, pk):
    barcode = Barcodes.objects.get(id=pk)

    context = {
        'barcode': barcode,
    }

    return render(request, 'texnolog/barcode.html', context)


def statistics(request):
    product = Product.objects.all()
    tegirmon = Tegirmon.objects.all()
    pr = Tarozi.objects.all().order_by('-id')
    context = {
        "product": product,
        "tegirmon": tegirmon,
        "pr":pr,
    }
    return render(request, 'texnolog/statistics.html', context)


def addtarozisoni(request):
    if request.method == "POST":
        product = request.POST.get('product')
        tegirmon = request.POST.get('tegirmon')
        soni = request.POST.get('soni')
        date = request.POST.get('date')
        Tarozi.objects.create(product_id=product, tegirmon_id=tegirmon, soni=soni, date=date)

        return redirect('statistics')

def difference(request):
    dat = []
    taroz = Tarozi.objects.all().values(
        'product__name', 'date', "tegirmon_id", 'tegirmon__name').annotate(total=Sum('soni'))
    prod = ProductionHistory.objects.all().values(
        'product__name', 'date', "tegirmon_id", 'tegirmon__name').annotate(total=Sum('qopsoni'))
    for t in taroz:
        for p in prod:
            if t['product__name'] == p['product__name'] and t['date'] == p['date'] and t['tegirmon_id'] == p['tegirmon_id']:
                dt = {
                    "product": t['product__name'],
                    "date": t['date'],
                    "tegirmon_id": t['tegirmon_id'],
                    "tegirmon": t['tegirmon__name'],
                    "t_total": t['total'],
                    "p_total": p['total']
                }
                dat.append(dt)
    context = {
        'data': dat
    }
    return render(request, 'texnolog/difference.html', context)


class Brak(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'texnolog/brak.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [1, 10]:
            return redirect('logout')
        return super(Brak, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Brak, self).get_context_data(**kwargs)
        products = Return_product.objects.filter(status=2)
        return {
            'products': products,
        }
