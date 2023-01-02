# Generated by Django 4.1.4 on 2023-01-02 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "add_slug_to_product"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="customer",
            index=models.Index(
                fields=["last_name", "first_name"],
                name="store_custo_last_na_e6a359_idx",
            ),
        ),
        migrations.AlterModelTable(
            name="customer",
            table="store_customers",
        ),
    ]
