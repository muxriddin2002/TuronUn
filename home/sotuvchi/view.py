from asyncio.log import logger
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from home.models import *
import json
from home.api.firebase_push import send_notification, run_send_notification
# add basket
from decimal import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from django.db.models import Avg, Max, Min, Sum
from multiprocessing import Process
import threading

def checkclient():
    check = CheckClientType.objects.last()
    customer = Customer.objects.all()
    d0 = datetime.now().date()
    for cus in customer:
        if Order.objects.filter(customer=cus).count() > 0:
            order = Order.objects.filter(customer=cus).last()
            delta = d0 - order.date
            if int(delta.days) >= check.active:
                cus.status = 1
            if int(delta.days) >= check.normal:
                cus.status = 2
            if int(delta.days) >= check.passive:
                cus.status = 3
            cus.save()
    return True


class Dashboard(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'sotuvchi/dashboard.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 4:
            return redirect('logout')
        return super(Dashboard, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Dashboard, self).get_context_data(**kwargs)
        checkclient()

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
        kirim = Order.objects.filter(seller=self.request.user).aggregate(summa_total=Sum('summa_total'))['summa_total']
        qaytuvsumma = Qaytuv.objects.filter(seller=self.request.user).aggregate(summa_total=Sum('summa_total'))['summa_total']
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
            monthly = Order.objects.filter(
                seller=self.request.user, date__month=i, date__year=year)

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
            monthly = Qaytuv.objects.filter(
                seller=self.request.user, date__month=i, date__year=year)
            for income in monthly:
                chiqim_oylar[i].append(income.summa_total)

        customers = Customer.objects.filter(employe=self.request.user)
        cus = []
        total_sum = 0
        for i in customers:
            ord = Order.objects.filter(customer=i)
            summa = Decimal(0)
            for o in ord:
                summa += o.summa_total
                total_sum += o.summa_total
                
            dt = {
                "name": i.name,
                "debt": i.debt,
                "hudud": i.hudud,
                "phone": i.phone,
                "total": summa,
            }
            cus.append(dt)
        products = Store.objects.all()
        user = self.request.user
        passive_haridorlar = Customer.objects.filter(status=3, employe=user).count()
        active_haridorlar = Customer.objects.filter(status=1, employe=user).count()
        normal_haridorlar = Customer.objects.filter(status=2, employe=user).count()
        return {
            "passive_haridorlar": passive_haridorlar,
            "active_haridorlar": active_haridorlar,
            "normal_haridorlar": normal_haridorlar,
            "products": products,
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
            "cus": cus,
            "customers": customers,
            "haridorlar": customers.count(),
            'new_order': Order.objects.filter(
                seller=self.request.user, status=1
            ).count(),
            'old_order': Order.objects.filter(
                seller=self.request.user, status=4
            ).count(),
            "active_qaytuv": Qaytuv.objects.filter(
                seller=self.request.user, status=1
            ).count(),
            "old_qaytuv": Qaytuv.objects.filter(
                seller=self.request.user, status=2
            ).count(),
            'kirim': kirim,
            'qaytuvsumma': qaytuvsumma,
            'total_sum': total_sum,
        }


def getdashdetailsel(request):
    user = request.user
    
    start = request.GET.get('start')
    
    end = request.GET.get('end')
    order = Order.objects.filter(seller=user, date__gte=start, date__lte=end)
    kirim = sum(i.summa_total for i in order)
    qaytuv = Qaytuv.objects.filter(seller=user, date__gte=start, date__lte=end)
    qaytuvsumma = sum(i.summa_total for i in qaytuv)
    dt = {
        'new_order': Order.objects.filter(seller=user, date__gte=start, date__lte=end, status=1).count(),
        'old_order': Order.objects.filter(seller=user, date__gte=start, date__lte=end, status=2).count(),
        "active_qaytuv": Qaytuv.objects.filter(seller=user, date__gte=start, date__lte=end, status=1).count(),
        "old_qaytuv": Qaytuv.objects.filter(seller=user, date__gte=start, date__lte=end, status=2).count(),
        'kirim': int(kirim),
        "qaytuvsumma": int(qaytuvsumma),
    }
    return JsonResponse(dt)


def getchangechartsel(request):
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
        monthly = Order.objects.filter(
            customer=customer, date__month=i, date__year=year)

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
        monthly = Qaytuv.objects.filter(
            customer=customer, date__month=i, date__year=year)

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


class GetOrder(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'sotuvchi/get_order.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 4:
            return redirect('logout')
        return super(GetOrder, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(GetOrder, self).get_context_data(**kwargs)
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        user = self.request.user

        if date_start is not None and date_end is not None:
            d_st = datetime.strptime(date_start, "%m/%d/%Y")
            d_en = datetime.strptime(date_end, "%m/%d/%Y")
            orders = Order.objects.filter(
                date__gte=d_st.date(),
                date__lte=d_en.date(), seller=user
            )
        else:
            orders = Order.objects.filter(
                status__in=[1, 2], seller=user).order_by('-id')

        customer = Customer.objects.filter(employe=user)
        # mew
        tegirmons = Tegirmon.objects.all()

        return {
            'customers': customer,
            'orders': orders,
            'tegirmons': tegirmons
        }


class GetQaytuv(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'sotuvchi/get_qaytuv.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 4:
            return redirect('logout')
        return super(GetQaytuv, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(GetQaytuv, self).get_context_data(**kwargs)
        user = self.request.user
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')

        if date_start is not None and date_end is not None:
            d_st = datetime.strptime(date_start, "%m/%d/%Y")
            d_en = datetime.strptime(date_end, "%m/%d/%Y")
            orders = Qaytuv.objects.filter(
                date__gte=d_st.date(),
                date__lte=d_en.date(),
                seller=user
            )
        else:
            orders = Qaytuv.objects.filter(seller=user).order_by('-id', )[:30]
        customer = Customer.objects.filter(employe=user)

        return {
            'customers': customer,
            'orders': orders,
        }

class GetOrderActive(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'sotuvchi/get_order_active.html'

    def dispatch(self, *args, **kwargs):
        return super(GetOrderActive, self).dispatch(*args, **kwargs) if self.request.user.is_authenticated else redirect('login')

    def get_context_data(self, **kwargs):
        super(GetOrderActive, self).get_context_data(**kwargs)
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        user = self.request.user
        
        if user.type in [1,8,17] :
            orders = Order.objects.filter(
                status__in=[1, 2, 3]
            ).order_by('-id')[:30]
        elif date_start is not None and date_end is not None:
            d_st = datetime.strptime(date_start, "%m/%d/%Y")
            d_en = datetime.strptime(date_end, "%m/%d/%Y")
            orders = Order.objects.filter(
                date__gte=d_st.date(),
                date__lte=d_en.date(),
                status__in=[1, 2, 3], seller=user
            )
        else:
            orders = Order.objects.filter(
                status__in=[1, 2, 3], seller=user
            ).order_by('-id')

        return {
            'orders': orders,
            'total_sum': orders.aggregate(Sum('summa_total'))['summa_total__sum'],
        }

class GetOrderPassive(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'sotuvchi/get_order_passive.html'

    def dispatch(self, *args, **kwargs):
        return super(GetOrderPassive, self).dispatch(*args, **kwargs) if self.request.user.is_authenticated else redirect('login')

    def get_context_data(self, **kwargs):
        super(GetOrderPassive, self).get_context_data(**kwargs)
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        user = self.request.user

        if date_start is not None and date_end is not None:
            d_st = datetime.strptime(date_start, "%m/%d/%Y")
            d_en = datetime.strptime(date_end, "%m/%d/%Y")
            orders = Order.objects.filter(
                date__gte=d_st.date(),
                date__lte=d_en.date(),
                status__in=[4], seller=user
            )
        else:
            orders = Order.objects.filter(
                status=4, seller=user).order_by('-id')
        return {
            'orders': orders,
            'summa_total': orders.aggregate(Sum('summa_total'))['summa_total__sum'],
        }

class Mijozlar(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'sotuvchi/mijozlar.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.type != 4:
            return redirect('login')
        return super(Mijozlar, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Mijozlar, self).get_context_data(**kwargs)
        user = self.request.user
        customers = Customer.objects.filter(employe=user)
        haqdorlik = sum(i.debt for i in customers if i.debt > 0)
        qarzdorlik = sum(i.debt for i in customers if i.debt < 0)

        return {
            'haqdorlik': haqdorlik,
            'qarzdorlik': qarzdorlik,
            'customers': customers
        }

class OrderDetail(DetailView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'sotuvchi/buyurtma_detail.html'
    context_object_name = 'order'
    model = Order

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 4:
            return redirect('logout')
        order = Order.objects.get(id=self.kwargs['pk'])
        if  order.seller != self.request.user:
            return redirect('logout')
        return super(OrderDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderDetail, self).get_context_data(**kwargs)
        context['products'] = Store.objects.filter(miqdori__gt = 0)
        context['tegirmon'] = Tegirmon.objects.all()
        return context

class QaytuvDetail(DetailView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'sotuvchi/qaytuv_detail.html'
    context_object_name = 'order'
    model = Qaytuv

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 4:
            return redirect('logout')
        return super(QaytuvDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QaytuvDetail, self).get_context_data(**kwargs)
        context['products'] = Store.objects.all()
        context['tegirmon'] = Tegirmon.objects.all()
        context['maxsulotjs'] = json.dumps(
            list(Store.objects.values('id', 'product__name', 'product', 'miqdori', 'tegirmon')))
        return context

class OrderDetailActive(DetailView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'sotuvchi/buyurtma_detail_active.html'
    context_object_name = 'order'
    model = Order

    def dispatch(self, *args, **kwargs):
        # sourcery skip: assign-if-exp, reintroduce-else, swap-if-expression
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super(OrderDetailActive, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderDetailActive, self).get_context_data(**kwargs)
        context['products'] = Store.objects.all()
        return context

def create_order(request):
    try:
        customer = request.POST.get('customer')
        tegirmon = request.POST.get('tegirmon')
        date = request.POST.get("date")
        order = Order.objects.create(
            customer_id=customer,
            payment_date=date,
            seller_id=request.user.id,
            tegirmon_id=tegirmon,
            date_time = timezone.now()
        )
        #send notification
        mobile_users = Employee.objects.filter(type__in = [5,6,15,16,20])
        p = threading.Thread(target=run_send_notification, args=(mobile_users,))
        p.start()
        messages.success(request, "Ma'lumot muvofaqiyatli saqlandi!")
        return redirect('sotuvchi-order-detail', pk=order.id)
        # return redirect('sotuvchi-get-order')
    except Exception as er:
        print(er)
        messages.error(request, "Ma'lumotlar saqlashda xatolik bor!")
        return redirect('sotuvchi-get-order')

def create_qaytuv(request):
    try:
        customer = request.POST.get('customer')
        Qaytuv.objects.create(
            customer_id=customer,
            seller_id=request.user.id
        )
        return redirect('sotuvchi-get-qaytuv')
    except Exception:
        return redirect('sotuvchi-get-qaytuv')

# Smart select ajax
def load_products(request):
    try:
        user = request.user
        order_id = request.GET.get('order_id')
        tg_id = get_object_or_404(Order, pk=order_id,   seller=user).tegirmon_id
        products = Store.objects.filter(tegirmon_id=tg_id, miqdori__gt = 0 ).order_by('id')
    except Exception as e:
        print(e)
        products = Store.objects.none()

    context = {
        'products': products,

    }
    return render(request, 'sotuvchi/product_table.html', context)

# Smart select ajax
def load_modal(request):
    try:
        user = request.user
        order_id = request.GET.get('order_id')
        orders = get_object_or_404(Order.objects.order_by('-date'), pk=order_id,  seller=user)

    except Exception as e:
        orders = Order.objects.none()
        print(e)

    context = {
        'orders': orders
    }
    return render(request, 'sotuvchi/modal_data.html', context)

# main save to basket via a href

@login_required(login_url='/login/')
@csrf_exempt
def add_basket(request, order_id, pro_id, narxi, qop_soni):
    # sourcery skip: raise-specific-error
    try:
        narxi = float(narxi)
        qop_soni = float(qop_soni)
        # check user type
        if request.user.type != 4:
            return redirect('logout')
        #checking
        store = Store.objects.get(id=pro_id)
        if store.miqdori < qop_soni:
            raise Exception(f'Omborda {store.product} miqdori kam !')

        # check if request user is seller
        is_seller = Order.objects.filter(
            id=order_id, seller_id=request.user.id).exists()
        if order_id == 0 or pro_id == 0 or narxi == 0 or qop_soni == 0 or is_seller == False:
            raise Exception(
                'Qiymatlarda xatolik bor 0ga teng yoki bu user bu orderni yaratmagan!')

        order = get_object_or_404(Order, pk=order_id)

        clint = Order.objects.get(id=order_id, seller=request.user).customer

        bc = Basket.objects.filter(orderlar__seller=request.user,
                                   orderlar__customer=clint, product_id=pro_id, orderlar=order_id).count()
        if bc > 0:
            logger.error(f'{request.user} can create only one time {bc} basket')
            raise Exception(f'{request.user}! Bu maxsulot oldin saqlangan ')
        else:
            bs = Basket.objects.create(
                product_id=pro_id,
                hajmi=qop_soni,
                price=narxi,
            )

        BaskCounter.objects.create(basket=bs, miqdori=bs.hajmi)
        order.baskets.add(bs)
        #plan
        plan ,created = Plan.objects.get_or_create(sotuvchi=request.user)
        plan.soni -= qop_soni
        plan.save()

        store.miqdori -= qop_soni
        store.save()
        
        if order.type_bonus is not None:
            if order.type_bonus == '1':
                summa = Decimal(bs.hajmi) * Decimal(bs.price)
                total = summa * order.bonus / 100
                order.summa_total += summa - total
                order.save()
                customer = Customer.objects.get(id=order.customer.id)
                customer.debt += summa - total
                customer.save()
            if order.type_bonus == '2':
                total = Decimal(bs.hajmi) * Decimal(bs.price)
                order.summa_total += total
                order.save()
                customer = Customer.objects.get(id=order.customer.id)
                customer.debt += total
                customer.save()
        else:
            sum = Decimal(bs.hajmi) * Decimal(bs.price)
            order.summa_total += sum
            order.save()
            # customer = Customer.objects.get(id=order.customer.id)
            # customer.debt += Decimal(sum)
            # customer.save()
        
        return JsonResponse({'bs_id': bs.id})
    except Exception as er:
        logger.error(f'{er} add basket')
        # return HttpResponseBadRequest('Bad request')
        return JsonResponse({'status': 'error', 'message': f'{er}'}, status=500)  


# delete basket via a href
@login_required(login_url='/login/')
@csrf_exempt
def delete_basket(request, order_id, bk_id):
    try:
        # check user type
        if request.user.type != 4:
            return redirect('logout')

        # check if request user is seller
        is_seller = Order.objects.filter(
            id=order_id, seller_id=request.user.id).exists()
        if order_id == 0 or bk_id == 0 or is_seller == False:
            logger.error('Delete basket')
            raise Exception('Valuelar xato bor 0ga teng yoki bu user bu orderni create qilmagan')

        bk = Basket.objects.get(id=bk_id)
        price = bk.price
        qop_soni = bk.hajmi
        total = Decimal(qop_soni) * Decimal(price)


        order = Order.objects.get(id=order_id)
        customer = Customer.objects.get(id=order.customer.id)
        if order.type_bonus == "1":
            summa = total * order.bonus / 100
            # customer.debt -= total - summa
            order.summa_total -= total - summa
        else:
            # customer.debt -= total
            order.summa_total -= total
        customer.save()
        order.save()
        
        #plan
        plan ,created = Plan.objects.get_or_create(sotuvchi=request.user)
        #save plan
        plan.soni += int(qop_soni)
        plan.save()
        #store
        store = Store.objects.get(id=bk.product.id)
        store.miqdori += float(qop_soni)
        store.save()
        bk.delete()

        return JsonResponse({'status': 'ok'})
    except Plan.DoesNotExist:
        Plan.objects.create(sotuvchi=request.user, soni=10000)
        return HttpResponseBadRequest('Bad request')
    except Exception as er:
        logger.error(f'{er} add basket')
        return JsonResponse({'status': 'error', 'message': f'{er}'}, status=500)
        # return HttpResponseBadRequest('Bad request')


# edit basket via a href
@login_required(login_url='/login/')
@csrf_exempt
def edit_basket(request, order_id, pro_id_edit, narxi_edit, qop_soni_edit, e_id):
    # sourcery skip: raise-specific-error
    try:
        qop_soni_edit = float(qop_soni_edit)
        narxi_edit = float(narxi_edit)
        # check user type
        if request.user.type != 4:
            return redirect('logout')

        # check if request user is seller
        is_seller = Order.objects.filter(
            id=order_id, seller_id=request.user.id).exists()
        if order_id == 0 or pro_id_edit == 0 or e_id == 0 or qop_soni_edit == 0 or is_seller == False:
            logger.error('Edit basket error')
            raise Exception(
                'Qiymatlarda xato bor 0ga teng yoki bu user bu orderni yaratmagan!')

        bask = Basket.objects.get(id=e_id)
        #edit basket
        store = Store.objects.get(id=bask.product.id)
        store.miqdori += bask.hajmi
        
        if store.miqdori < qop_soni_edit:
            store.miqdori -= bask.hajmi
            logger.error('Edit basket da bu miqdor kam')
            raise Exception(f'Omborda {qop_soni_edit} miqdordan kam!')
        else:
            logger.info(f'{bask} Basket yangilandi')
            store.miqdori -= qop_soni_edit
        store.save()
        order = Order.objects.get(id=order_id)
        customer = Customer.objects.get(id=order.customer.id)
        old_total_bask = Decimal(bask.hajmi) * Decimal(bask.price)
        order.summa_total -= old_total_bask
        # customer.debt -= old_total_bask
        new_total_bask = Decimal(qop_soni_edit) * Decimal(narxi_edit)
        order.summa_total += new_total_bask
        # customer.debt += new_total_bask

        customer.save()
        order.save()

        plan ,created = Plan.objects.get_or_create(sotuvchi=request.user)
        plan.soni += bask.hajmi
        plan.soni -= int(qop_soni_edit)
        plan.save()


        bask.product_id = pro_id_edit
        bask.hajmi = qop_soni_edit
        bask.price = narxi_edit
        bask.save()
        return JsonResponse({'status': 'ok'})
    except Plan.DoesNotExist:
        Plan.objects.create(sotuvchi=request.user, soni=10000)
        return HttpResponseBadRequest('Bad request')
    except Exception as er:
        logger.error(f'{er} add basket')
        # return HttpResponseBadRequest('Bad request')
        return JsonResponse({'status': 'error', 'message': f'{er}'}, status=500)  

def add_basket_qaytuv(request):
    try:
        order_id = request.POST.get('order_id')
        pro_id = request.POST.get('pro_id')
        qop_soni = request.POST.get('qop_soni')
        narxi = request.POST.get('narxi')
        qaytuv = Qaytuv.objects.get(id=order_id)
        total = Decimal(qop_soni) * Decimal(narxi)
        qaytuv.summa_total += Decimal(total)
        customer = Customer.objects.get(id=qaytuv.customer.id)
        customer.debt -= Decimal(total)
        customer.save()
        bs = BasketQaytuv.objects.create(
            product_id=pro_id,
            hajmi=qop_soni,
            price=narxi
        )
        qaytuv.baskets.add(bs)
        #plan 
        plan ,created = Plan.objects.get_or_create(sotuvchi=request.user)
        plan.soni += int(qop_soni)
        plan.save()
        
        store = Store.objects.get(id=pro_id)
        store.miqdori += int(qop_soni)
        store.save()
        qaytuv.save()
        return redirect('sotuvchi-qaytuv-detail', pk=order_id)
    except Plan.DoesNotExist:
        Plan.objects.create(sotuvchi=request.user, soni=10000)
        return HttpResponseBadRequest('Bad request')
    except Exception as er:
        print(er)
        return redirect('sotuvchi-get-qaytuv')

def delete_basket_qaytuv(request):
    try:
        order_id = request.GET.get('order_id')
        bk_id = request.GET.get('bk_id')
        bk = BasketQaytuv.objects.get(id=bk_id)
        price = Decimal(bk.price)
        qop_soni = bk.hajmi
        total = Decimal(qop_soni) * Decimal(price)
        qaytuv = Qaytuv.objects.get(id=order_id)
        qaytuv.summa_total -= total
        customer = Customer.objects.get(id=qaytuv.customer.id)
        customer.debt += Decimal(total)
        #plan
        plan ,created = Plan.objects.get_or_create(sotuvchi=request.user)
        plan.soni -= int(qop_soni)
        plan.save()
        #store
        store = Store.objects.get(id=bk.product.id)
        store.miqdori -= int(qop_soni)
        store.save()
        customer.save()
        qaytuv.save()

        bk.delete()
        return redirect('sotuvchi-qaytuv-detail', pk=order_id)
    except Plan.DoesNotExist:
        Plan.objects.create(sotuvchi=request.user, soni=10000)
        return HttpResponseBadRequest('Bad request')
    except:
        return redirect('sotuvchi-get-qaytuv')

def edit_basket_qaytuv(request):
    try:
        order_id = request.POST.get('order_id')
        pro_id_edit = request.POST.get('pro_id_edit')
        qop_soni_edit = request.POST.get("qop_soni_edit")
        narxi_edit = request.POST.get('narxi_edit')
        e_id = request.POST.get('vg_id')
        bask = BasketQaytuv.objects.get(id=e_id)
        qaytuv = Qaytuv.objects.get(id=order_id)

        customer = Customer.objects.get(id=qaytuv.customer.id)
        old_total_bask = Decimal(bask.hajmi) * Decimal(bask.price)
        qaytuv.summa_total -= old_total_bask
        customer.debt += old_total_bask
        new_total_bask = Decimal(qop_soni_edit) * Decimal(narxi_edit)
        qaytuv.summa_total += new_total_bask
        customer.debt -= new_total_bask
        customer.save()

        qaytuv.save()

        store = Store.objects.get(id=bask.product.id)
        #plan
        plan ,created = Plan.objects.get_or_create(sotuvchi=request.user)
        
        store.miqdori -= bask.hajmi
        plan.soni -= bask.hajmi
        
        plan.soni += int(qop_soni_edit)
        store.miqdori += int(qop_soni_edit)
        
        plan.save()
        store.save()

        bask.product_id = pro_id_edit
        bask.hajmi = qop_soni_edit
        bask.price = narxi_edit
        bask.save()

        return redirect('sotuvchi-qaytuv-detail', pk=order_id)
    except Plan.DoesNotExist:
        Plan.objects.create(sotuvchi=request.user, soni=10000)
        return redirect('sotuvchi-get-qaytuv')
    except:
        return redirect('sotuvchi-get-qaytuv')

def craetecustomer(request):
    try:
        if request.method == "POST":
            r = request.POST.get
            user = request.user
            name = r("name")
            hudud = r("select")
            phone = r("phone")
            extra_phone = r("extra_phone")
            location = r("location")
            bank_name = r("bank_name")
            bank_number = r("bank_number")
            inn = r("inn")
            mfo = r("mfo")
            existing_user = Customer.objects.filter(phone=phone).count()
            if existing_user > 0:
                messages.error(request, f"{phone} telefon raqami orqali mijoz qo'shilgan")
            else:
                Customer.objects.create(name=name, employe=user, hudud=hudud, phone=phone, extra_phone=extra_phone,
                                        location=location,
                                        bank_name=bank_name, bank_number=bank_number, inn=inn, mfo=mfo)
                messages.success(request, "Ma'lumotlar muvofaqiyatli saqlandi")

        return redirect("customers")
    except Exception as e:
        print(e)
        messages.error(request, f"{e} bo'limida xatolik")
        return redirect("customers")

class ResidualBranchesDetail(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'sotuvchi/residual-branches.html'
    model = ResidualBranches

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 4:
            return redirect('logout')
        return super(ResidualBranchesDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ResidualBranchesDetail,
                        self).get_context_data(**kwargs)
        user = self.request.user
        context['residue'] = ResidualBranches.objects.filter(saler=user)

        return context


def changeresidue(request, pk):
    residue = ResidualBranches.objects.get(id=pk)
    url = residue.url
    data = requests.get(
        f'{url}api/get_detail/?product_name={residue.product.name}').json()
    now = datetime.now()
    if data['status'] == 404:
        messages.error(request, "Bunday maxsulot hali omborda yoq")
    else:
        residue.quantity = data['quantity']
        residue.date = now
        residue.save()
        messages.success(request, "Ma'lumotlar muvofaqiyatli o'zgartirildi")

    return redirect("residual-branches")

def changeallresidue(request):
    user = request.user
    residue = ResidualBranches.objects.filter(saler=user)
    # print(residue)
    for i in residue:
        url = i.url
        data = requests.get(
            f'{url}api/get_detail/?product_name={i.product.name}').json()
        now = datetime.now()
        if data['status'] == 404:
            messages.error(request, "Bunday maxsulot hali omborda yoq")
            return redirect("residual-branches")
        else:
            i.quantity = data['quantity']
            i.date = now
            i.save()

    messages.success(request, "Ma'lumotlar muvofaqiyatli o'zgartirildi")
    return redirect("residual-branches")


def addbonus(request):
    try:
        client_id = request.POST.get("client_id")
        type = request.POST.get("type")
        bonus = request.POST.get("bonus")
        order_id = request.POST.get("order_id")
        order = Order.objects.get(id=order_id)
        client = Customer.objects.get(id=client_id)
        order.type_bonus = type
        order.bonus = bonus
        if type == "2":
            order.summa_total -= Decimal(bonus)
            client.debt -= Decimal(bonus)
            client.save()
        order.save()

        return redirect('sotuvchi-order-detail', pk=order_id)
    except Exception as e:
        print(e)
        return redirect('sotuvchi-get-order')


def DeleteOrder(request, pk):
    try:
        order = Order.objects.get(id=pk)
        customer = order.customer
        baskets = order.baskets.all()
        for i in baskets:
            store = Store.objects.get(id=i.product.id)
            store.miqdori += int(i.hajmi)
            store.save()
        if order.type_bonus == '1':
            customer.debt -= order.summa_total
            customer.save()
        if order.type_bonus == "2":
            customer.debt -= order.summa_total
            customer.save()
        order.delete()
        messages.success(request, "Ma'lumotlar muvofaqiyatli o'chirildi")
        return redirect("sotuvchi-get-order")
    except Exception as e:
        print(e)
        messages.error(request, "Ma'lumotlar  o'chirishda xatolik")
        return redirect("sotuvchi-get-order")


def ClientOrder(request, pk):
    try:
        client = Customer.objects.get(id=pk)
        order = Order.objects.filter(customer=client)

        context = {
            'order': order,
        }
        return render(request, 'sotuvchi/client_orders.html', context)
    except Exception as e:
        return redirect('sotuvchi-get-order')
