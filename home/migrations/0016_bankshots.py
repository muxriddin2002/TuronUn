# Generated by Django 3.2.4 on 2022-02-16 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_paymenthistory_bank_shot'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankShots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shot_numbers', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
