# Generated by Django 2.2.3 on 2021-03-21 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='img',
            field=models.ImageField(null=True, upload_to='categoria'),
        ),
    ]
