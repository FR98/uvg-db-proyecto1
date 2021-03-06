# Generated by Django 3.0.4 on 2020-03-24 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tracks', '0001_initial'),
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceLine',
            fields=[
                ('invoicelineid', models.IntegerField(primary_key=True, serialize=False)),
                ('unitprice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('invoiceid', models.ForeignKey(db_column='invoiceid', on_delete=django.db.models.deletion.DO_NOTHING, to='invoices.Invoice')),
                ('trackid', models.ForeignKey(db_column='trackid', on_delete=django.db.models.deletion.DO_NOTHING, to='tracks.Track')),
            ],
            options={
                'db_table': 'invoiceline',
            },
        ),
    ]
