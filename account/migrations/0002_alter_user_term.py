# Generated by Django 4.2 on 2023-06-10 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='term',
            field=models.BooleanField(),
        ),
    ]
