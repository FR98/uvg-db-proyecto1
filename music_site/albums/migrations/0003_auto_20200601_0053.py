# Generated by Django 3.0.4 on 2020-06-01 00:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0002_auto_20200324_0620'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='albumid',
            new_name='id',
        ),
    ]