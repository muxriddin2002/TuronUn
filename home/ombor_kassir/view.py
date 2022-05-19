from datetime import timedelta
from locale import currency
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from home.models import *

#Kassa
class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'ombor_kassa/dashboard.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type not in [19]:
            return redirect('logout')
        return super(Dashboard, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
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
        context['dollar'] = Currency.objects.last()
        currency = Currency.objects.last()
        context['olish_sum'] = currency.olish_sum
        context['sotish_sum'] = currency.sotish_sum
        #kassa
        context['kassa_dollor'] = OmborCash.objects.values_list('naqd_pull_dollor',flat=True).last()
        context['kassa_sum'] = OmborCash.objects.values_list('naqd_pull_sum',flat=True).last()
        context['categories'] = ChiqimCategory.objects.all()
        
        if date_start is not None and date_end is not None:
            d_st = datetime.strptime(date_start, "%m/%d/%Y")
            d_en = datetime.strptime(date_end, "%m/%d/%Y")
            context['kirim_history'] = PaymentHistory.objects.filter(type=1, date__gte=d_st.date(),date__lte=d_en.date()).order_by('-id')
            context['chiqim_history'] = PaymentHistory.objects.filter(type=2, date__gte=d_st.date(),date__lte=d_en.date()).order_by('-id')
            context['convertHistory'] = ConvertHistory.objects.filter(date__gte=d_st.date(), date__lte=d_en.date()).order_by('-id')
        else:
            context['kirim_history'] = PaymentHistory.objects.filter(type=1,date__month__gte = month).order_by('-id')
            context['chiqim_history'] = PaymentHistory.objects.filter(type=2, date__month__gte = month).order_by('-id')
            context['convertHistory'] = ConvertHistory.objects.filter(date__month__gte = month).order_by('-id')
        return context
