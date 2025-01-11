# Generated by Django 5.1.4 on 2025-01-09 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MotionSensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_motion_detected', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SmartLight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('state', models.BooleanField(default=False)),
                ('brightness', models.IntegerField(default=100)),
                ('color', models.CharField(default='White', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Thermostat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('current_temperature', models.FloatField()),
                ('target_temperature', models.FloatField()),
            ],
        ),
    ]