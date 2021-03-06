# Generated by Django 3.0.4 on 2020-06-01 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0003_customer_userid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='customerid',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='userid',
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
