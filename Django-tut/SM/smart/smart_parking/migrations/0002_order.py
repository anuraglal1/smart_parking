# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-07 17:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smart_parking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('start_time', models.TimeField(blank=True)),
                ('end_time', models.TimeField(blank=True)),
                ('payment_option', models.CharField(max_length=50)),
                ('slot_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smart_parking.slot')),
            ],
        ),
    ]