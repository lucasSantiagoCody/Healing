# Generated by Django 5.0.4 on 2024-04-27 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0004_alter_specialty_specialty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialty',
            name='specialty',
            field=models.CharField(max_length=100),
        ),
    ]
