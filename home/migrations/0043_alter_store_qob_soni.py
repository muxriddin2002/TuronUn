# Generated by Django 3.2.4 on 2022-03-02 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0042_merge_20220301_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='qob_soni',
            field=models.IntegerField(blank=True, default=0, help_text='Auto calculate', null=True),
        ),
    ]
