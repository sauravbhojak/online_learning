# Generated by Django 2.0 on 2021-07-06 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210629_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='add_cart',
            name='course_id',
        ),
        migrations.RemoveField(
            model_name='add_cart',
            name='student_id',
        ),
        migrations.RemoveField(
            model_name='check_out',
            name='course_id',
        ),
        migrations.RemoveField(
            model_name='check_out',
            name='student_id',
        ),
        migrations.RemoveField(
            model_name='course',
            name='category_id',
        ),
        migrations.RemoveField(
            model_name='course',
            name='tutor_id',
        ),
        migrations.RemoveField(
            model_name='wish_list',
            name='course_id',
        ),
        migrations.RemoveField(
            model_name='wish_list',
            name='student_id',
        ),
        migrations.DeleteModel(
            name='Add_Cart',
        ),
        migrations.DeleteModel(
            name='Check_out',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='Wish_list',
        ),
    ]