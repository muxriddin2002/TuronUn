from datetime import datetime, timedelta
from django.db.models import Sum, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, DetailView
from decimal import * 
from django.shortcuts import redirect
from django.contrib import messages
from home.models import *
from django.utils import timezone



class Dashboard(TemplateView, LoginRequiredMixin):
    """Dashboard view for operator

    Args:
        TemplateView (_type_): TemplateView
        LoginRequiredMixin (_type_): operator must be logged in

    Returns:
        _type_: operator dashboard
    """    
    login_url = '/login'
    template_name = 'operator/dashboard.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 18:
            return redirect('logout')
        return super(Dashboard, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        super(Dashboard, self).get_context_data(**kwargs)

        day = timezone.now()
        month = day.month
        year = day.year
        thirty_days_ago = day - timedelta(days=30)
        month = thirty_days_ago.month
        if month == 12:
            month2 = 1
            year2 = year + 1
        else:
            month2 = month + 1
            year2 = year
            
        gte = datetime(year, month, 1)
        lte = datetime(year2, month2, 1)
        
        sotuvchlar = Employee.objects.filter(type=4)
        datas = []
        for i in sotuvchlar:
            oreder_summa_total = Order.objects.filter(seller=i).aggregate(Sum('summa_total'), Count('id'))
            oreder_total_fineshed = Order.objects.filter(seller=i,status=4).aggregate(Count('id'))['id__count']
            dt = {
                'name': f'{i.first_name} {i.last_name}',
                'summa_total': oreder_summa_total['summa_total__sum'],
                'total_count': oreder_summa_total['id__count'],
                'total_fineshed_count': oreder_total_fineshed,
            }
            datas.append(dt)

        # Chiqib ketgan order count
        orders_count = Order.objects.filter(status=4, date__month__gte=month).aggregate(Count('id'))['id__count']
        order_sum = Order.objects.filter(status=4, date__month__gte=month).aggregate(Sum('summa_total'))['summa_total__sum']

        # Chiqib ketgan order summa
        neworder =   Order.objects.filter(status__in=[1, 2, 3], date__month__gte=month).aggregate(Sum('summa_total'))['summa_total__sum']
        oldqaytuv = Qaytuv.objects.filter(status=2, date__month__gte=month).aggregate(Sum('summa_total'))['summa_total__sum']
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

        return {
            'sellers': datas,
            'orders_count': orders_count,
            'order_sum': order_sum,
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

            'neworder': int(neworder),
            'oldqaytuv': oldqaytuv,
            'customers': Customer.objects.all(),
        }
        
class OrderList(ListView, LoginRequiredMixin):
    """All orders

    Args:
        TemplateView (_type_): _description_
        LoginRequiredMixin (_type_): _description_

    Returns:
        _type_: orders list
    """
    login_url = '/login'
    template_name = 'operator/order_list.html'
    model = Order

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [1,17,18,21]:
            return redirect('logout')
        return super(OrderList, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        super(OrderList, self).get_context_data(**kwargs)
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        day = timezone.now()
        # month = day.month
        year = day.year

        thirty_days_ago = day - timedelta(days=30)
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
            ).order_by('summa_total')
            passive_orders = Order.objects.filter(
                date__gte=d_st.date(),
                date__lte=d_en.date(),
                status = 4
            )

        else:
            orders = Order.objects.filter(date__gte=thirty_days_ago.date(), status__in=[1, 2, 3]).order_by('summa_total')
            passive_orders = Order.objects.filter(date__gte=thirty_days_ago.date(), status=4).order_by('-id')
        passive_orders_total_sum = passive_orders.aggregate(Sum('summa_total'))['summa_total__sum']
        orders_total_sum = orders.aggregate(Sum('summa_total'))['summa_total__sum']
        dollar = Currency.objects.last()
        return {
            'orders': orders,
            'passive_orders': passive_orders,
            'dollar': dollar,
            'orders_total_sum': orders_total_sum,
            'passive_orders_total_sum': passive_orders_total_sum,
        }


#OrderDetail
class OrderDetails(DetailView, LoginRequiredMixin):
    """Order detail for operator type

    Args:
        TemplateView (_type_): _description_
        LoginRequiredMixin (_type_): _description_

    Returns:
        _type_: _description_
    """
    model = Order
    login_url = '/login'
    template_name = 'operator/order_detail.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [1, 17, 18, 21]:
            return redirect('logout')
        return super(OrderDetails, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(OrderDetails, self).get_context_data(**kwargs)
        order  = self.get_object()
        context['order_baskets'] = order.baskets.all()
        context['order_sum'] = order.summa_total
        context['dollar'] =  Currency.objects.last()
        return context
    

def edit_operator_basket(request):
    """Edit operator basket

    Args:
        request (_type_): POST

    Returns:
        _type_: save basket count updated
    """
    try:
        if request.method == 'POST':
            e_basket_id=request.POST.get('basket_id')
            hajmi=request.POST.get('hajmi')
            basket = Basket.objects.get(id=e_basket_id)
            store = Store.objects.get(id=basket.product.id)
            new_hajm = basket.hajmi - int(float(hajmi))
            if store.miqdori < int(new_hajm):
                raise Exception('Omborda kam bu miqdordan!')
            order = Order.objects.get(baskets=basket)
            print(order)
            customer = Customer.objects.get(id=order.customer.id)
            
            old_total_bask = Decimal(basket.hajmi) * Decimal(basket.price)
            order.summa_total -= old_total_bask
            customer.debt -= old_total_bask
            
            new_total_bask = Decimal(hajmi) * Decimal(basket.price)
            order.summa_total += new_total_bask
            customer.debt += new_total_bask
            
            customer.save()
            order.save()
            
            
            store.miqdori += basket.hajmi
            store.miqdori -=  int(float(hajmi))
            store.save()
            basket.hajmi =  int(float(hajmi))
            basket.save()
            messages.success(request, "Yangilandi!")
            return redirect('mijoz', id=order.id)
    except Exception as e:
        print(e)
        return HttpResponse(e)