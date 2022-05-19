from rest_framework import serializers
from home.models import *

class TypeofProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeofProduct
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    type = TypeofProductSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

class TegirmonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tegirmon
        fields = "__all__"

class Return_productSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    tegirmon = TegirmonSerializer(read_only=True)

    class Meta:
        model = Return_product
        fields = "__all__"

class ProductionHistorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    tegirmon = TegirmonSerializer(read_only=True)

    class Meta:
        model = ProductionHistory
        fields = "__all__"

class StoreSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    type = TypeofProductSerializer(read_only=True)
    tegirmon = TegirmonSerializer(read_only=True)

    class Meta:
        model = Store
        fields = "__all__"


class StoreHistorySerializer(serializers.ModelSerializer):
    tegirmon = TegirmonSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = StoreHistory
        fields = "__all__"

class BrigadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brigada
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class TypeOutlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOutlay
        fields = "__all__"

class AktOutlaySerializer(serializers.ModelSerializer):
    type = TypeOutlaySerializer(read_only=True)

    class Meta:
        model = AktOutlay
        fields = "__all__"

class BasketQaytuvSerializer(serializers.ModelSerializer):
    product = StoreSerializer(read_only=True)
    type = TypeofProductSerializer(read_only=True)

    class Meta:
        model = BasketQaytuv
        fields = "__all__"

class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = "__all__"

        extra_kwargs = {'password': {'write_only': True}}

class BasketSerializer(serializers.ModelSerializer):
    product = StoreSerializer(read_only=True)
    type = TypeofProductSerializer(read_only=True)

    class Meta:
        model = Basket
        fields = "__all__"


class OrderIdMijozSanaSerializer(serializers.ModelSerializer):
    mijoz = serializers.SerializerMethodField()
    sana = serializers.CharField(source='date')

    def get_mijoz(self, obj):
        customer = Customer.objects.get(id=obj.customer.id)
        
        return customer.name

    class Meta:
        model = Order
        fields = ['id', 'mijoz', 'sana']


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    baskets = BasketSerializer(many=True, read_only=True)
    seller = EmployeeSerializer(read_only=True)
    # left_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

class QaytuvSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Qaytuv
        fields = "__all__"

class ClientSerializerTarozi(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'compony']

class ClientUnSerializerTarozi(serializers.ModelSerializer):
    class Meta:
        model = ClientUn
        fields = ['id', 'compony']

#branch
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"

#bugdoy wagon
class WagonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AktWagon
        fields = ['id', 'number', "brutto_fakt",
                  "tara_fakt",
                  "netto_fakt",  ]

# un wagon
class UnWagonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AktUnWagon
        fields = ['id', 'number', "brutto_fakt",
                  "tara_fakt",
                  "netto_fakt", "product", ]

#bugdoy akt serializer
class AktSerializer(serializers.ModelSerializer):
    total_netto = serializers.SerializerMethodField()
    vagon_soni = serializers.SerializerMethodField()
    client = ClientSerializerTarozi(read_only=True)
    # branch = BranchSerializer(read_only=True)
    branch = TegirmonSerializer(read_only=True)

    class Meta:
        model = Akt
        fields = [
            "id",
            "name",
            "client",
            "stansiya",
            "branch",
            "date_start",
            "date_end",
            "status",
            'total_netto',
            'vagon_soni',
            'is_edited'
        ]

    def get_total_netto(self, obj):
        return sum(wg.netto_akt for wg in obj.wagons.all())

    def get_vagon_soni(self, obj):
        return obj.wagons.all().count()

# un akt serializer
class UnAktSerializer(serializers.ModelSerializer):
    total_netto = serializers.SerializerMethodField()
    vagon_soni = serializers.SerializerMethodField()
    client = ClientUnSerializerTarozi(read_only=True)
    # branch = BranchSerializer(read_only=True)
    ombor = TegirmonSerializer(read_only=True)
    wagons = UnWagonSerializer(many=True, read_only=True)
    class Meta:
        model = UnAkt
        fields = [
            "id",
            "wagons",
            "client",
            "stansiya",
            "ombor",
            "date_start",
            "date_end",
            "status",
            'total_netto',
            'vagon_soni',
            'is_edited'
        ]

    def get_total_netto(self, obj):
        return sum(wg.netto_akt for wg in obj.wagons.all())

    def get_vagon_soni(self, obj):
        return obj.wagons.all().count()

class TurnofCarsSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = TurnofCars
        fields = "__all__"

class TurnofCarsofTashkentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = TurnofCarsofTashkent
        fields = "__all__"

class ClientTinSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientTin
        fields = "__all__"

class TypeofTinSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeofTin
        fields = "__all__"

class TinhistorySerializer(serializers.ModelSerializer):
    client = ClientTinSerializer(read_only=True)
    type = TypeofTinSerializer(read_only=True)

    class Meta:
        model = Tinhistory
        fields = "__all__"

class TinSerializer(serializers.ModelSerializer):
    type = TypeofTinSerializer(read_only=True)
    tegirmon = TegirmonSerializer(read_only=True)

    class Meta:
        model = Tin
        fields = "__all__"

class ExpanceTinSerializer(serializers.ModelSerializer):
    
    type = TypeofTinSerializer(read_only=True)

    class Meta:
        model = ExpanceTin
        fields = "__all__"

class ReturnedIncomeTinHistoryTinSerializer(serializers.ModelSerializer):
    
    type = TypeofTinSerializer(read_only=True)

    class Meta:
        model = ReturnedIncomeTinHistory
        fields = "__all__"
        

class ReturnedExpanseTinHistoryTinSerializer(serializers.ModelSerializer):
    
    type = TypeofTinSerializer(read_only=True)

    class Meta:
        model = ReturnedIncomeTinHistory
        fields = "__all__"
        
