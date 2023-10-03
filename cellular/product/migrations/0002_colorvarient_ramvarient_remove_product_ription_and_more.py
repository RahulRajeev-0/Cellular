# Generated by Django 4.2.5 on 2023-09-27 04:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorVarient',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('color_name', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RamVarient',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('ram_no', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='ription',
        ),
        migrations.AddField(
            model_name='product',
            name='color_varient',
            field=models.ManyToManyField(to='product.colorvarient'),
        ),
        migrations.AddField(
            model_name='product',
            name='ram_varient',
            field=models.ManyToManyField(to='product.ramvarient'),
        ),
    ]
