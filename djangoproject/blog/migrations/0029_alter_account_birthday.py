# Generated by Django 4.2.5 on 2023-09-24 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0028_account_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='birthday',
            field=models.DateField(default=None, null=True),
        ),
    ]
