# Generated by Django 5.1.1 on 2024-10-13 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_shippingaddress_shipping_address2_order_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Shipping_address',
            new_name='shipping_address',
        ),
        migrations.AddField(
            model_name='order',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
    ]
