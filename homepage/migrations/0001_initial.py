# Generated by Django 2.0.7 on 2018-07-26 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('body', models.TextField()),
                ('date', models.DateTimeField()),
                ('address', models.CharField(max_length=140)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
