# Generated by Django 2.2.3 on 2022-01-27 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20220127_2137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='first_name',
            new_name='first_name1',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='last_name',
            new_name='last_name1',
        ),
    ]
