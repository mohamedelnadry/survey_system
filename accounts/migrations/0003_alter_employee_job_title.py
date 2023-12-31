# Generated by Django 4.2.4 on 2023-08-29 10:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_jobtitle_alter_employee_job_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="job_title",
            field=models.ForeignKey(
                default="New",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="job_title",
                to="accounts.jobtitle",
            ),
        ),
    ]
