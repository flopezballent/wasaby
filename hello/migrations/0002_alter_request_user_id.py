# Generated by Django 4.0.4 on 2022-07-24 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='user_id',
            field=models.CharField(max_length=200),
        ),
    ]