# Generated by Django 2.1.2 on 2018-12-20 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0076_auto_20181212_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puc',
            name='prod_fam',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='puc',
            name='prod_type',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]