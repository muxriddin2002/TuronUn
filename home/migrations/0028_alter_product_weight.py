# Generated by Django 3.2.4 on 2022-02-27 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_employee_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.FloatField(blank=True, default=0, help_text='25kg = 1qob', null=True),
        ),
    ]
