# Generated by Django 2.1.2 on 2018-12-11 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0074_auto_20181205_0907'),
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
