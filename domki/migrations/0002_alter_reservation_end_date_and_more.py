# Generated by Django 5.1.1 on 2024-09-21 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("domki", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="end_date",
            field=models.DateField(verbose_name="Koniec rezerwacji"),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="start_date",
            field=models.DateField(verbose_name="Poczatek rezerwacji"),
        ),
    ]
