# Generated by Django 5.0.4 on 2024-05-05 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_movierulz"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movierulz",
            name="link",
            field=models.CharField(max_length=1000),
        ),
    ]
