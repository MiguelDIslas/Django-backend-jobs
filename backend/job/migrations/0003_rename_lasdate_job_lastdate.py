# Generated by Django 4.0.5 on 2022-07-01 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_candidatesapplied'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='lasDate',
            new_name='lastDate',
        ),
    ]