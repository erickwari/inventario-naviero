# Generated by Django 5.2.2 on 2025-06-09 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0007_remove_servicio_empleado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
    ]
