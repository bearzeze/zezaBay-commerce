# Generated by Django 4.1.3 on 2023-04-04 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='img_URL',
            field=models.URLField(default='https://www.postermywall.com/index.php/poster/view/20f626b12d9207649f81a24f4ce48308'),
        ),
    ]