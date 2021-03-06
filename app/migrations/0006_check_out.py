# Generated by Django 2.0 on 2021-06-26 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_wish_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Check_out',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Student_name', models.CharField(max_length=100)),
                ('State', models.CharField(max_length=100)),
                ('City', models.CharField(max_length=100)),
                ('Address', models.CharField(max_length=200)),
                ('Pincode', models.IntegerField()),
                ('Phone', models.IntegerField()),
                ('Course_name', models.CharField(max_length=100)),
                ('Course_price', models.IntegerField()),
                ('Total', models.IntegerField()),
                ('Subtotal', models.IntegerField()),
                ('is_created', models.DateTimeField(auto_now_add=True)),
                ('is_updated', models.DateTimeField(auto_now_add=True)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Course')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Student')),
            ],
        ),
    ]
