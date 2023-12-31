# Generated by Django 4.2.4 on 2023-08-29 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobTitle",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "JobTitle",
                "verbose_name_plural": "JobTitles",
            },
        ),
        migrations.AlterField(
            model_name="employee",
            name="job_title",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="job_title",
                to="accounts.jobtitle",
            ),
        ),
    ]
