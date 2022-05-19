from datetime import datetime, timedelta
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, DetailView
from decimal import * 
from django.shortcuts import redirect
from home.models import *
from django.utils import timezone


class Dashboard(ListView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'hujjatchi/order_list.html'
    model = Order

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 22:
            return redirect('logout')
        return super(Dashboard, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        super(Dashboard, self).get_context_data(**kwargs)
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        day = timezone.now()
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

        return {
            'orders': orders,
            'passive_orders': passive_orders
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
    template_name = 'hujjatchi/order_detail.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 22:
            return redirect('logout')
        return super(OrderDetails, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(OrderDetails, self).get_context_data(**kwargs)
        order  = self.get_object()
        context['order_baskets'] = order.baskets.all()
        return context