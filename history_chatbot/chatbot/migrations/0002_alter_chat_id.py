# Generated by Django 4.2.8 on 2024-05-27 15:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("chatbot", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chat",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid1, primary_key=True, serialize=False
            ),
        ),
    ]