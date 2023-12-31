# Generated by Django 2.1.3 on 2019-02-22 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20190217_0825'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clientsession',
            options={'default_permissions': (), 'permissions': (), 'verbose_name_plural': 'Client Session'},
        ),
        migrations.AlterModelOptions(
            name='customeruser',
            options={'default_permissions': (), 'permissions': (), 'verbose_name_plural': 'Users of Customers'},
        ),
        migrations.AlterModelOptions(
            name='employeeservice',
            options={'default_permissions': (), 'permissions': (), 'verbose_name_plural': 'Services of Employees'},
        ),
        migrations.AlterModelOptions(
            name='employeeuser',
            options={'default_permissions': (), 'permissions': (), 'verbose_name_plural': 'Users of Employees'},
        ),
        migrations.AlterModelOptions(
            name='servicebooking',
            options={'default_permissions': (), 'permissions': (), 'verbose_name_plural': 'Services of Bookings'},
        ),
        migrations.AlterModelOptions(
            name='sessionimages',
            options={'default_permissions': (), 'permissions': (), 'verbose_name_plural': 'Images'},
        ),
    ]
