# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-03-15 15:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='菜单')),
                ('icon', models.CharField(blank=True, max_length=10, null=True, verbose_name='菜单图标')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='permission_module.Menu')),
            ],
            options={
                'verbose_name': '菜单',
                'verbose_name_plural': '菜单',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='权限')),
                ('url', models.CharField(max_length=128, unique=True)),
                ('icon', models.CharField(blank=True, max_length=10, null=True, verbose_name='权限图标')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='permission_module.Menu')),
            ],
            options={
                'verbose_name': '权限',
                'verbose_name_plural': '权限',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='角色')),
            ],
            options={
                'verbose_name': '角色',
                'verbose_name_plural': '角色',
            },
        ),
        migrations.AddField(
            model_name='permission',
            name='roles',
            field=models.ManyToManyField(related_name='permissions', to='permission_module.Role'),
        ),
    ]
