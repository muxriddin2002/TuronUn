# Generated by Django 3.2.4 on 2022-05-19 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0101_alter_bankshots_shot_numbers'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_payment',
            field=models.DateField(blank=True, null=True),
        ),
    ]
