# Generated by Django 3.2.4 on 2022-03-04 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0058_expanse_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('1', 'Active'), ('2', 'In process'), ('3', 'Process done'), ('4', 'Finished'), ('5', 'Rejected')], default=1, max_length=50),
        ),
    ]
