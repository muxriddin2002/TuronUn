# Generated by Django 3.2.4 on 2022-04-07 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0097_employee_firebase_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='type',
            field=models.IntegerField(choices=[(1, 'Director'), (2, 'Accounter'), (3, 'Manager'), (4, 'Sotuvchi'), (5, 'Qoravul'), (6, 'Omborchi asosiy'), (7, 'Tarozi_hisobchi bon'), (8, 'Tarozi_hisobchi Xisobchi'), (9, 'Tarozi_hisobchi Moliyachi'), (10, 'Texnolog'), (11, 'Omborchi filial'), (12, 'Kassir'), (13, 'Yem Production'), (14, 'Un Production'), (15, 'Yem Ombor'), (16, 'Un Ombor'), (17, 'Sotuv rahbari'), (18, 'Operator'), (19, 'Ombor kassir'), (20, 'Qoravul + Asosiy Ombor'), (21, 'Yordamchi bugalter')], default=0),
        ),
    ]
