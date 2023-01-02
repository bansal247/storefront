# Generated by Django 4.1.5 on 2023-01-02 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "store",
            "0002_rename_store_custo_last_na_e6a359_idx_store_custo_last_na_2e448d_idx_and_more",
        ),
    ]

    operations = [
        migrations.RunSQL("""
            INSERT INTO store_collection (title)
            VALUES ('collection1')""",
            """
            DELETE FROM store_collection
            WHERE title = 'collection1'
        """)
    ]