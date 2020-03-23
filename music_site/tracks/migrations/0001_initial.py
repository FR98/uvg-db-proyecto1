# Generated by Django 3.0.4 on 2020-03-23 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('albums', '0001_initial'),
        ('mediaTypes', '0001_initial'),
        ('genres', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('trackid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('composer', models.CharField(blank=True, max_length=220, null=True)),
                ('milliseconds', models.IntegerField()),
                ('bytes', models.IntegerField()),
                ('unitprice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('albumid', models.ForeignKey(db_column='albumid', on_delete=django.db.models.deletion.DO_NOTHING, to='albums.Album')),
                ('genreid', models.ForeignKey(db_column='genreid', on_delete=django.db.models.deletion.DO_NOTHING, to='genres.Genre')),
                ('mediatypeid', models.ForeignKey(db_column='mediatypeid', on_delete=django.db.models.deletion.DO_NOTHING, to='mediaTypes.MediaType')),
            ],
            options={
                'db_table': 'track',
            },
        ),
    ]
