# Generated by Django 3.2.5 on 2023-05-09 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20230508_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewrating',
            name='sentiment',
        ),
    ]
