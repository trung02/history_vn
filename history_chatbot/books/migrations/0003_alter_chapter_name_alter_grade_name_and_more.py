# Generated by Django 4.2.8 on 2024-05-06 07:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0002_title_content_delete_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chapter",
            name="name",
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name="grade",
            name="name",
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="name",
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name="title",
            name="content",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="title",
            name="name",
            field=models.CharField(max_length=500),
        ),
    ]