# Generated by Django 5.0.6 on 2024-06-19 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("react", "0005_alter_eachstream_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eachstream",
            name="link",
            field=models.URLField(max_length=1500),
        ),
    ]
