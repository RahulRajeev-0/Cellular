# Generated by Django 4.2.5 on 2023-11-03 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_remove_order_coupon_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]