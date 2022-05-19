# Generated by Django 3.2.4 on 2022-02-26 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_product_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankshots',
            name='bank_sum',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=155),
        ),
    ]
