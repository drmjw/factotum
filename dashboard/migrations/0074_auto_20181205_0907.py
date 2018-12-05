# Generated by Django 2.1.2 on 2018-12-05 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0073_remove_producttopuc_puc_assigned_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='script',
            name='script_type',
            field=models.CharField(choices=[('DL', 'download'), ('EX', 'extraction'), ('PC', 'product categorization'), ('DC', 'data cleaning')], default='EX', max_length=2),
        ),
    ]