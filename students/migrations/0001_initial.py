# Generated by Django 5.2.4 on 2025-07-03 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.CharField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=100)),
            ],
        ),
    ]
