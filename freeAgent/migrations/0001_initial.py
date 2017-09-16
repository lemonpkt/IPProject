# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-16 05:12
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('user_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('category', models.BooleanField(default=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.IntegerField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('description', models.CharField(max_length=300)),
                ('title', models.CharField(max_length=100)),
                ('cost', models.DecimalField(decimal_places=15, max_digits=30)),
                ('pub_date', models.DateTimeField(verbose_name='date created')),
                ('code', models.FileField(upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('project_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='freeAgent.Project')),
                ('project_rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='freeAgent.Member'),
        ),
        migrations.AddField(
            model_name='project',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worker', to='freeAgent.Member'),
        ),
    ]
