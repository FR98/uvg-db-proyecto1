# Generated by Django 3.0.4 on 2020-03-23 01:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tracks', '0001_initial'),
        ('playlists', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaylistTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlistid', models.ForeignKey(db_column='playlistid', on_delete=django.db.models.deletion.DO_NOTHING, to='playlists.Playlist')),
                ('trackid', models.ForeignKey(db_column='trackid', on_delete=django.db.models.deletion.DO_NOTHING, to='tracks.Track')),
            ],
            options={
                'db_table': 'playlisttrack',
            },
        ),
    ]
