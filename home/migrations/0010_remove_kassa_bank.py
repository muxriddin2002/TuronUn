# Generated by Django 3.2.4 on 2022-02-15 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_kassa_bank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kassa',
            name='bank',
        ),
    ]
