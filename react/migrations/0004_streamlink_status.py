# Generated by Django 5.0.6 on 2024-06-18 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("react", "0003_eachstream"),
    ]

    operations = [
        migrations.AddField(
            model_name="streamlink",
            name="status",
            field=models.BooleanField(default=True),
        ),
    ]