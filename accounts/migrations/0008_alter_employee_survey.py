# Generated by Django 4.2.4 on 2023-08-31 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_rename_survey_survey_questions'),
        ('accounts', '0007_employee_survey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='survey',
            field=models.ManyToManyField(blank=True, null=True, related_name='employee_surveys', to='survey.survey'),
        ),
    ]
