# Generated by Django 5.0.3 on 2024-05-13 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minor', '0004_rename_categories_categorie_product_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categorie',
            new_name='Categories',
        ),
    ]
