# Generated by Django 2.0.7 on 2018-07-26 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_auto_20180726_0728'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('address_line', models.TextField()),
                ('city', models.CharField(max_length=60)),
                ('state', models.CharField(max_length=60)),
                ('pincode', models.CharField(max_length=10)),
                ('is_home', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('title', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'review',
            },
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50)),
                ('contact_number', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'db_table': 'seller',
            },
        ),
        migrations.AddField(
            model_name='review',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Seller'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddField(
            model_name='address',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Seller'),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddIndex(
            model_name='seller',
            index=models.Index(fields=['company_name', 'created_at', 'updated_at'], name='seller_index'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['rating', 'created_at', 'updated_at'], name='review_index'),
        ),
        migrations.AddIndex(
            model_name='address',
            index=models.Index(fields=['pincode', 'state', 'city', 'created_at', 'updated_at'], name='address_index'),
        ),
    ]
