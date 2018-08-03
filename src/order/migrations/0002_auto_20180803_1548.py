# Generated by Django 2.0.7 on 2018-08-03 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('order', '0001_initial'),
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Address'),
        ),
        migrations.AddField(
            model_name='order',
            name='cart_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Cart'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.PaymentMethod'),
        ),
        migrations.AddField(
            model_name='lineshippingdetails',
            name='lineitem_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Lineitem'),
        ),
        migrations.AddField(
            model_name='lineshippingdetails',
            name='shiping_details_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.ShippingDetails'),
        ),
        migrations.AddField(
            model_name='lineitemtax',
            name='lineitem_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Lineitem'),
        ),
        migrations.AddField(
            model_name='lineitem',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order'),
        ),
        migrations.AddField(
            model_name='lineitem',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product'),
        ),
        migrations.AddField(
            model_name='lineitem',
            name='seller_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Seller'),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='cart_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Cart'),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product'),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='seller_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Seller'),
        ),
    ]
