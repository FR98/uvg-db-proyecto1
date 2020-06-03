# Generated by Django 3.0.4 on 2020-06-01 03:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0002_auto_20200324_0620'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='userid',
            field=models.ForeignKey(blank=True, db_column='userid', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]