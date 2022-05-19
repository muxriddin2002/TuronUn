from asyncio.log import logger
from home.bugalter.functions import sendSmsOneContact
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from home.models import Store
from home.models import Category, Customer, Employee
from django.contrib import messages
from django.conf import settings

def homeView(request):
    if request.user.is_authenticated:
        return switcher(request.user)
    else:
        return redirect('login')

def switcher(user):
    try:
        if user.type == 1:
            return redirect('director-dashboard')
        elif user.type == 2:
            return redirect('bank-kassa')
        elif user.type == 4:
            return redirect('sotuvchi_dashboard')
        elif user.type == 9:
            return redirect('tarozi-moliya-dashboard')
        elif user.type == 8:
            return redirect('tarozi-dashboard')
        elif user.type == 10:
            return redirect('texnolog-dashboard')
        elif user.type == 12:
            return redirect('kassa')
        #new role
        elif user.type == 17:
            return redirect('sotuv_rahbar_dashboard')
        elif user.type == 18:
            return redirect('operator-dashboard')
        elif user.type == 19:
            return redirect('ombor_kassa_dashboard')
        elif user.type == 22:
            return redirect('hujjatchi_dashboard')
        elif user.type == 21:
            return redirect('yordamchi_bugalter_dashboard')
        else:
            return redirect('logout')
    except Exception as e:
        logger.error(f"{e}")
        return redirect('logout')

def login_view(request):
    if request.user.is_authenticated:
        user = request.user
        return switcher(user)
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            employe = Employee.objects.filter(username=username)
            if employe.count() > 0:
                emp = authenticate(username=username, password=password)
                if emp is not None:
                    login(request, emp)
                    return switcher(emp)
                else:
                    messages.error(request, 'Login yoki parol xato!')
                    return redirect('login')
            else:
                messages.error(request, 'Bunday foydalanuvchi mavjud emas!')
                return redirect('login')

        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

#askar edited
def customeredit(request):
    try:
        if request.method == "POST":
            if request.user.type in [18, 1]:
                category = request.POST['category']
                category = Category.objects.get(id=category)
                #Category
                customer = request.POST['customer']
                customer = Customer.objects.get(id=customer)
                customer.category = category
                #limit
                limit = request.POST['limit']
                customer.limit = limit
                #name
                f_name = request.POST['f_name']
                customer.name = f_name
                #phone
                phone = request.POST['phone']
                customer.phone = phone
                #location
                lacation = request.POST['address']
                customer.location = lacation
                #hudu
                hudud = request.POST['hudud']
                customer.hudud = hudud
                #save
                customer.save()
            messages.success(request, "Muvofaqiyatli o'zgartirildi")
            if request.user.type == 17:
                return redirect('mijozlar')
            return redirect("customers")

    except Exception as e:
        messages.error(request, f"{e}da Xatolik")
        return redirect("customers")
    
# SEND SMS if store miqdor is less than 0
def store_product_alert_sms_send():
    stores = Store.objects.filter(miqdori__lte = 0)
    number = settings.SMS_STORE_PRODUCT_NUMBER
    for store in stores:
        txt = f'{store.tegirmon} ombordagi {store.product} mahsulot, {store.miqdori} miqdorda qoldi! '
        sendSmsOneContact(number, str(txt))
   
