# Generated by Django 5.0.6 on 2024-07-04 06:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base_app", "0004_alter_content_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="content",
            name="image",
            field=models.FileField(
                blank=True, default=None, null=True, upload_to="images/"
            ),
        ),
    ]