# Generated by Django 5.1.7 on 2025-04-21 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_agency_intro_agency_overview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberexperience',
            name='enddate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
