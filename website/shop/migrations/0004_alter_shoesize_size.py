# Generated by Django 5.0.4 on 2024-04-26 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rename_image_item_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoesize',
            name='size',
            field=models.DecimalField(decimal_places=2, max_digits=3, unique=True),
        ),
    ]