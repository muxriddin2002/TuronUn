# Generated by Django 3.2.4 on 2022-03-07 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0066_auto_20220307_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='converthistory',
            name='currency',
            field=models.PositiveIntegerField(default=0, max_length=155),
        ),
    ]
