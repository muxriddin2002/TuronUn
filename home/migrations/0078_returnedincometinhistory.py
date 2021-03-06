# Generated by Django 3.2.4 on 2022-03-12 12:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0077_auto_20220311_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnedIncomeTinHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('izoh', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.typeoftin')),
            ],
        ),
    ]
