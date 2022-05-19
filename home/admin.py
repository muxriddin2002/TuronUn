from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext, gettext_lazy as _
from .models import *
from django.contrib.auth.admin import UserAdmin

#import export
from import_export.admin import ImportExportActionModelAdmin


# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = ['id','username', 'first_name','last_name', 'phone', 'type', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Extra'), {'fields': ('phone', 'type', 'tegirmon','order_number', 'firebase_token')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.unregister(Group)
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'compony', 'name', 'phone', 'address',
                    'comment', 'debt'
                    ]
@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment', 'date', 'comment', 'type',
                    
                    ]
admin.site.register(WheatHistory)
admin.site.register(Return_product)
admin.site.register(UnAkt)
admin.site.register(ClientUn)
admin.site.register(AktUnOutlay)
admin.site.register(Category)

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
admin.site.register(AktOutlay)
admin.site.register(TypeOutlay)




@admin.register(AktUnWagon)
class AktUnWagonAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "number",
        "brutto_akt",
        "tara_akt",
        "netto_akt",
        "brutto_fakt",
        "tara_fakt",
        "netto_fakt",
    ]


@admin.register(AktWagon)
class AktWagonAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "number",
        "brutto_akt",
        "tara_akt",
        "netto_akt",
        "brutto_fakt",
        "tara_fakt",
        "netto_fakt",
    ]


@admin.register(Akt)
class AktAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "client",
        "stansiya",
        "branch",
        "date_start",
        "date_end",
        "status",
    ]


@admin.register(Tegirmon)
class TegirmonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Brigada)
class BrigadaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(TypeofProduct)
class TypeofProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'pr_code']


@admin.register(Customer)
class CustomerAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'phone','location', 'debt']
    
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'price', 'miqdori','tegirmon']
    list_filter = ['product', 'tegirmon']


@admin.register(StoreHistory)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product',  'date', 'tegirmon', 'qopsoni']

# Plan register 
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'sotuvchi', 'soni']

    
@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    list_display = ['id', 'naqd_pull_sum', 'naqd_pull_dollor']
    
@admin.register(OmborCash)
class OmborCashAdmin(admin.ModelAdmin):
    list_display = ['id', 'naqd_pull_sum', 'naqd_pull_dollor']
    
@admin.register(QozoqCash)
class CashAdmin(admin.ModelAdmin):
    list_display = ['id', 'naqd_pull_sum', 'naqd_pull_dollor']
    
@admin.register(SecondCash)
class SecondCashAdmin(admin.ModelAdmin):
    list_display = ['id', 'naqd_pull_sum', 'naqd_pull_dollor']

@admin.register(TurnofCarsofTashkent)
class TurnofCarsofTashkentAdmin(admin.ModelAdmin):
    list_display = ['id', 'turn', 'waiting', 'chois']
    
@admin.register(TurnofCars)
class TurnofCarsAdmin(admin.ModelAdmin):
    list_display = ['id', 'turn', 'waiting', 'chois']

@admin.register(BankShots)
class BankShotAdmin(admin.ModelAdmin):
    list_display = ['id', 'bank_name', 'shot_numbers','bank_sum']
    
@admin.register(Order)
class OrderAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'customer', 'seller','summa_total', 'status','tegirmon', 'date', 'get_baskets']
    list_filter = ['seller','tegirmon']
    search_fields = ('customer__name', 'seller__username', 'seller__first_name')
    date_hierarchy = 'date'
    list_display_links = ('id', 'customer', 'seller')
    def get_baskets(self, obj):
        return ",".join([str(p.id) for p in obj.baskets.all()]) 

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'miqdori','hajmi', 'price','load']
    list_filter = ['product']
    list_display_links = ('id', 'product', 'miqdori')
    
admin.site.register(CashConvertHistory)
admin.site.register(ReturnedIncomeTinHistory)
admin.site.register(ReturnedExpanseTinHistory)
admin.site.register(ChiqimCategory)
admin.site.register(ChiqimSubCategory)
admin.site.register(BaskCounter)
admin.site.register(Currency)
admin.site.register(Qaytuv)
admin.site.register(BasketQaytuv)
admin.site.register(Barcodes)
admin.site.register(ProductionHistory)
admin.site.register(ResidualBranches)
admin.site.register(Expanse)
admin.site.register(Sendedsms)
admin.site.register(TypeofTin)
admin.site.register(ClientTin)
admin.site.register(Tinhistory)
admin.site.register(Tin)
admin.site.register(Tarozi)
admin.site.register(SMSTemplate)
admin.site.register(SMSHistory)
admin.site.register(CheckClientType)
admin.site.register(CheckCustomerType)
admin.site.register(ExpanceTin)
admin.site.register(ConvertHistory)
