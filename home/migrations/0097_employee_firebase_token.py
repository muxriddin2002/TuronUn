# Generated by Django 3.2.4 on 2022-04-04 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0096_alter_product_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='firebase_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
