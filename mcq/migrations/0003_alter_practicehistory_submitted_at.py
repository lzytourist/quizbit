# Generated by Django 5.1.3 on 2024-11-20 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcq', '0002_practicehistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practicehistory',
            name='submitted_at',
            field=models.DateTimeField(null=True),
        ),
    ]