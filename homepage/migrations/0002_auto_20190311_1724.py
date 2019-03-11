# Generated by Django 2.1.3 on 2019-03-11 21:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['date']},
        ),
        migrations.AddField(
            model_name='event',
            name='address2',
            field=models.CharField(blank=True, max_length=140),
        ),
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.CharField(default='', max_length=140),
        ),
        migrations.AddField(
            model_name='event',
            name='display',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='event',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=10, editable=False, max_digits=13, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='link',
            field=models.URLField(blank=True, max_length=140, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=10, editable=False, max_digits=13, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='state',
            field=models.CharField(default='', max_length=2),
        ),
        migrations.AddField(
            model_name='event',
            name='submitter',
            field=models.CharField(default='', max_length=140),
        ),
        migrations.AlterField(
            model_name='event',
            name='address',
            field=models.CharField(max_length=140, validators=[django.core.validators.RegexValidator(message='Enter only letters or numbers', regex='^[a-zA-Z0-9 .-]+$')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='body',
            field=models.TextField(blank=True),
        ),
    ]
