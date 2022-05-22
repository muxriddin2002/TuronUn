from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone
from datetime import datetime


class Tegirmon(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'Ombor'
        verbose_name_plural = 'Omborlar'

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    type_employee = (
        (1, "Director"),  # web                     +++
        (2, "Accounter"),  # web                    +++
        (3, "Manager"),  # web                      ---
        (4, "Sotuvchi"),  # web                     +++
        (5, "Qoravul"),  # android                  +++
        (6, "Omborchi asosiy"),  # and              +++
        (7, "Tarozi_hisobchi bon"),  # and          +++
        (8, "Tarozi_hisobchi Xisobchi"),  # web     +++
        (9, "Tarozi_hisobchi Moliyachi"),  # web    +++
        (10, "Texnolog"),  # web                    +++
        (11, "Omborchi filial"),  # and             +++
        (12, "Kassir"),  # web                      +++

        (13, "Yem Production"),  # and
        (14, "Un Production"),  # and
        (15, "Yem Ombor"),  # and
        (16, "Un Ombor"),  # and
        #new employee
        (17, "Sotuv rahbari"),  # new role web
        (18, "Operator"),  # new role web
        (19, "Ombor kassir"),  # new role web
        (20, "Qoravul + Asosiy Ombor"),  # new role web
        (21, "Yordamchi bugalter"),  # new role web
        (22, "Hujjatchi"),  # new role web
    )
    phone = models.CharField(max_length=25, null=True, blank=True)
    type = models.IntegerField(default=0, choices=type_employee)
    tegirmon = models.ForeignKey(Tegirmon, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.PositiveSmallIntegerField(null=True, blank=True)
    firebase_token = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.first_name

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'Ishchi'
        verbose_name_plural = 'Ishchilar'

# Sotuvchilar uchun planlar
class Plan(models.Model):
    sotuvchi = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='plan')
    soni = models.IntegerField(default=0)
    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Planlar'
    
class ClientUn(models.Model):
    compony = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    comment = models.TextField(max_length=1000, null=True, blank=True)
    debt = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    date_start = models.DateField(default=timezone.now)
    class Meta:
        verbose_name = 'Un klinti'
        verbose_name_plural = 'Un klintilar'
        
class Client(models.Model):
    compony = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    comment = models.TextField(max_length=1000, null=True, blank=True)
    debt = models.DecimalField(max_digits=155, decimal_places=2, default=0)

    def __str__(self):
        return self.compony
    class Meta:
        verbose_name = 'Klint'
        verbose_name_plural = 'Klintlar'
        
# sourcery skip: avoid-builtin-shadow
class ClientTin(models.Model):
    compony = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    comment = models.TextField(max_length=1000, null=True, blank=True)
    debt = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    date_start = models.DateField(default=timezone.now)
    class Meta:
        verbose_name = 'Qob klinti'
        verbose_name_plural = 'Qob klintilar'

class TypeofTin(models.Model):
    name = models.CharField(max_length=255)


class Tinhistory(models.Model):
    type = models.ForeignKey(TypeofTin, on_delete=models.CASCADE)
    client = models.ForeignKey(ClientTin, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField()
    date = models.DateField(default=timezone.now)
    # 1 active 2 finished
    status = models.IntegerField(default=1)
    izoh = models.CharField(max_length=255, null=True, blank=True)
    tegirmon = models.ForeignKey(Tegirmon, on_delete=models.CASCADE, default=1, null=True, blank=True)

    class Meta:
        verbose_name = 'Qop tarixi'
        verbose_name_plural = 'Qop tarixi'

class Tin(models.Model):
    type = models.ForeignKey(TypeofTin, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField()
    tegirmon = models.ForeignKey(Tegirmon, on_delete=models.CASCADE, default=1, null=True, blank=True)

    class Meta:
        verbose_name = 'Qop'
        verbose_name_plural = 'Qoplar'

class ExpanceTin(models.Model):
    type = models.ForeignKey(TypeofTin, on_delete=models.CASCADE)
    izoh = models.CharField(max_length=255,blank=True,null=True)
    date = models.DateField(default=timezone.now)
    quantity = models.IntegerField(blank=True, null=True)
    tegirmon = models.ForeignKey(Tegirmon, on_delete=models.CASCADE,default=1, null=True, blank=True)
    class Meta:
        verbose_name = 'Chiqim qop'
        verbose_name_plural = 'Chiqim qoplar'

class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# sourcery skip: avoid-builtin-shadow
class Branch(models.Model):
    name = models.CharField(max_length=255)


class TypeOutlay(models.Model):
    name = models.CharField(max_length=255)


class AktOutlay(models.Model):
    type = models.ForeignKey(TypeOutlay, on_delete=models.CASCADE)
    summa = models.FloatField(default=0)
    date = models.DateField(default=timezone.now)
    chois = (
        ('1', "To'lanmagan"),
        ('2', "To'langan"),
    )
    status = models.CharField(choices=chois, max_length=255, default=1)


class AktUnOutlay(models.Model):
    type = models.ForeignKey(TypeOutlay, on_delete=models.CASCADE)
    summa = models.FloatField(default=0)
    date = models.DateField(default=timezone.now)
    chois = (
        ('1', "To'lanmagan"),
        ('2', "To'langan"),
    )
    status = models.CharField(choices=chois, max_length=255, default=1)


class AktWagon(models.Model):
    number = models.IntegerField(default=0)
    brutto_akt = models.IntegerField(default=0)
    tara_akt = models.IntegerField(default=0)
    netto_akt = models.IntegerField(default=0)
    brutto_fakt = models.IntegerField(default=0)
    tara_fakt = models.IntegerField(default=0)
    netto_fakt = models.IntegerField(default=0)

    def __str__(self):
        return str(self.number)
    
    class Meta:
        verbose_name = 'Akt Wagon'
        verbose_name_plural = 'Akt Wagonlar'


class AktUnWagon(models.Model):
    number = models.IntegerField(default=0)
    brutto_akt = models.IntegerField(default=0)
    tara_akt = models.IntegerField(default=0)
    netto_akt = models.IntegerField(default=0)
    
    brutto_fakt = models.IntegerField(default=0)
    tara_fakt = models.IntegerField(default=0)
    netto_fakt = models.IntegerField(default=0)
    
    #akt wagon products
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return str(self.number)
    
    class Meta:
        verbose_name = 'Akt Un Wagon'
        verbose_name_plural = 'Akts Un Wagonlar'

#yem 
class Akt(models.Model):
    status_type = (
        (1, "Created"),
        (2, "accepted")
    )
    name = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    stansiya = models.CharField(max_length=255, null=True, blank=True)
    #new
    branch = models.ForeignKey(Tegirmon, on_delete=models.CASCADE)
    wagons = models.ManyToManyField(AktWagon)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    status = models.IntegerField(default=1, choices=status_type)
    outlay = models.ManyToManyField(AktOutlay)
    price = models.FloatField(default=0)
    comment = models.TextField(null=True, blank=True)
    is_edited = models.BooleanField(default=False)
    total = models.FloatField(default=0)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Akt'
        verbose_name_plural = 'Aktlar'

class TypeofProduct(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    weight = models.FloatField(default=1,blank=True,null=True, help_text='50kg = 1qob')
    type = models.ForeignKey(TypeofProduct, on_delete=models.CASCADE)
    pr_code = models.PositiveIntegerField(null=True, blank=True, unique=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk:
            super().save(force_insert, force_update, using, update_fields)
        else:
            pr = Product.objects.last()
            self.pr_code = int(pr.pr_code) + 1 if pr is not None else 10
            super(Product, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Maxsulot'
        verbose_name_plural = 'Maxsulotlar'

class UnAkt(models.Model):
    status_type = (
        (1, "Created"),
        (2, "Accepted")
    )
    # product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # product = models.ManyToManyField(Product, blank=True)
    
    client = models.ForeignKey(ClientUn, on_delete=models.CASCADE)
    stansiya = models.CharField(max_length=255, null=True, blank=True)
    # branch = models.ForeignKey(Branch, on_delete=models.CASCADE)  # tegirmon
    ombor = models.ForeignKey(Tegirmon, on_delete=models.CASCADE, blank=True, null=True)  # tegirmon
    
    wagons = models.ManyToManyField(AktUnWagon)  # wagon
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    status = models.IntegerField(default=1, choices=status_type)
    outlay = models.ManyToManyField(AktUnOutlay)  # chiqim
    price = models.FloatField(default=0)
    comment = models.TextField(null=True, blank=True)
    is_edited = models.BooleanField(default=False)
    total = models.FloatField(default=0)
    #new
    num1=models.CharField(max_length=255, null=True, blank=True)
    num2=models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Un Akt'
        verbose_name_plural = 'Un Aktlar'

class Brigada(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Return_product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    izoh = models.CharField(max_length=255)
    tegirmon = models.ForeignKey(Tegirmon, on_delete=models.SET_NULL, null=True)
    qopsoni = models.IntegerField()
    image = models.ImageField(upload_to='returned/', null=True, blank=True)
    status = models.IntegerField(choices=(
        (1, 'active'),
        (2, 'finished'),
    ), default=1)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Qaytgan mahsulot'
        verbose_name_plural = 'Qaytgan mahsulotlar'


class Store(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='store_product')
    price = models.FloatField(default=0)
    miqdori = models.FloatField(default=0)
    qob_soni = models.IntegerField(default=0, help_text='Auto calculate', null=True, blank=True)
    tegirmon = models.ForeignKey(Tegirmon, on_delete=models.CASCADE, null=True)
 
    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     if self.qob_soni:
    #         super().save(force_insert, force_update, using, update_fields)
    #     else:
    #         self.qob_soni = self.miqdori // self.product.weight
    #         super(Store, self).save(force_insert, force_update, using, update_fields)
    
    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

class StoreHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    tegirmon = models.ForeignKey(Tegirmon, on_delete=models.CASCADE)
    chois = (
        ('1', 'created'),
        ('2', 'accepted'),
    )
    status = models.CharField(choices=chois, max_length=50)
    qopsoni = models.PositiveIntegerField()

    def __str__(self):
        return self.product.name


class ProductionHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    tegirmon = models.ForeignKey(Tegirmon, on_delete=models.CASCADE)
    qopsoni = models.PositiveIntegerField()

    def __str__(self):
        return self.product.name


class Category(models.Model):
    name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name or "category"
    


class Customer(models.Model):
    name = models.CharField(max_length=255)
    employe = models.ForeignKey(Employee, on_delete=models.CASCADE)
    debt = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    #new
    hudud  = models.IntegerField(choices=(
        (1, 'Samarqand'),
        (2, 'Toshkent'),
        (3, 'Jizzax'),
        (4, "Afg'on"),
        (5, 'Navoiy'),
        (6, 'Qashqadaryo'),
        (7, 'Surxondaryo'),
        (8, 'Qoraqalpogiston'),
        (9, 'Andijon'),
        (10, 'Buxoro'),
        (11, 'Fargona'),
        (12, 'Xorazm'),
        (13, 'Namangan'),
        (14, 'Sirdaryo'),
    ),default=1)
    phone = models.CharField(max_length=30, null=True, blank=True, unique=True)
    extra_phone = models.CharField(max_length=30, null=True, blank=True)
    location = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    bank_number = models.IntegerField(default=0, null=True, blank=True)
    inn = models.IntegerField(default=0, null=True, blank=True)
    mfo = models.IntegerField(default=0, null=True, blank=True)
    limit = models.IntegerField(default=0, null=True, blank=True)
    birthday = models.DateField(null=True,blank=True)
    status = models.IntegerField(choices=(
        (1, 'Faol'),
        (2, 'Kamroq tovar oluvchilar '),
        (3, 'Ishlamay qolgan mijozlar '),
    ), default=1)
    #new 
    status_turi = models.IntegerField(choices=(
        (1, "Kup miqdorda, kam oladi"),
        (2, "Kam miqdorda, kup oladi"),  
    ), default=2)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #
    #
    #     super().save(self, *args, **kwargs)
    #
    class Meta:
        verbose_name = 'Mijoz'
        verbose_name_plural = 'Mijozlar'


class CheckClientType(models.Model):
    active = models.IntegerField()
    normal = models.IntegerField()
    passive = models.IntegerField()
    
class CheckCustomerType(models.Model):
    urtacha = models.IntegerField(default=0)


class Basket(models.Model):
    product = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)  # product
    miqdori = models.FloatField(default=0)
    hajmi = models.FloatField(default=0)
    price = models.FloatField(default=0)
    brigada = models.ForeignKey(Brigada, on_delete=models.CASCADE, null=True, blank=True)
    is_edited = models.BooleanField(default=False) # is_edited
    load = models.BooleanField(default=False)  ## Zakas  Yuklandi ##
    
    class Meta:
        verbose_name = 'Savatcha'
        verbose_name_plural = 'Savatchalar'

    
class BaskCounter(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    miqdori = models.FloatField(default=0,null=True, blank=True)


class BasketQaytuv(models.Model):
    product = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    miqdori = models.FloatField(default=0)
    hajmi = models.FloatField(default=0)
    price = models.FloatField(default=0)
    brigada = models.ForeignKey(Brigada, on_delete=models.CASCADE, null=True, blank=True)
    is_edited = models.BooleanField(default=False)
    load = models.BooleanField(default=False)  # Zakas  Yuklandi


class WheatHistory(models.Model):
    kilo_1 = models.FloatField(default=0)
    kilo_2 = models.FloatField(default=0)
    kilo_3 = models.FloatField(default=0)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

#Chiqim category model
class ChiqimCategory(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Chiqim Category"
       
    def __str__(self):
        return self.name 
     
class ChiqimSubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ChiqimCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Chiqim Sub-Category"
    
    def __str__(self):
        return self.name 
class Order(models.Model):
    status_type = (
        ('1', "Active"),
        ('2', "In process"),  ## yuklanyapti (add turn)
        ('3', "Process done"),  ##yuklanib boldi
        ('4', "Finished"), ##tamamlandi
        ('5', "Rejected"), # bekor qilindi
    )
   
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    seller = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_time = models.DateTimeField(blank=True, null=True)
    date_payment = models.DateField(null=True, blank=True) # tulov vaqti
    date = models.DateField(default=timezone.now)
    update_date = models.DateField(default=timezone.now)
    summa_total = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    baskets = models.ManyToManyField(Basket,related_name='orderlar')
    status = models.CharField(max_length=50, choices=status_type, default=1)
    img = models.ImageField(upload_to='Sended orders/', null=True, blank=True)
    car_number = models.CharField(max_length=50, null=True, blank=True)
    driver_phone = models.CharField(max_length=50, null=True, blank=True)
    type_bonus = models.CharField(choices=(
        ('1', 'Percent'),
        ('2', 'Dollar'),
    ), max_length=255, null=True, blank=True)
    bonus = models.IntegerField(default=0)
    payment_date = models.DateField()
    
    #new fields
    tegirmon = models.ForeignKey(Tegirmon, on_delete=models.SET_NULL, null=True, blank=True)
    #date_times
    turned_date = models.DateTimeField(blank=True, null=True)
    entered_date = models.DateTimeField(blank=True, null=True)
    left_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.customer.name
    
    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'

class Qaytuv(models.Model):
    status_type = (
        ('1', "Active"),
        ('2', "Done")
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    seller = models.ForeignKey(Employee, on_delete=models.CASCADE)
    summa_total = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)
    baskets = models.ManyToManyField(BasketQaytuv)
    comment = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=status_type, default=1)


class Currency(models.Model):
    sotish_sum = models.IntegerField()
    olish_sum = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sotish_sum)


class TurnofCars(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    turn = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    waiting = models.BooleanField(default=True)
    chois = (
        ('1', 'Active'),
        ('2', 'Yuklanyapti'),
        ('3', 'Chiqib ketti'),
        ('4', 'Bekor qilindi'),
    )
    status = models.CharField(choices=chois, max_length=255)

class TurnofCarsofTashkent(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    turn = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    waiting = models.BooleanField(default=True)
    chois = (
        ('1', 'Active'),
        ('2', 'Yuklanyapti'),
        ('3', 'Chiqib ketti'),
        ('4', 'Bekor qilindi'),
    )
    status = models.CharField(choices=chois, max_length=255)


class Barcodes(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    date = models.DateField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):  # overriding save()
        # sourcery skip: use-datetime-now-not-today
        if self.pk is not None:
            super().save(force_insert, force_update, using, update_fields)
        else:
            date = datetime.today()
            year = str(date.year)
            year2 = year[-2:]
            bar = Barcodes.objects.filter(product=self.product).last()
            if bar is not None:
                self.code = int(bar.code) + 1
            else:
                cod = 100001
                self.code = str(self.product.pr_code) + str(year2) + str(cod)
            return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return str(self.code)


class BarcodesHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    quantity = models.IntegerField()


class PaymentHistory(models.Model):
    clienttin = models.ForeignKey(ClientTin, on_delete=models.SET_NULL, null=True, blank=True)
    clientun = models.ForeignKey(ClientUn, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    custom_date = models.DateField(null=True, blank=True)
    by_user = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    type = models.CharField(choices=(
        ('1', 'income'),
        ('2', 'expance')
    ), max_length=255)
    chois = (
        ('1', 'Bank'),
        ('2', 'Plastik'),
        ('3', 'Naqd'),
    )
    turi = models.CharField(choices=chois, max_length=255)
    for_expance = models.BooleanField(default=False)
    #kurs
    currency = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    bank_shot = models.CharField(max_length=255, null=True, blank=True)
    cash = models.CharField(max_length=255, default="")
    kassa = models.ForeignKey('Cash', on_delete=models.SET_NULL, null=True, blank=True)
    second_cash = models.ForeignKey('SecondCash', on_delete=models.SET_NULL, null=True, blank=True)
    qozoq_cash = models.ForeignKey('QozoqCash', on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    sub_category = models.ForeignKey(ChiqimSubCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{str(self.type)} {str(self.by_user)} {str(self.payment)}'

#shot numbers
class BankShots(models.Model):
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    bank_sum = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    shot_numbers = models.CharField(max_length=255,null=True, blank=True)
    class Meta:
        verbose_name_plural = "Bank hisob raqamlar"

class Cash(models.Model):
    money = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    #new fields
    name = models.CharField(max_length=255, null=True, blank=True)
    naqd_pull_sum = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    naqd_pull_dollor = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=True,blank=True,null=True)
    
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Kassa"

class SecondCash(models.Model):
    #new fields
    name = models.CharField(max_length=255, null=True, blank=True)

    naqd_pull_sum = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    naqd_pull_dollor = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Ikkkinchi Kassa"

class QozoqCash(models.Model):
    #new fields
    name = models.CharField(max_length=255, null=True, blank=True)

    naqd_pull_sum = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    naqd_pull_dollor = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Qozoq Kassa"


class ResidualBranches(models.Model):
    saler = models.ForeignKey(Employee, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    url = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    filial = models.CharField(max_length=255)
    manzil = models.CharField(max_length=255)

    def __str__(self):
         return f'{self.saler} + {self.product} + {self.quantity}'


# sourcery skip: avoid-builtin-shadow
class TypeExpanse(models.Model):
    name = models.CharField(max_length=255)


class Expanse(models.Model):
    summa = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(ChiqimSubCategory, on_delete=models.SET_NULL, null=True)
    izoh = models.CharField(max_length=255)
    chois = (
        ('1', 'unpaid'),
        ('2', 'paid'),
    )
    status = models.CharField(choices=chois, max_length=255, default=1)


class Sendedsms(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    clientun = models.ForeignKey(ClientUn, on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    sms = models.CharField(max_length=2555)


class Tarozi(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    tegirmon = models.ForeignKey(Tegirmon, on_delete=models.SET_NULL, null=True)
    soni = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return f'{self.soni}'


class SMSTemplate(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    chois = (
        (1, "Tug'ilgan kun"),
        (2, "Bayram va boshqalar"),
    )
    type = models.IntegerField(choices=chois)
    date = models.DateField(blank=True, null=True)
    text = models.TextField(default="")
    active = models.BooleanField(default=False)
    customer = models.ManyToManyField(Customer)

    def __str__(self):
        return self.name


class SMSHistory(models.Model):
    smstemplate = models.ForeignKey(SMSTemplate, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(blank=True, null=True)
    is_success = models.BooleanField(default=False)
    send_count = models.IntegerField(default=0)
    not_send_count = models.IntegerField(default=0)

    def __str__(self):
        return self.smstemplate.name

class ConvertHistory(models.Model):
    som = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    converter = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    to_dollor = models.BooleanField(default=False)
    to_som = models.BooleanField(default=False)
    cash = models.CharField(max_length=255, default="")
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    izoh = models.CharField(max_length=255, default="Izoh")
    
    def __str__(self):
        return f'{self.converter.username} - {self.som}'
    
class CashConvertHistory(models.Model):
    converter = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    from_cash = models.CharField(max_length=255)
    to_cash = models.CharField(max_length=255)
    choise = (
        (1, "USD"),
        (2, "UZS"),
    )
    usd_or_uzs = models.IntegerField(choices=choise)
    som = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    comment = models.CharField(max_length=255, default="Kassalar urtasida convert")
    
    def __str__(self):
        return self.comment
    
    class Meta:
        verbose_name_plural = "Kassalar urtasida convert"
        
#Kirim bulgan qoblarni taminotchilarga qaytarish history    
class ReturnedIncomeTinHistory(models.Model):
    type = models.ForeignKey(TypeofTin, on_delete=models.CASCADE)
    quantity = models.FloatField()
    izoh = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    tegirmon = models.ForeignKey(Tegirmon, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.izoh
    class Meta:
            verbose_name_plural = "Kirim bulgan qoplarni qaytarish tarixi"
#Kirim bulgan qoblarni taminotchilarga qaytarish history    
class ReturnedExpanseTinHistory(models.Model):
    type = models.ForeignKey(TypeofTin, on_delete=models.CASCADE)
    quantity = models.FloatField()
    izoh = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    tegirmon = models.ForeignKey(Tegirmon, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.izoh
    class Meta:
            verbose_name_plural = "Chiqim bulgan qoplarni qaytarish tarixi"
            

# Ombor kassasi
class OmborCash(models.Model):
    #new fields
    name = models.CharField(max_length=255, null=True, blank=True)

    naqd_pull_sum = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    naqd_pull_dollor = models.DecimalField(max_digits=155, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Ombor Kassasi"
