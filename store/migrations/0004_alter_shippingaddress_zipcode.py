# Generated by Django 4.0.2 on 2022-03-26 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_customer_email_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='zipcode',
            field=models.IntegerField(),
        ),
    ]
