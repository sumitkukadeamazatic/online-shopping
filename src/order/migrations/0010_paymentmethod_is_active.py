# Generated by Django 2.0.7 on 2018-10-10 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20181009_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
