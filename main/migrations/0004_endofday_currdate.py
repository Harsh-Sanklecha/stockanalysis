# Generated by Django 3.1.2 on 2020-12-12 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20201128_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='endofday',
            name='currDate',
            field=models.CharField(max_length=30, null=True),
        ),
    ]