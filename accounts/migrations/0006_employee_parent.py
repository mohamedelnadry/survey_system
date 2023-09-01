# Generated by Django 4.2.4 on 2023-08-30 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_employee_job_title_delete_jobtitle'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='accounts.employee'),
        ),
    ]
