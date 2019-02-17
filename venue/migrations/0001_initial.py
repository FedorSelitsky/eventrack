# Generated by Django 2.1.5 on 2019-02-04 20:20

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(default='', max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip', models.CharField(default='', max_length=255)),
                ('name', models.CharField(default='', max_length=255)),
                ('phone', models.CharField(default='', max_length=255)),
                ('street', models.CharField(default='', max_length=255)),
                ('capacity', models.IntegerField(null=True)),
                ('description', models.TextField(default='')),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('website', models.URLField(default='')),
                ('songkick_url', models.URLField(default='')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='venues', to='venue.Location')),
            ],
        ),
    ]
