# Generated by Django 5.1.1 on 2024-10-31 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_customers_alter_address_customer_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Collections',
            new_name='Collection',
        ),
        migrations.RenameModel(
            old_name='Customers',
            new_name='Customer',
        ),
    ]
