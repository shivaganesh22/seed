# Generated by Django 5.0.6 on 2024-06-19 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("react", "0008_alter_eachstream_is_uploaded"),
    ]

    operations = [
        migrations.AddField(
            model_name="eachstream",
            name="is_edited",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="eachstream",
            name="link",
            field=models.CharField(max_length=1500),
        ),
    ]