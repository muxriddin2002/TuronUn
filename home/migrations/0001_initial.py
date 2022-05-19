# Generated by Django 3.2.4 on 2022-02-07 12:18

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(blank=True, max_length=25, null=True)),
                ('type', models.IntegerField(choices=[(1, 'Director'), (2, 'Accounter'), (3, 'Manager'), (4, 'Sotuvchi'), (5, 'Qoravul'), (6, 'Omborchi asosiy'), (7, 'Tarozi_hisobchi bon'), (8, 'Tarozi_hisobchi Xisobchi'), (9, 'Tarozi_hisobchi Moliyachi'), (10, 'Texnolog'), (11, 'Omborchi filial'), (12, 'Kassir'), (13, 'Yem Production'), (14, 'Un Production'), (15, 'Yem Ombor'), (16, 'Un Ombor'), (17, 'Sotuv rahbari')], default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
                'abstract': False,
                'swappable': 'AUTH_USER_MODEL',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AktUnOutlay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summa', models.FloatField(default=0)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('1', "To'lanmagan"), ('2', "To'langan")], default=1, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='AktUnWagon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('brutto_akt', models.IntegerField(default=0)),
                ('tara_akt', models.IntegerField(default=0)),
                ('netto_akt', models.IntegerField(default=0)),
                ('brutto_fakt', models.IntegerField(default=0)),
                ('tara_fakt', models.IntegerField(default=0)),
                ('netto_fakt', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='AktWagon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('brutto_akt', models.IntegerField(default=0)),
                ('tara_akt', models.IntegerField(default=0)),
                ('netto_akt', models.IntegerField(default=0)),
                ('brutto_fakt', models.IntegerField(default=0)),
                ('tara_fakt', models.IntegerField(default=0)),
                ('netto_fakt', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miqdori', models.FloatField(default=0)),
                ('hajmi', models.FloatField(default=0)),
                ('price', models.FloatField(default=0)),
                ('is_edited', models.BooleanField(default=False)),
                ('load', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BasketQaytuv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miqdori', models.FloatField(default=0)),
                ('hajmi', models.FloatField(default=0)),
                ('price', models.FloatField(default=0)),
                ('is_edited', models.BooleanField(default=False)),
                ('load', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Brigada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.DecimalField(decimal_places=2, default=0, max_digits=155)),
            ],
            options={
                'verbose_name_plural': 'Kassa',
            },
        ),
        migrations.CreateModel(
            name='CheckClientType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.IntegerField()),
                ('normal', models.IntegerField()),
                ('passive', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CheckCustomerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urtacha', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compony', models.CharField(max_length=255)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('comment', models.TextField(blank=True, max_length=1000, null=True)),
                ('debt', models.DecimalField(decimal_places=2, default=0, max_digits=155)),
            ],
        ),
        migrations.CreateModel(
            name='ClientTin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compony', models.CharField(max_length=255)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('comment', models.TextField(blank=True, max_length=1000, null=True)),
                ('debt', models.DecimalField(decimal_places=2, default=0, max_digits=155)),
                ('date_start', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ClientUn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compony', models.CharField(max_length=255)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('comment', models.TextField(blank=True, max_length=1000, null=True)),
                ('debt', models.DecimalField(decimal_places=2, default=0, max_digits=155)),
                ('date_start', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sotish_sum', models.IntegerField()),
                ('olish_sum', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('debt', models.DecimalField(decimal_places=2, default=0, max_digits=155)),
                ('hudud', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('extra_phone', models.CharField(blank=True, max_length=30, null=True)),
                ('location', models.CharField(max_length=255)),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('bank_number', models.IntegerField(blank=True, default=0, null=True)),
                ('inn', models.IntegerField(blank=True, default=0, null=True)),
                ('mfo', models.IntegerField(blank=True, default=0, null=True)),
                ('limit', models.IntegerField(blank=True, default=1000000, null=True)),
                ('birthday', models.DateField(null=True)),
                ('status', models.IntegerField(choices=[(1, 'Faol'), (2, 'Kamroq tovar oluvchilar '), (3, 'Ishlamay qolgan mijozlar ')], default=1)),
                ('status_turi', models.IntegerField(choices=[('1', 'Kup miqdorda, kam oladi'), ('2', 'Kam miqdorda, kup oladi')], default=2)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('update_date', models.DateField(default=django.utils.timezone.now)),
                ('summa_total', models.DecimalField(decimal_places=2, default=0, max_digits=155)),
                ('status', models.CharField(choices=[('1', 'Active'), ('2', 'In process'), ('3', 'Process done'), ('4', 'Finished')], default=1, max_length=50)),
                ('img', models.ImageField(blank=True, null=True, upload_to='Sended orders/')),
                ('car_number', models.CharField(blank=True, max_length=50, null=True)),
                ('driver_phone', models.CharField(blank=True, max_length=50, null=True)),
                ('type_bonus', models.CharField(blank=True, choices=[('1', 'Percent'), ('2', 'Dollar')], max_length=255, null=True)),
                ('bonus', models.IntegerField(default=0)),
                ('payment_date', models.DateField()),
                ('baskets', models.ManyToManyField(related_name='orderlar', to='home.Basket')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.customer')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('pr_code', models.PositiveIntegerField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tegirmon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TypeExpanse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TypeofProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TypeofTin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TypeOutlay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WheatHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kilo_1', models.FloatField(default=0)),
                ('kilo_2', models.FloatField(default=0)),
                ('kilo_3', models.FloatField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UnAkt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stansiya', models.CharField(blank=True, max_length=255, null=True)),
                ('date_start', models.DateField(blank=True, null=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Created'), (2, 'Accepted')], default=1)),
                ('price', models.FloatField(default=0)),
                ('comment', models.TextField(blank=True, null=True)),
                ('is_edited', models.BooleanField(default=False)),
                ('total', models.FloatField(default=0)),
                ('num1', models.CharField(blank=True, max_length=255, null=True)),
                ('num2', models.CharField(blank=True, max_length=255, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.clientun')),
                ('ombor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.tegirmon')),
                ('outlay', models.ManyToManyField(to='home.AktUnOutlay')),
                ('wagons', models.ManyToManyField(to='home.AktUnWagon')),
            ],
        ),
        migrations.CreateModel(
            name='TurnofCarsofTashkent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turn', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('waiting', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('1', 'Active'), ('2', 'Yuklanyapti'), ('3', 'Chiqib ketti')], max_length=255)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.order')),
            ],
        ),
        migrations.CreateModel(
            name='TurnofCars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turn', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('waiting', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('1', 'Active'), ('2', 'Yuklanyapti'), ('3', 'Chiqib ketti')], max_length=255)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.order')),
            ],
        ),
        migrations.CreateModel(
            name='Tinhistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('quantity', models.IntegerField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.IntegerField(default=1)),
                ('izoh', models.CharField(blank=True, max_length=255, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.clienttin')),
                ('tegirmon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.tegirmon')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.typeoftin')),
            ],
        ),
        migrations.CreateModel(
            name='Tin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('quantity', models.IntegerField()),
                ('tegirmon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.tegirmon')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.typeoftin')),
            ],
        ),
        migrations.CreateModel(
            name='Tarozi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soni', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.product')),
                ('tegirmon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.tegirmon')),
            ],
        ),
        migrations.CreateModel(
            name='StoreHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('1', 'created'), ('2', 'accepted')], max_length=50)),
                ('qopsoni', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
                ('tegirmon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.tegirmon')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('miqdori', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
                ('tegirmon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.tegirmon')),
            ],
        ),
        migrations.CreateModel(
            name='SMSTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.IntegerField(choices=[(1, "Tug'ilgan kun"), (2, 'Bayram va boshqalar')])),
                ('date', models.DateField(blank=True, null=True)),
                ('text', models.TextField(default='')),
                ('active', models.BooleanField(default=False)),
                ('customer', models.ManyToManyField(to='home.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='SMSHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('is_success', models.BooleanField(default=False)),
                ('send_count', models.IntegerField(default=0)),
                ('not_send_count', models.IntegerField(default=0)),
                ('smstemplate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.smstemplate')),
            ],
        ),
        migrations.CreateModel(
            name='Sendedsms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sms', models.CharField(max_length=2555)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.client')),
                ('clientun', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.clientun')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.customer')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Return_product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('izoh', models.CharField(max_length=255)),
                ('qopsoni', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='returned/')),
                ('status', models.IntegerField(choices=[(1, 'active'), (2, 'finished')], default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
                ('tegirmon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.tegirmon')),
            ],
        ),
        migrations.CreateModel(
            name='ResidualBranches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('url', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('filial', models.CharField(max_length=255)),
                ('manzil', models.CharField(max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
                ('saler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Qaytuv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summa_total', models.DecimalField(decimal_places=2, default=0, max_digits=155)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('1', 'Active'), ('2', 'Done')], default=1, max_length=255)),
                ('baskets', models.ManyToManyField(to='home.BasketQaytuv')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.customer')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('qopsoni', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
                ('tegirmon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.tegirmon')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.typeofproduct'),
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soni', models.IntegerField(default=0)),
                ('sotuvchi', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='plan', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.FloatField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('1', 'income'), ('2', 'expance')], max_length=255)),
                ('turi', models.CharField(choices=[('1', 'Bank'), ('2', 'Plastik'), ('3', 'Naqd')], max_length=255)),
                ('for_expance', models.BooleanField(default=False)),
                ('by_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.client')),
                ('clienttin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.clienttin')),
                ('clientun', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.clientun')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.customer')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='tegirmon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.tegirmon'),
        ),
        migrations.CreateModel(
            name='Expanse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summa', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('izoh', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('1', 'unpaid'), ('2', 'paid')], default=1, max_length=255)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.typeexpanse')),
            ],
        ),
        migrations.CreateModel(
            name='ExpanceTin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('izoh', models.CharField(max_length=255)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('quantity', models.IntegerField()),
                ('tegirmon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.tegirmon')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.typeoftin')),
            ],
        ),
        migrations.AddField(
            model_name='basketqaytuv',
            name='brigada',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.brigada'),
        ),
        migrations.AddField(
            model_name='basketqaytuv',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.store'),
        ),
        migrations.AddField(
            model_name='basket',
            name='brigada',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.brigada'),
        ),
        migrations.AddField(
            model_name='basket',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.store'),
        ),
        migrations.CreateModel(
            name='BaskCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miqdori', models.PositiveIntegerField(default=0)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.basket')),
            ],
        ),
        migrations.CreateModel(
            name='BarcodesHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
            ],
        ),
        migrations.CreateModel(
            name='Barcodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('date', models.DateField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.product')),
            ],
        ),
        migrations.AddField(
            model_name='aktunwagon',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.product'),
        ),
        migrations.AddField(
            model_name='aktunoutlay',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.typeoutlay'),
        ),
        migrations.CreateModel(
            name='AktOutlay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summa', models.FloatField(default=0)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('1', "To'lanmagan"), ('2', "To'langan")], default=1, max_length=255)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.typeoutlay')),
            ],
        ),
        migrations.CreateModel(
            name='Akt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('stansiya', models.CharField(blank=True, max_length=255, null=True)),
                ('date_start', models.DateField(blank=True, null=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Created'), (2, 'accepted')], default=1)),
                ('price', models.FloatField(default=0)),
                ('comment', models.TextField(blank=True, null=True)),
                ('is_edited', models.BooleanField(default=False)),
                ('total', models.FloatField(default=0)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.tegirmon')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.client')),
                ('outlay', models.ManyToManyField(to='home.AktOutlay')),
                ('wagons', models.ManyToManyField(to='home.AktWagon')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='tegirmon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.tegirmon'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
