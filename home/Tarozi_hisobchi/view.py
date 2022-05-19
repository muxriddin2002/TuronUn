from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from django.http import JsonResponse

from home.models import Akt, Client, Branch, AktWagon, Store, Order, Product, UnAkt, AktUnWagon, ClientUn, Tegirmon

class Dashboard(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_hisobchi/dashboard.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 8:
            return redirect('logout')
        return super(Dashboard, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Dashboard, self).get_context_data(**kwargs)
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
            monthly = Akt.objects.filter(status=2, date_start__month=i, date_start__year=year).count()
            akt_oylar[i].append(monthly)

        aktun_oylar = {
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
            monthly = UnAkt.objects.filter(status=2, date_start__month=i, date_start__year=year).count()

            aktun_oylar[i].append(monthly)

        client_bugdoy = Client.objects.all()
        client_un = ClientUn.objects.all()

        return {
            "client_bugdoy": client_bugdoy.count(),
            "client_un": client_un.count(),
            "clientun": client_un,
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

            "janc": sum(aktun_oylar[1]),
            "febc": sum(aktun_oylar[2]),
            "marc": sum(aktun_oylar[3]),
            "aprc": sum(aktun_oylar[4]),
            "mayc": sum(aktun_oylar[5]),
            "junc": sum(aktun_oylar[6]),
            "julc": sum(aktun_oylar[7]),
            "augc": sum(aktun_oylar[8]),
            "sepc": sum(aktun_oylar[9]),
            "octc": sum(aktun_oylar[10]),
            "novc": sum(aktun_oylar[11]),
            "decc": sum(aktun_oylar[12]),

            'clients': clients,
            'old_wagons': old_wagons,
            'new_wagons': new_wagons,
            'total_yem': int(total_yem),
            'total_un': int(total_un),

        }

def getchangechartdashun(request):
    day = datetime.now()
    month = day.month
    year = day.year
    client_id = request.GET.get('client')
    client = ClientUn.objects.get(id=client_id)

    unkirim_oylar = {
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
        monthly = UnAkt.objects.filter(client=client, date_start__month=i, date_start__year=year).count()
        unkirim_oylar[i].append(monthly)

    dt = {
        "janb": sum(unkirim_oylar[1]),
        "febb": sum(unkirim_oylar[2]),
        "marb": sum(unkirim_oylar[3]),
        "aprb": sum(unkirim_oylar[4]),
        "mayb": sum(unkirim_oylar[5]),
        "junb": sum(unkirim_oylar[6]),
        "julb": sum(unkirim_oylar[7]),
        "augb": sum(unkirim_oylar[8]),
        "sepb": sum(unkirim_oylar[9]),
        "octb": sum(unkirim_oylar[10]),
        "novb": sum(unkirim_oylar[11]),
        "decb": sum(unkirim_oylar[12]),
    }
    return JsonResponse(dt)

def Getdashdetail(request):
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


    dt = {
        'old_wagons': old_wagons,
        'new_wagons': new_wagons,
        'total_yem': total_yem,
        'total_un': total_un,
    }
    return JsonResponse(dt)

def getchangechartdashtar(request):
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
        monthly = Akt.objects.filter(client=client, date_start__month=i, date_start__year=year).count()
        bugdoykirim_oylar[i].append(monthly)
        print(monthly)

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
#ajax load tegirmon products un type
def ajax_load_tegirmon_products_un(request):
    try:
        tegirmon_id = request.GET.get('tegirmon')
        products = Store.objects.filter(tegirmon_id=tegirmon_id, product__type__name="Un").order_by('id')
    except Exception:
        products = Store.objects.filter(product__type__name="Un")
    return render(request, 'tarozi_hisobchi/ajax_products.html', {'products': products})

#ajax load tegirmon products yem type
def ajax_load_tegirmon_yem(request):
    try:
        tegirmon_id = request.GET.get('tegirmon')
        products = Store.objects.filter(tegirmon_id=tegirmon_id, product__type__name="Yem").order_by('id')
    except Exception:
        products = Store.objects.filter(product__type__name="Yem").order_by('id')
    return render(request, 'tarozi_hisobchi/ajax_products_yem.html', {'productlar': products})

class UnOmborView(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_hisobchi/un_ombori.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [1, 8, 9, 10, 4]:
            return redirect('logout')
        return super(UnOmborView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UnOmborView, self).get_context_data(**kwargs)
        context['uns'] = Store.objects.filter(product__type__name="Un")
        context['tegirmon'] = Tegirmon.objects.all()
        
        return context

class YemOmborView(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_hisobchi/yem_ombor.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [1, 8, 9, 10, 4]:
            return redirect('logout')
        return super(YemOmborView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(YemOmborView, self).get_context_data(**kwargs)
        yems = Store.objects.filter(product__type__name="Yem")
        tegirmon =  Tegirmon.objects.all()
        return {
            "yems": yems,
            'tegirmon': tegirmon
        }

class ClientView(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_hisobchi/client_hisoboti.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        print(self.request.user.type)
        if self.request.user.type not in [8, 9, 10]:
            return redirect('logout')
        return super(ClientView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(ClientView, self).get_context_data(**kwargs)
        search = self.request.GET.get('search')
        if search is not None:
            clients = Client.objects.filter(Q(compony__icontains=search)|Q(name__icontains=search)|Q(phone__icontains=search)|Q(address__icontains=search))
        else:
            clients = Client.objects.all()
        return {
            "clients": clients
        }

class ClientunView(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_hisobchi/client_hisobotiun.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [8, 9, 10]:
            return redirect('logout')
        return super(ClientunView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(ClientunView, self).get_context_data(**kwargs)
        search = self.request.GET.get('search')
        if search is not None:
            clients = ClientUn.objects.filter(Q(compony__icontains=search)|Q(name__icontains=search)|Q(phone__icontains=search)|Q(address__icontains=search))
        else:
            clients = ClientUn.objects.all()
        return {
            "clients": clients
        }

class UnView(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_hisobchi/un_list.html'
    #check user type and redirect to logout
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 8:
            return redirect('logout')
        return super(UnView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(UnView, self).get_context_data(**kwargs)
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
            akts = UnAkt.objects.all().order_by("-id")[:30]
        
        
        client = ClientUn.objects.all()
        ombors = Tegirmon.objects.all()
        return {
            'akts': akts,
            'clients': client,
            'ombors': ombors,
        }

class AktView(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_hisobchi/akt_list.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 8:
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
        clients = Client.objects.all()
        branchs = Tegirmon.objects.all()
        return {
            'akts': akts,
            'clients': clients,
            'branchs': branchs
        }

class AktHisobot(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_hisobchi/akt_hisobot.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [8, 9, 10]:
            return redirect('logout')
        return super(AktHisobot, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(AktHisobot, self).get_context_data(**kwargs)
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
        return {
            'akts': akts,
        }

class AktHisobotDetail(DetailView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'tarozi_hisobchi/akt_hisobot_detail.html'
    context_object_name = 'akt'
    model = Akt

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [8, 9, 10]:
            return redirect('logout')
        return super(AktHisobotDetail, self).dispatch(*args, **kwargs)
# create un akt
def create_akt_un(request):
    try:
        product = request.POST.get('product')
        
        num1 = request.POST.get('num1')
        num2 = request.POST.get('num2')
        
        date_start = request.POST.get('date_start')
        stansiya = request.POST.get('stansiya')
        client_id = request.POST.get('client')
        branch_id = request.POST.get('branch')
        UnAkt.objects.create(
            stansiya=stansiya,
            client_id=client_id,
            ombor_id=branch_id,
            date_start=date_start,
            num1=num1,
            num2=num2
        )
        return redirect('un-list')
    except Exception as err:
        print(err)
        return redirect('un-list')

def create_akt_post(request):
    try:
        name = request.POST.get('name')
        date_start = request.POST.get('date_start')
        stansiya = request.POST.get('stansiya')
        client_id = request.POST.get('client')
        branch_id = request.POST.get('branch')
        Akt.objects.create(
            name=name,
            stansiya=stansiya,
            client_id=client_id,
            branch_id=branch_id,
            date_start=date_start
        )
        return redirect('akt-list')
    except Exception as err:
        print(err)
        return redirect('akt-list')
# AKT un detail  view
def aktun_detail(request):
    try:
        akt_id = request.GET.get('akt')
        product = Product.objects.all()
        akt = UnAkt.objects.get(id=akt_id)
        
        context = {
            "akt": akt,
            "product":product,
        }
        return render(request, 'tarozi_hisobchi/create_aktun.html', context)
    except Exception as err:
        print(err)
        return redirect('un-list')
#detail akt
def akt_detail(request):
    try:
        akt_id = request.GET.get('akt')
        akt = Akt.objects.get(id=akt_id)
        context = {
            "akt": akt
        }
        return render(request, 'tarozi_hisobchi/create_akt.html', context)
    except Exception as err:
        return redirect('akt-list')
# AktUnWagon create
def aktun_detail_post(request):
    try:
        product_id = request.POST.get('product')
        
        vg_raqami = request.POST.get('number')
        brutto = request.POST.get('brutto')
        tara = request.POST.get('tara')
        netto = request.POST.get('netto')
        akt_id = request.POST.get('akt')
        
        akt = UnAkt.objects.get(id=akt_id)
        bg = AktUnWagon.objects.create(
            number=vg_raqami,
            brutto_akt=brutto,
            tara_akt=tara,
            netto_akt=netto,
            product_id=product_id,
        )
        
        akt.wagons.add(bg)
        akt.save()
        url = "/tarozi-hisobchi/aktun-detail?akt=" + str(akt_id)
        return redirect(url)
    except Exception as err:
        print(err)
        return redirect('un-list')

def akt_detail_post(request):
    try:
        vg_raqami = request.POST.get('number')
        brutto = request.POST.get('brutto')
        tara = request.POST.get('tara')
        netto = request.POST.get('netto')
        akt_id = request.POST.get('akt')
        akt = Akt.objects.get(id=akt_id)
        bg = AktWagon.objects.create(
            number=vg_raqami,
            brutto_akt=brutto,
            tara_akt=tara,
            netto_akt=netto
        )
        akt.wagons.add(bg)
        akt.save()
        url = "/tarozi-hisobchi/akt-detail?akt=" + str(akt_id)
        return redirect(url)
    except Exception as err:
        print(err)
        return redirect('akt-list')
#wagon un detail
def aktun_detail_edit(request):
    try:
        product_edit = request.POST.get('product_edit')
        vg_raqami = request.POST.get('number_edit')
        brutto = request.POST.get('brutto_edit')
        tara = request.POST.get('tara_edit')
        netto = request.POST.get('netto_edit')
        akt_id = request.POST.get('akt')
        vg_id = request.POST.get('vg_id')
        wg = AktUnWagon.objects.get(id=vg_id)
        wg.number = vg_raqami
        wg.brutto_akt = brutto
        wg.tara_akt = tara
        wg.netto_akt = netto
        #new update product
        wg.product_id = product_edit
        wg.save()
        url = "/tarozi-hisobchi/aktun-detail?akt=" + str(akt_id)
        return redirect(url)
    except Exception as err:
        print(err)
        return redirect('un-list')

def akt_detail_edit(request):
    try:
        vg_raqami = request.POST.get('number_edit')
        brutto = request.POST.get('brutto_edit')
        tara = request.POST.get('tara_edit')
        netto = request.POST.get('netto_edit')
        akt_id = request.POST.get('akt')
        vg_id = request.POST.get('vg_id')
        wg = AktWagon.objects.get(id=vg_id)
        wg.number = vg_raqami
        wg.brutto_akt = brutto
        wg.tara_akt = tara
        wg.netto_akt = netto
        wg.save()
        url = "/tarozi-hisobchi/akt-detail?akt=" + str(akt_id)
        return redirect(url)
    except Exception as err:
        print(err)
        return redirect('akt-list')

def aktun_detail_delete(request):
    try:
        vg_id = request.GET.get("vg_id")
        akt_id = request.GET.get('akt_id')
        wg = AktUnWagon.objects.get(id=vg_id)
        wg.delete()
        url = "/tarozi-hisobchi/aktun-detail?akt=" + str(akt_id)
        return redirect(url)
    except Exception as err:
        print(err)
        return redirect('un-list')

def akt_detail_delete(request):
    try:
        vg_id = request.GET.get("vg_id")
        akt_id = request.GET.get('akt_id')
        wg = AktWagon.objects.get(id=vg_id)
        wg.delete()
        url = "/tarozi-hisobchi/akt-detail?akt=" + str(akt_id)
        return redirect(url)
    except Exception as err:
        print(err)
        return redirect('akt-list')
#create cliene for yem
def craeteclient(request):
    if request.method == "POST":
        r = request.POST.get
        compony = r("compony")
        name = r("name")
        hudud = r("hudud")
        phone = r("phone")
        Client.objects.create(compony=compony, name=name, address=hudud, phone=phone)
    return redirect('clients')
#create cliene for un
def craeteclientun(request):
    if request.method == "POST":
        r = request.POST.get
        compony = r("compony")
        name = r("name")
        hudud = r("hudud")
        phone = r("phone")
        ClientUn.objects.create(compony=compony, name=name, address=hudud, phone=phone)
    return redirect('clientsun')
