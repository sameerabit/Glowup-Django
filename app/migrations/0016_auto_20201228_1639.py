# Generated by Django 3.1.4 on 2020-12-28 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_auto_20190216_0422'),
        ('app', '0015_auto_20190520_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.ForeignKey(blank=True, db_column='status', limit_choices_to={'is_active': True, 'type_category': 1}, null=True, on_delete=django.db.models.deletion.CASCADE, to='config.type', verbose_name='Status'),
        ),
    ]