# Generated by Django 2.0.7 on 2018-08-16 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lineitem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('quantity', models.PositiveIntegerField()),
                ('reason', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(max_length=50)),
                ('lineitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Lineitem')),
            ],
        ),
        migrations.CreateModel(
            name='LineitemShippingDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('quantity', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('return_lineitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='return.Lineitem')),
                ('shipping_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.ShippingDetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('status', models.CharField(max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('status', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('return_lineitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='return.Lineitem')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='lineitem',
            name='return_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='return.Order'),
        ),
        migrations.AddIndex(
            model_name='lineitem',
            index=models.Index(fields=['status', 'reason'], name='return_lineitem_index'),
        ),
    ]
