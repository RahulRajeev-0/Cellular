# Generated by Django 4.2.5 on 2023-10-16 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_payment_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=100),
        ),
    ]
