# Generated by Django 2.0 on 2021-06-25 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_wish_list_addcart_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Wish_list',
        ),
    ]
