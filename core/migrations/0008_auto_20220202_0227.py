# Generated by Django 2.2.3 on 2022-02-01 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20220202_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='prn',
            field=models.BigIntegerField(default=1212, null=True),
        ),
    ]
