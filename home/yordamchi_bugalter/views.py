from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from home.models import *

class Clients(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'yordamchi_bugalter/bugalter_clients.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 21:
            return redirect('logout')
        return super(Clients, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Clients, self).get_context_data(**kwargs)
        clients = Customer.objects.all()
        dollar = Currency.objects.last()
        haqdorlik = sum(i.debt for i in clients if i.debt > 0)
        qarzdorlik = sum(i.debt for i in clients if i.debt < 0)
        bank_numbers = BankShots.objects.all()
        return {
            "clients": clients,
            "dollar": dollar,
            "haqdorlik": haqdorlik,
            "qarzdorlik": qarzdorlik,
            'bank_numbers': bank_numbers,
        }