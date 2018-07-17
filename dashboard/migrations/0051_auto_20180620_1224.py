# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-20 12:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0050_auto_20180611_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtractedFunctionalUse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('raw_cas', models.CharField(blank=True, max_length=50, null=True, verbose_name='Raw CAS')),
                ('raw_chem_name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Raw chemical name')),
                ('report_funcuse', models.CharField(blank=True, max_length=100, null=True, verbose_name='Reported functional use')),
                ('extracted_text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uses', to='dashboard.ExtractedText')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='extractedchemical',
            name='extracted_text',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chemicals', to='dashboard.ExtractedText'),
        ),
        migrations.AlterField(
            model_name='extractedchemical',
            name='raw_cas',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Raw CAS'),
        ),
        migrations.AlterField(
            model_name='extractedchemical',
            name='raw_chem_name',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Raw chemical name'),
        ),
        migrations.AlterField(
            model_name='extractedchemical',
            name='raw_max_comp',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Raw maximum composition'),
        ),
        migrations.AlterField(
            model_name='extractedchemical',
            name='raw_min_comp',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Raw minimum composition'),
        ),
        migrations.AlterField(
            model_name='extractedchemical',
            name='report_funcuse',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Reported functional use'),
        ),
    ]