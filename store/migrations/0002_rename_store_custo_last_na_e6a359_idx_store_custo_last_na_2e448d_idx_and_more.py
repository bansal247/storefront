# Generated by Django 4.1.4 on 2023-01-02 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_customer_store_custo_last_na_e6a359_idx_and_more"),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="customer",
            new_name="store_custo_last_na_2e448d_idx",
            old_name="store_custo_last_na_e6a359_idx",
        ),
        migrations.AlterModelTable(
            name="customer",
            table=None,
        ),
    ]
