# Generated by Django 5.0.4 on 2024-05-05 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_fcm_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fcm_token",
            name="token",
            field=models.CharField(max_length=500, unique=True),
        ),
    ]
