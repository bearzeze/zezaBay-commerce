# Generated by Django 4.1.3 on 2023-04-12 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_item_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='img_URL',
            field=models.URLField(default='https://d1csarkz8obe9u.cloudfront.net/posterpreviews/bjj-logo-design-template-20f626b12d9207649f81a24f4ce48308_screen.jpg?ts=1678120477'),
        ),
    ]
