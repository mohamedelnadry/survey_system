# Generated by Django 4.2.4 on 2023-08-31 13:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "survey",
            "0006_remove_answer_employee_remove_answer_response_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="survey",
            old_name="survey",
            new_name="questions",
        ),
    ]
