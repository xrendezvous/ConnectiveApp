# Generated by Django 5.0.6 on 2024-06-03 05:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Contact",
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
                ("name", models.CharField(default="Name", max_length=20)),
                ("surname", models.CharField(default="Surname", max_length=20)),
                ("email", models.EmailField(max_length=254, null=True)),
                ("mobile_phone", models.CharField(max_length=20, null=True)),
                ("work_phone", models.CharField(max_length=20, null=True)),
                ("home_phone", models.CharField(max_length=20, null=True)),
                ("birthdate", models.DateField(blank=True, null=True)),
                ("is_favorite", models.BooleanField(default=False)),
                ("facebook", models.URLField(blank=True, null=True)),
                ("instagram", models.URLField(blank=True, null=True)),
                ("tiktok", models.URLField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Address",
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
                ("country", models.CharField(max_length=20, null=True)),
                ("city", models.CharField(max_length=20, null=True)),
                ("address", models.CharField(max_length=100, null=True)),
                (
                    "contact",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app_contacts.contact",
                    ),
                ),
            ],
        ),
    ]
