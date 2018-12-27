# Generated by Django 2.1.2 on 2018-12-25 04:57
from datetime import datetime
from django.db import migrations, models
import django.db.models.deletion
import dashboard.models.extracted_chemical

def switch_to_raw(apps, schema_editor):
    """ From non inehirtance to post inheritance """
    t = datetime.now()
    OldChem = apps.get_model('dashboard', 'ExtractedChemical_x')
    NewChem = apps.get_model('dashboard', 'ExtractedChemical_new')
    OldFU = apps.get_model('dashboard', 'ExtractedFunctionalUse_x')
    NewFU = apps.get_model('dashboard', 'ExtractedFunctionalUse_new')
    OldLP = apps.get_model('dashboard', 'ExtractedListPresence_x')
    NewLP = apps.get_model('dashboard', 'ExtractedListPresence_new')
    OldDSSTox = apps.get_model('dashboard', 'DSSToxSubstance')
    # NewDSSTox = apps.get_model('dashboard', 'DSSToxSubstance_new')
    for chem in OldChem.objects.all():
        dtox=None
        if OldDSSTox.objects.filter(extracted_chemical_id=chem.id):
            dtox = OldDSSTox.objects.get(extracted_chemical_id=chem.id)
            # dtox = NewDSSTox.objects.create(
            #             id=old_dss.id,
            #             true_cas=old_dss.true_cas,
            #             true_chemname=old_dss.true_chemname,
            #             rid=old_dss.rid,
            #             sid=old_dss.sid,
            #             created_at=old_dss.created_at,
            #             updated_at=old_dss.updated_at
            #         )
        new_chem = NewChem(id=chem.id,
                            raw_cas=chem.raw_cas,
                            raw_chem_name=chem.raw_chem_name,
                            raw_min_comp=chem.raw_min_comp,
                            raw_max_comp =chem.raw_max_comp,
                            report_funcuse=chem.report_funcuse,
                            ingredient_rank=chem.ingredient_rank,
                            raw_central_comp=chem.raw_central_comp,
                            extracted_text=chem.extracted_text,
                            unit_type=chem.unit_type,
                            weight_fraction_type=chem.weight_fraction_type,
                            dss_tox=dtox,
                            created_at=chem.created_at,
                            updated_at=chem.updated_at,
        )
        new_chem.save()

    for fu in OldFU.objects.all():
        new_fu = NewFU.objects.create(raw_cas=fu.raw_cas,
            raw_chem_name=fu.raw_chem_name,
            report_funcuse=fu.report_funcuse,
            extracted_text=fu.extracted_text,
            created_at=fu.created_at,
            updated_at=fu.updated_at,
            )
    for lp in OldLP.objects.all():
        new_lp = NewLP.objects.create(raw_cas=lp.raw_cas,
            raw_chem_name=lp.raw_chem_name,
            extracted_cpcat=lp.extracted_cpcat,
            created_at=lp.created_at,
            updated_at=lp.updated_at,
            )
    print(datetime.now()-t)

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0077_rawchem'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawchem',
            name='dss_tox',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.DSSToxSubstance'),
        ),
        migrations.RenameModel('ExtractedChemical', 'ExtractedChemical_x'),
        migrations.RenameModel('ExtractedFunctionalUse', 'ExtractedFunctionalUse_x'),
        migrations.RenameModel('ExtractedListPresence', 'ExtractedListPresence_x'),
        # migrations.RenameModel('DSSToxSubstance', 'DSSToxSubstance_x'),
        # migrations.CreateModel(
        #     name='DSSToxSubstance_new',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('true_cas', models.CharField(blank=True, max_length=50, null=True)),
        #         ('true_chemname', models.CharField(blank=True, max_length=500, null=True)),
        #         ('rid', models.CharField(blank=True, max_length=50, null=True)),
        #         ('sid', models.CharField(blank=True, max_length=50, null=True)),
        #         ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
        #         ('updated_at', models.DateTimeField(blank=True, null=True)),
        #     ],
        # ),
        migrations.CreateModel(
            name='ExtractedChemical_new',
            fields=[
                ('rawchem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.RawChem')),
                ('raw_min_comp', models.CharField(blank=True, max_length=100, null=True, verbose_name='Raw minimum composition')),
                ('raw_max_comp', models.CharField(blank=True, max_length=100, null=True, verbose_name='Raw maximum composition')),
                ('report_funcuse', models.CharField(blank=True, max_length=100, null=True, verbose_name='Reported functional use')),
                ('ingredient_rank', models.PositiveIntegerField(blank=True, null=True, validators=[dashboard.models.extracted_chemical.validate_ingredient_rank])),
                ('raw_central_comp', models.CharField(blank=True, max_length=100, null=True)),
                ('extracted_text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chemicals', to='dashboard.ExtractedText')),
                ('unit_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.UnitType')),
                ('weight_fraction_type', models.ForeignKey(default='1', null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.WeightFractionType')),
            ],
            options={
                'abstract': False,
            },
            bases=('dashboard.rawchem',),
        ),
        migrations.CreateModel(
            name='ExtractedFunctionalUse_new',
            fields=[
                ('rawchem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.RawChem')),
                ('report_funcuse', models.CharField(blank=True, max_length=100, null=True, verbose_name='Reported functional use')),
                ('extracted_text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uses', to='dashboard.ExtractedText')),
            ],
            options={
                'abstract': False,
            },
            bases=('dashboard.rawchem',),
        ),
        migrations.CreateModel(
            name='ExtractedListPresence_new',
            fields=[
                ('rawchem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.RawChem')),
                ('extracted_cpcat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presence', to='dashboard.ExtractedCPCat')),
            ],
            options={
                'abstract': False,
            },
            bases=('dashboard.rawchem',),
        ),
        
        migrations.RunPython(switch_to_raw, reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='dsstoxsubstance',
            name='extracted_chemical',
        ),
        migrations.DeleteModel('Ingredient'),
        # migrations.DeleteModel('DSSToxSubstance_x'),
        migrations.DeleteModel('ExtractedChemical_x'),
        migrations.RenameModel('ExtractedChemical_new', 'ExtractedChemical'),
        migrations.DeleteModel('ExtractedFunctionalUse_x'),
        migrations.RenameModel('ExtractedFunctionalUse_new', 'ExtractedFunctionalUse'),
        migrations.DeleteModel('ExtractedListPresence_x'),
        migrations.RenameModel('ExtractedListPresence_new', 'ExtractedListPresence'),
        # migrations.RenameModel('DSSToxSubstance_new', 'DSSToxSubstance'),

        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('lower_wf_analysis', models.DecimalField(blank=True, decimal_places=15, max_digits=16, null=True, validators=[dashboard.models.ingredient.validate_wf_analysis])),
                ('central_wf_analysis', models.DecimalField(blank=True, decimal_places=15, max_digits=16, null=True, validators=[dashboard.models.ingredient.validate_wf_analysis])),
                ('upper_wf_analysis', models.DecimalField(blank=True, decimal_places=15, max_digits=16, null=True, validators=[dashboard.models.ingredient.validate_wf_analysis])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='ingredient',
            name='extracted_chemical',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.ExtractedChemical'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='script',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Script'),
        ),
        migrations.AlterField(
            model_name='rawchem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='rawchem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        # migrations.AlterField(
        #     model_name='dsstoxsubstance',
        #     name='created_at',
        #     field=models.DateTimeField(auto_now_add=True, null=True),
        # ),
        # migrations.AlterField(
        #     model_name='dsstoxsubstance',
        #     name='updated_at',
        #     field=models.DateTimeField(auto_now=True, null=True),
        # ),
    ]
