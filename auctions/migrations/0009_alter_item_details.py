# Generated by Django 4.1.3 on 2023-04-07 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='details',
            field=models.TextField(default='No details available.', max_length=600),
        ),
    ]