# Generated by Django 3.2.4 on 2022-03-01 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_auto_20220301_1034'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bankshots',
            options={'verbose_name_plural': 'Bank hisob raqamlar'},
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]
