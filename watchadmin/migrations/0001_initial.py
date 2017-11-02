# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-17 09:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderid', models.IntegerField()),
                ('goodsid', models.IntegerField()),
                ('name', models.CharField(max_length=32)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('num', models.IntegerField()),
            ],
            options={
                'db_table': 'watchapp_detail',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeid', models.IntegerField()),
                ('goods', models.CharField(max_length=32)),
                ('company', models.CharField(max_length=50)),
                ('descr', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('picname', models.CharField(max_length=255)),
                ('state', models.IntegerField(default=1)),
                ('store', models.IntegerField(default=0)),
                ('num', models.IntegerField(default=0)),
                ('clicknum', models.IntegerField(default=0)),
                ('addtime', models.IntegerField()),
            ],
            options={
                'db_table': 'watchapp_goods',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField()),
                ('linkman', models.CharField(max_length=32)),
                ('address', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=6)),
                ('phone', models.CharField(max_length=16)),
                ('addtime', models.IntegerField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('state', models.IntegerField()),
            ],
            options={
                'db_table': 'watchapp_orders',
            },
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('pid', models.IntegerField(default=0)),
                ('path', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'watchapp_types',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('name', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=32)),
                ('sex', models.IntegerField()),
                ('address', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=6)),
                ('phone', models.CharField(max_length=16)),
                ('email', models.CharField(max_length=50)),
                ('state', models.IntegerField(default=1)),
                ('addtime', models.IntegerField()),
            ],
            options={
                'db_table': 'watchapp_users',
            },
        ),
    ]
