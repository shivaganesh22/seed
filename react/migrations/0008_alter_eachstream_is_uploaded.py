# Generated by Django 5.0.6 on 2024-06-19 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("react", "0007_eachstream_is_uploaded"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eachstream",
            name="is_uploaded",
            field=models.BooleanField(default=False),
        ),
    ]