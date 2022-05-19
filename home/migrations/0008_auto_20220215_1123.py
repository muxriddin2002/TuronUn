# Generated by Django 3.2.4 on 2022-02-15 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20220210_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankShot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'BankShots-(BankShot)',
            },
        ),
        migrations.AlterModelOptions(
            name='cash',
            options={'verbose_name_plural': 'Kassa-(Cash)'},
        ),
        migrations.CreateModel(
            name='Kassa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naqd_pull_sum', models.DecimalField(decimal_places=2, default=0, max_digits=155)),
                ('naqd_pull_dollor', models.DecimalField(decimal_places=2, default=0, max_digits=155)),
                ('bank_shot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.bankshot')),
            ],
            options={
                'verbose_name_plural': 'Kassa',
            },
        ),
    ]
