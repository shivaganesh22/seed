# Generated by Django 5.0.6 on 2024-06-19 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("react", "0006_alter_eachstream_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="eachstream",
            name="is_uploaded",
            field=models.BooleanField(default=True),
        ),
    ]