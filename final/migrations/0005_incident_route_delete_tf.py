# Generated by Django 4.1.5 on 2023-01-13 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0004_rename_mainform_stop'),
    ]

    operations = [
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stop1', models.IntegerField()),
                ('stop2', models.IntegerField()),
                ('line', models.CharField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='Tf',
        ),
    ]
