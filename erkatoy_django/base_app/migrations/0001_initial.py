# Generated by Django 5.0.6 on 2024-07-02 12:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name_uz", models.CharField(max_length=50)),
                ("name_ru", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Content",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        choices=[("uz", "Uz"), ("ru", "Ru")], max_length=25
                    ),
                ),
                ("title", models.CharField(max_length=256)),
                ("text", models.TextField()),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="base_app.category",
                    ),
                ),
            ],
        ),
    ]