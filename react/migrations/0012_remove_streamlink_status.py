# Generated by Django 5.0.6 on 2024-06-20 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("react", "0011_streamlink_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="streamlink",
            name="status",
        ),
    ]
