# Generated by Django 3.2.4 on 2022-03-01 05:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_customer_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConvertHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dollor', models.DecimalField(decimal_places=2, default=0, max_digits=155)),
                ('som', models.DecimalField(decimal_places=2, default=0, max_digits=155)),
                ('currency', models.DecimalField(decimal_places=2, default=0, max_digits=155)),
                ('converter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]
