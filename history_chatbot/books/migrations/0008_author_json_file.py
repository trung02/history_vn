# Generated by Django 4.2.8 on 2024-06-19 15:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0007_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="json_file",
            field=models.JSONField(default=""),
        ),
    ]