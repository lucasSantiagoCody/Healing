# Generated by Django 5.0.4 on 2024-04-27 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_rename_doctordata_doctor_remove_opendate_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialty',
            name='specialty',
            field=models.CharField(choices=[('pdt', 'Pediatria'), ('dgt', 'Dermatologista'), ('cgt', 'Cardiologista'), ('odt', 'Ortopedista')], max_length=3),
        ),
    ]
