# Generated by Django 2.2.3 on 2021-03-22 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0003_producto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('apellido', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('direccion', models.TextField()),
            ],
        ),
    ]
