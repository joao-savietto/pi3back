# Generated by Django 5.2 on 2025-05-09 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_selectionprocess_options_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
