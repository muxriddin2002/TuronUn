from asyncio.log import logger
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import *
from datetime import datetime, timedelta
from decimal import *
from django.db.models import Q, Sum, F
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models.functions import Coalesce

# ajax
def ajax_load_ombor(request):
    try:
        ombors = Tegirmon.objects.all()
    except Exception as e:
        logger.error(e)

    context = {
        'ombors': ombors,
    }
    return render(request, 'sotuv_rahbari/ombor_ajax.html', context)

# Check customer & clint type
def checkclient():
    try:
        check = CheckClientType.objects.last()
        check_cus = CheckCustomerType.objects.last()
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
                
            #check customer urtacha
            cus_order_count = Order.objects.filter(customer=cus).count()
            cus_total_suma = sum(item.summa_total for item in Order.objects.filter(customer=cus))
            if cus_order_count>0:
                avg_urta = cus_total_suma/cus_order_count
                cus.status_turi = 1 if check_cus.urtacha <= avg_urta else 2
                cus.save()
        return True
    except Exception as e:
        logger.error(e)
  
#filter dashboard
def getdashdetalsotuv(request):
    try:
        start = request.GET.get('start')
        end = request.GET.get('end')
        

        ac_order = Order.objects.filter(status__in=[1, 2, 3], date__gte=start, date__lte=end)
        ac_order_sum = sum(i.summa_total for i in ac_order)

        qaytuv = Qaytuv.objects.filter(date__date__gte=start, date__date__lte=end)
        qaytuvsumma = sum(i.summa_total for i in qaytuv)
        
        suc_order = Order.objects.filter(status=4, date__gte=start, date__lte=end)
        oldorder = sum(i.summa_total for i in suc_order)
        dt = {
            'ac_order_sum': ac_order_sum,
            'qaytuvsumma': qaytuvsumma,
            'oldorder': oldorder,
        }
        return JsonResponse(dt)
    except Exception as e:
        logger.error(e)



# ajax dash mioz ajax
def getdashdetailmijoz(request):
    try:
        #time
        day = datetime.now()
        # month = day.month
        year = day.year
        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30)
        month = thirty_days_ago.month


        date_start = request.GET.get('start')
        date_end = request.GET.get('end')
        customers = Customer.objects.all()
        cus = []
        total_sums = Decimal(0)
        if date_start is not None and date_end is not None:
            for i in customers:
                ord = Order.objects.filter(customer=i, date__gte=date_start, date__lte=date_end)
                summa = Decimal(0)

                for o in ord:
                    summa += o.summa_total
                    total_sums += o.summa_total

                dt = {
                    "name": i.name,
                    "debt": i.debt,
                    "hudud": i.hudud,
                    "phone": i.phone,
                    "total": summa,
                    }
                cus.append(dt)
        else:
            for i in customers:
                ord = Order.objects.filter(customer=i, date__gte=thirty_days_ago.date(), status__in = [1,2,3,4])
                summa = Decimal(0)

                for o in ord:
                    summa += o.summa_total
                    total_sums += o.summa_total

                dt = {
                    "name": i.name,
                    "debt": i.debt,
                    "hudud": i.hudud,
                    "phone": i.phone,
                    "total": summa,
                    }
                cus.append(dt)


    except Exception as e:
        logger.error(e)
        cus = []
        total_sums = Decimal(0)

    context = {
        'cus': cus,
        'total_sums': total_sums,
    }
    return render(request, 'sotuv_rahbari/ajax_cus.html', context)

#get hudud suma
from django.db.models import  F, DecimalField
from django.db.models import Q
def getdashhududsumma(request): #sourcery no-metrics
    try:
        #time
        day = timezone.now()
        year = day.year - 1

        date_start = request.GET.get('start')
        date_end = request.GET.get('end')

        thirty_days_ago = day - timedelta(days=30)
        month = thirty_days_ago.month
        

        if month == 12:
            month2 = 1
            year2 = year + 1
        else:
            month2 = month + 1
            year2 = year
            
        total = 0
        if date_start is not None and date_end is not None:
            # table viloyatlar buyicha sotilgan orderlar totol sumasi
            hudud_orders = Order.objects.filter(date__gte=date_start, date__lte=date_end, status=4)
        else:
            # table viloyatlar buyicha sotilgan orderlar totol sumasi
            hudud_orders = Order.objects.filter(date__gte=thirty_days_ago.date(), status=4)
            
        samarqand_total_sum =  hudud_orders.filter(customer__hudud=1).aggregate(summa_total=Coalesce(Sum('summa_total'),Decimal(0)))
        toshkent_total_sum =  hudud_orders.filter(customer__hudud=2).aggregate(summa_total=Coalesce(Sum('summa_total'),Decimal(0)))
        jizzax_total_sum =  hudud_orders.filter(customer__hudud=3).aggregate(summa_total=Coalesce(Sum('summa_total'),Decimal(0)))
        afgon_total_sum =  hudud_orders.filter(customer__hudud=4).aggregate(summa_total=Coalesce(Sum('summa_total'),Decimal(0)))
        navoiy_total_sum =  hudud_orders.filter(customer__hudud=5).aggregate(summa_total=Coalesce(Sum('summa_total'),Decimal(0)))
        qashqadaryo_total_sum =  hudud_orders.filter(customer__hudud=6).aggregate(summa_total=Coalesce(Sum('summa_total'),Decimal(0)))
        surxondaryo_total_sum =  hudud_orders.filter(customer__hudud=7).aggregate(summa_total=Coalesce(Sum('summa_total'),Decimal(0)))
        qoraqalpoq_total_sum =  hudud_orders.filter(customer__hudud=8).aggregate(summa_total=Coalesce(Sum('summa_total'),Decimal(0)))
        andijon_total_sum =  hudud_orders.filter(customer__hudud=9).aggregate(summa_total=Coalesce(Sum('summa_total'),Decimal(0)))
        buxora_total_sum =  hudud_orders.filter(customer__hudud=10).aggregate(summa_total=Coalesce(Sum('summa_total'),Decimal(0)))
        fargona_total_sum =  hudud_orders.filter(customer__hudud=11).aggregate(summa_total=Coalesce(Sum('summa_total'),Decimal(0)))
        xorazm_total_sum =  hudud_orders.filter(customer__hudud=12).aggregate(summa_total=Coalesce(Sum('summa_total'),Decimal(0)))
        namangan_total_sum =  hudud_orders.filter(customer__hudud=13).aggregate(summa_total=Coalesce(Sum('summa_total'),Decimal(0)))
        sirdaryo_total_sum =  hudud_orders.filter(customer__hudud=14).aggregate(summa_total=Coalesce(Sum('summa_total'),Decimal(0)))
        #calculate total sum
        total += samarqand_total_sum['summa_total'] + toshkent_total_sum['summa_total'] + jizzax_total_sum['summa_total'] + afgon_total_sum['summa_total'] + navoiy_total_sum['summa_total'] + qashqadaryo_total_sum['summa_total'] + surxondaryo_total_sum['summa_total'] + qoraqalpoq_total_sum['summa_total'] + andijon_total_sum['summa_total'] + buxora_total_sum['summa_total'] + fargona_total_sum['summa_total'] + xorazm_total_sum['summa_total'] + namangan_total_sum['summa_total'] + sirdaryo_total_sum['summa_total']
        
        #SLV tahlil
        order_baskets = Basket.objects.filter(orderlar__in=hudud_orders)
        sold_maxsulotlar = set(Basket.objects.filter(orderlar__in=hudud_orders).values_list('product__product__name', 'product__product__weight'))
        data = []   
        for order_basket in sold_maxsulotlar:
            if order_basket is not None:
                dt = {
                    'name': order_basket[0],
                    'data': {
                    'sam_hajmi' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 1 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'],
                    'tos_hajmi' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 2 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'],
                    'jiz_hajmi' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 3 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'],
                    'afg_hajmi' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 4 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'],
                    'nav_hajmi' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 5 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'],
                    'qas_hajmi' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 6 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'],
                    'sur_hajmi' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 7 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'],
                    'qor_hajmi' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 8 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'],
                    'and_hajmi' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 9 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'],
                    'bux_hajmi' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 10 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'],
                    'far_hajmi' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 11 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'],
                    'xor_hajmi' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 12 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'],
                    'nam_hajmi' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 13 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'],
                    'sir_hajmi' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 14 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'],
                    
                    'sam_kg' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 1 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'] * Decimal(order_basket[1]) / 50,
                    'tos_kg' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 2 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'] * Decimal(order_basket[1]) / 50,
                    'jiz_kg' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 3 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'] * Decimal(order_basket[1]) / 50,
                    'afg_kg' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 4 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'] * Decimal(order_basket[1]) / 50,
                    'nav_kg' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 5 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'] * Decimal(order_basket[1]) / 50,
                    'qas_kg' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 6 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'] * Decimal(order_basket[1]) / 50,
                    'sur_kg' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 7 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'] * Decimal(order_basket[1]) / 50,
                    'qor_kg' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 8 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'] * Decimal(order_basket[1]) / 50,
                    'and_kg' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 9 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'] * Decimal(order_basket[1]) / 50,
                    'bux_kg' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 10 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'] * Decimal(order_basket[1]) / 50,
                    'far_kg' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 11 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'] * Decimal(order_basket[1]) / 50,
                    'xor_kg' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 12 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'] * Decimal(order_basket[1]) / 50,
                    'nam_kg' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 13 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'] * Decimal(order_basket[1]) / 50,
                    'sir_kg' : order_baskets.filter(product__product__name = order_basket[0], orderlar__customer__hudud= 14 ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'] * Decimal(order_basket[1]) / 50,
                    'total_hajmi' : order_baskets.filter(product__product__name = order_basket[0] ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'],
                    'total_hajmi_kg' : order_baskets.filter(product__product__name = order_basket[0] ).aggregate(total__hajmi=Coalesce(Sum('hajmi',output_field=DecimalField()), Decimal(0)))['total__hajmi'] * Decimal(order_basket[1]) / 50,
                    },
                    'weight': order_basket[1],
                }
                data.append(dt)     
    except Exception as e:
        # data =[]
        logger.error(e)
        
    context = {
        'total':total,
        'samarqand_total_sum': samarqand_total_sum,
        'toshkent_total_sum': toshkent_total_sum,
        'jizzax_total_sum': jizzax_total_sum,
        'afgon_total_sum': afgon_total_sum,
        'navoiy_total_sum': navoiy_total_sum,
        'qashqadaryo_total_sum': qashqadaryo_total_sum,
        'surxondaryo_total_sum': surxondaryo_total_sum,
        'qoraqalpoq_total_sum': qoraqalpoq_total_sum,
        'andijon_total_sum': andijon_total_sum,
        'buxora_total_sum': buxora_total_sum,
        'fargona_total_sum': fargona_total_sum,
        'xorazm_total_sum': xorazm_total_sum,
        'namangan_total_sum': namangan_total_sum,
        'sirdaryo_total_sum': sirdaryo_total_sum,
        'data': data,
    }
    return render(request, 'sotuv_rahbari/ajax_hudud_sum.html', context)

# filtrer ech seller sold product via hudud
def getdashsellerhududsumma(request): #sourcery no-metrics
    try:
        #time
        day = timezone.now()
        # month = day.month -1
        year = day.year -1

        date_start = request.GET.get('start')
        date_end = request.GET.get('end')
        thirty_days_ago = day - timedelta(days=30)
        # print(thirty_days_ago) 2022-03-08 07:10:20.597103+00:00
        month = thirty_days_ago.month

        if month == 12:
            month2 = 1
            year2 = year + 1
        else:
            month2 = month + 1
            year2 = year
        
        employer_type_4 = Employee.objects.filter(type=4)
        emp_hudud_sums = []
        
        for cus in employer_type_4:
            total = Decimal(0)
            if date_start is not None and date_end is not None:
                date_orders = Order.objects.filter(seller=cus, date__gte=date_start, date__lte=date_end, status=4)
            else:
                date_orders = Order.objects.filter(seller=cus, date__gte=thirty_days_ago.date(), status=4)
            
            samarqand = date_orders.filter(customer__hudud=1).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))
            tashkent = date_orders.filter(customer__hudud=2).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))
            jizzax = date_orders.filter(customer__hudud=3).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))
            afgon = date_orders.filter(customer__hudud=4).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))
            navoiy = date_orders.filter(customer__hudud=5).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))
            qashqadaryo = date_orders.filter(customer__hudud=6).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))
            surxondaryo = date_orders.filter(customer__hudud=7).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))
            qoraqalpoq = date_orders.filter(customer__hudud=8).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))
            andijan = date_orders.filter(customer__hudud=9).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))
            buxoro = date_orders.filter(customer__hudud=10).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))
            fargona = date_orders.filter(customer__hudud=11).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))
            xorazm = date_orders.filter(customer__hudud=12).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))
            namangan =date_orders.filter(customer__hudud=13).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))
            sirdaryo = date_orders.filter(customer__hudud=14).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))
            #calculate total 
            total+= samarqand['summa_total'] + tashkent['summa_total'] + jizzax['summa_total'] + afgon['summa_total'] + navoiy['summa_total'] + qashqadaryo['summa_total'] + surxondaryo['summa_total'] + qoraqalpoq['summa_total'] + andijan['summa_total'] + buxoro['summa_total'] + fargona['summa_total'] + xorazm['summa_total'] + namangan['summa_total'] + sirdaryo['summa_total']
            dt = {
                'Ismi': f'{cus.first_name} {cus.last_name}',
                'samarqand': samarqand,
                'tashkent': tashkent,
                'jizzax': jizzax,
                'afgon': afgon,
                'navoiy': navoiy,
                'qashqadaryo': qashqadaryo,
                'surxondaryo': surxondaryo,
                'qoraqalpoq': qoraqalpoq,
                'andijan': andijan,
                'buxoro': buxoro,
                'fargona': fargona,
                'xorazm': xorazm,
                'namangan': namangan,
                'sirdaryo': sirdaryo,
                'total':total,
                }

            emp_hudud_sums.append(dt)
    except Exception as e:
        logger.error(e)
        emp_hudud_sums = []
        total = Decimal(0)
        
    context = {

        'emp_hudud_sums':emp_hudud_sums, 
        'total':total 
    }
    return render(request, 'sotuv_rahbari/ajax_seller_hudud_sum.html', context)

class Dashboard(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'sotuv_rahbari/dashboard.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 17:
            return redirect('logout')

        return super(Dashboard, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):  # sourcery no-metrics
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['ombors'] = Tegirmon.objects.all()
        checkclient()
        #time
        day = datetime.now()
        # month = day.month - 1
        year = day.year
        today = datetime.now()
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

        # success and created orders
        neworder = Order.objects.filter(status__in=[1, 2, 3], date__gte=thirty_days_ago.date()).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))['summa_total']

        # oldorder = sum(i.summa_total for i in Order.objects.filter(status=4, date__gte=thirty_days_ago.date()))
        oldorder = Order.objects.filter(status=4, date__gte=thirty_days_ago.date()).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))['summa_total']
        # success and created qaytuvlar
        newqaytuv = sum(i.summa_total for i in Qaytuv.objects.filter(status=1, date__gte=thirty_days_ago.date()))

        oldqaytuv = sum(i.summa_total for i in Qaytuv.objects.filter(status=2, date__gte=thirty_days_ago.date()))

        kirim = Order.objects.filter(date__gte=thirty_days_ago.date()).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))['summa_total']

        qaytuvsumma = Qaytuv.objects.filter(date__gte=thirty_days_ago.date()).aggregate(summa_total=Coalesce(Sum('summa_total'), Decimal(0)))['summa_total']

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
                date__month=i, date__year=year)

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
                date__month=i, date__year=year)
            for income in monthly:
                chiqim_oylar[i].append(income.summa_total)

        customers = Customer.objects.all()
        products = Store.objects.all()

        passive_haridorlar = Customer.objects.filter(status=3).count()
        normal_haridorlar = Customer.objects.filter(status=2).count()
        active_haridorlar = Customer.objects.filter(status=1).count()
        active_haridorlar_urtachasi = Customer.objects.filter(status_turi=1)
        passive_haridorlar_urtachasi = Customer.objects.filter(status_turi=2)

        return { 
            "passive_haridorlar": passive_haridorlar,
            "active_haridorlar": active_haridorlar,
            "normal_haridorlar": normal_haridorlar,
            "active_haridorlar_urtachasi": active_haridorlar_urtachasi,
            "passive_haridorlar_urtachasi": passive_haridorlar_urtachasi,
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

            "customers": customers,
            "haridorlar": customers.count(),
            'new_order': Order.objects.filter(
                status=1
            ).count(),
            'old_order': Order.objects.filter(
                status=4
            ).count(),
            "active_qaytuv": Qaytuv.objects.filter(
                status=1
            ).count(),
            "old_qaytuv": Qaytuv.objects.filter(
                status=2
            ).count(),
            'kirim': kirim,
            'qaytuvsumma': qaytuvsumma,

            # success orders
            'neworder': neworder,
            'oldorder': oldorder,
            # success qaytuv
            'newqaytuv': int(newqaytuv),
            'oldqaytuv': int(oldqaytuv),
        }

# get active  orders
class GetActiveOrder(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'sotuv_rahbari/get_active_order.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super(GetActiveOrder, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(GetActiveOrder, self).get_context_data(**kwargs)
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')

        search = self.request.GET.get('search')

        if search is not None:
            orders = Order.objects.filter(Q(customer__name__icontains=search) | Q(summa_total__icontains=search) | Q(driver_phone__icontains=search) | Q(
                seller__username__icontains=search) | Q(type_bonus__icontains=search), status__in=[1, 2, 3])
        elif date_start is not None and date_end is not None:
            d_st = datetime.strptime(date_start, "%m/%d/%Y")
            d_en = datetime.strptime(date_end, "%m/%d/%Y")
            orders = Order.objects.filter(
                date__gte=d_st.date(),
                date__lte=d_en.date(),
                status__in=[1, 2, 3]
            )
        else:
            orders = Order.objects.filter(
                status__in=[1, 2, 3]
            ).order_by('-id')

        return {
            'orders': orders
        }

# active order details
class OrderDetailActive(DetailView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'sotuv_rahbari/buyurtma_detail_active.html'
    context_object_name = 'order'
    model = Order

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super(OrderDetailActive, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(OrderDetailActive, self).get_context_data(**kwargs)

# seller lists
class SellerList(ListView, LoginRequiredMixin):

    login_url = '/login'
    template_name = 'sotuv_rahbari/seller_list.html'
    context_object_name = 'sellers'
    model = Employee

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super(SellerList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(SellerList, self).get_context_data(**kwargs)
        return {
            'sellers': Employee.objects.filter(type=4).order_by('order_number'),
            'dollar':  Currency.objects.last()

        }


# Yangi jadval
class SellerListJadval(ListView, LoginRequiredMixin):

    login_url = '/login'
    template_name = 'sotuv_rahbari/seller_list_2.html'
    context_object_name = 'sellers'
    model = Employee

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super(SellerListJadval, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(SellerListJadval, self).get_context_data(**kwargs)
        return {
            'sellers': Employee.objects.filter(type=4).order_by('order_number')
        }


# seller details
class SellerDetail(DetailView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'sotuv_rahbari/seller_detail.html'
    context_object_name = 'seller'
    model = Employee

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super(SellerDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SellerDetail, self).get_context_data(**kwargs)
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')

        if date_start is not None and date_end is not None:
            d_st = datetime.strptime(date_start, "%m/%d/%Y")
            d_en = datetime.strptime(date_end, "%m/%d/%Y")
            context['orders'] = Order.objects.filter(
                date__gte=d_st.date(),
                date__lte=d_en.date(),
                status__in=[1, 2, 3, 4], seller=self.kwargs['pk']
            )
        else:
            context['orders'] = Order.objects.filter(
                status__in=[1, 2, 3, 4], seller=self.kwargs['pk']
            ).order_by('-id')
            context['total_summa'] = Order.objects.filter(
                status__in=[1, 2, 3, 4], seller=self.kwargs['pk']
            ).aggregate(Sum('summa_total'))['summa_total__sum']

        context['seller'] = Employee.objects.get(id=self.kwargs['pk'])
        context['dollar'] = Currency.objects.last()

        return context

class Customers(TemplateView, LoginRequiredMixin):
    login_url = '/login'
    template_name = 'sotuv_rahbari/customers.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.type != 17:
            return redirect('logout')
        return super(Customers, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        super(Customers, self).get_context_data(**kwargs)
        seller = self.request.GET.get('seller')
        hudud = self.request.GET.get('hudud')
        category = self.request.GET.get('category')
        status = self.request.GET.get('status')
        
        
        if any(x is not None for x in [seller, hudud, category, status]):
            customers = Customer.objects.filter(Q(employe=seller)  & Q(hudud=hudud) & Q(category=category) & Q(status=status)).order_by('-id')
        else:
            customers = Customer.objects.filter(debt__lte=F('limit')).order_by('-id')
            
        sellers = Employee.objects.filter(type=4).order_by('order_number')
        categories = Category.objects.all()
        haqdorlik = sum(i.debt for i in customers if i.debt > 0)
        qarzdorlik = sum(i.debt for i in customers if i.debt < 0)
        return {
            'customers': customers,
            'sellers': sellers,
            'categories': categories,
            'haqdorlik': haqdorlik,
            'qarzdorlik': qarzdorlik
        }

# set plan for seller
def set_plan(request):
    try:
        if request.method == "POST":
            id = request.POST.get("id")
            plan_qob_soni = request.POST.get("plan", 0)
            employe = get_object_or_404(Employee, pk=id)
            plan = Plan.objects.get(sotuvchi=employe)
            plan.soni = plan_qob_soni
            plan.save()
            messages.success(request, "Muvofaqiyatli plan yangilandi!")
            return redirect("sotuv-rahbari-seller-list")
    except Plan.DoesNotExist:
        Plan.objects.create(sotuvchi=employe, soni=plan_qob_soni)
        messages.success(request, "Muvofaqiyatli plan belgilandi!")
        return redirect("sotuv-rahbari-seller-list")
    except Exception as e:
        logger.error(e)
        messages.error(request, 'Xatolik! Qob soni belgilang')
        return redirect('sotuv-rahbari-seller-list')

# ombor_detail
def ombor_detail(request, id):
    try:
        ombor = get_object_or_404(Tegirmon, id=id)
        stores = Store.objects.filter(tegirmon_id=id)
        context = {
            'stores': stores,
            'ombor': ombor,
        }
        return render(request, 'sotuv_rahbari/ombor_detail.html', context)
    except Exception as e:
        logger.error(e)
        return redirect('/')
