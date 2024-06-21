# Generated by Django 4.2.8 on 2024-06-19 18:53

from django.db import migrations, models
import quiz.models


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0006_alter_examjson_json_data"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="examjson",
            name="json_data",
        ),
        migrations.AddField(
            model_name="examjson",
            name="json_file",
            field=models.FileField(
                default="", upload_to="exam/", validators=[quiz.models.validate_json]
            ),
        ),
    ]