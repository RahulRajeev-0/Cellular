# Generated by Django 4.2.5 on 2023-10-24 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=10)),
                ('is_expired', models.BooleanField(default=False)),
                ('discount_price', models.IntegerField(default=100)),
                ('minimium_amount', models.IntegerField(default=5000)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Completed', 'Completed'), ('Cancel', 'Cancel'), ('Cancelled', 'Cancelled'), ('Cancelled by Admin', 'Cancelled by Admin'), ('Return', 'Return'), ('Returned', 'Returned')], default='New', max_length=30),
        ),
    ]
