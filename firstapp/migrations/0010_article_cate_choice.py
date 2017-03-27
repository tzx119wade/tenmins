# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-26 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0009_article_editor_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cate_choice',
            field=models.CharField(blank=True, choices=[('best', 'best'), ('hot', 'hot')], max_length=10, null=True),
        ),
    ]