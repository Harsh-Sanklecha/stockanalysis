# Generated by Django 3.1.2 on 2021-01-04 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20201212_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='endofday',
            name='report',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]