# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-03-22 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_module', '0003_auto_20200323_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draftarticle',
            name='label',
            field=models.ManyToManyField(blank=True, null=True, related_name='draft_article', to='blog_module.Label', verbose_name='label'),
        ),
        migrations.AlterField(
            model_name='publisharticle',
            name='label',
            field=models.ManyToManyField(blank=True, null=True, related_name='article', to='blog_module.Label', verbose_name='label'),
        ),
    ]
