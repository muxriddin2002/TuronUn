# Generated by Django 3.2.4 on 2022-03-26 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0088_alter_employee_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basket',
            options={'verbose_name': 'Savatcha', 'verbose_name_plural': 'Savatchalar'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Mijoz', 'verbose_name_plural': 'Mijozlar'},
        ),
    ]
