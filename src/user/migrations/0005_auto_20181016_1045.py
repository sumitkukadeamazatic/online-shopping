# Generated by Django 2.0.7 on 2018-10-16 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_resetpassword_is_reset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='users/profile_pics'),
        ),
    ]
