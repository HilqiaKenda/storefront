# Generated by Django 5.1.1 on 2024-10-03 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_address_zip_code'),
    ]

    operations = [
        migrations.RunSQL("""
            insert into store_collections(title) values('collection1')
        """,
        """
            DELETE FROM store_collections WHERE title = 'collection1'
        """)
    ]
