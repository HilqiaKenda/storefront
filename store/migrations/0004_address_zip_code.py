# Generated by Django 5.1.1 on 2024-10-03 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_add_slug_to_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='zip_code',
            field=models.CharField(default='_', max_length=6),
            preserve_default=False,
        ),
    ]
