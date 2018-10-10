# Generated by Django 2.0.7 on 2018-10-08 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_merge_20180919_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='product',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='product_seller',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='product.ProductSeller'),
            preserve_default=False,
        ),
    ]
