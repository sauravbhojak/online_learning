# Generated by Django 2.0 on 2021-07-10 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_remove_buyer_course_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyer',
            name='student_id',
        ),
    ]
