# Generated by Django 2.0.7 on 2018-10-08 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_merge_20180919_1407'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='parent_id',
            new_name='parent',
        ),
    ]
