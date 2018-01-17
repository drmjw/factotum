# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-10 21:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_remove_productdocument_upc'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gen_cat', models.CharField(max_length=50)),
                ('prod_fam', models.CharField(blank=True, max_length=50, null=True)),
                ('prod_type', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='data_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='dashboard.DataSource'),
        ),
        migrations.AddField(
            model_name='product',
            name='prod_cat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='dashboard.ProductCategory'),
            preserve_default=False,
        ),
    ]