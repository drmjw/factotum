# Generated by Django 2.1.2 on 2018-12-19 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0077_rawchem'),
    ]

    operations = [
        migrations.AddField(
            model_name='extractedchemical',
            name='rawchem_ptr_temp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.RawChem'),
        ),
        migrations.AddField(
            model_name='extractedfunctionaluse',
            name='rawchem_ptr_temp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.RawChem'),
        ),
        migrations.AddField(
            model_name='extractedlistpresence',
            name='rawchem_ptr_temp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.RawChem'),
        ),
        migrations.AddField(
            model_name='dsstoxsubstance',
            name='rawchem_ptr_temp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.RawChem'),
        ),
    ]
