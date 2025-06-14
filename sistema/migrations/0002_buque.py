# Generated by Django 5.2.2 on 2025-06-08 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buque',
            fields=[
                ('numero_buque', models.AutoField(primary_key=True, serialize=False)),
                ('altura', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ancho', models.DecimalField(decimal_places=2, max_digits=10)),
                ('largo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cap_max_carga', models.DecimalField(decimal_places=2, max_digits=12)),
                ('cant_trabajadores', models.IntegerField()),
            ],
        ),
    ]
