# Generated by Django 4.2.16 on 2024-11-11 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "voter_analytics",
            "0002_voter_voter_id_number_alter_voter_apartment_number_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="voter",
            name="voter_id_number",
            field=models.CharField(max_length=20),
        ),
    ]
