# Generated by Django 3.1.3 on 2020-11-18 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='pick_up_comment',
            field=models.TextField(null=True),
        ),
    ]
