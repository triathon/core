# Generated by Django 3.2.15 on 2022-09-29 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20220929_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='contract',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='functions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='result',
            field=models.TextField(default='{}'),
        ),
    ]