# Generated by Django 5.0.3 on 2024-07-10 08:59

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minor', '0007_rename_text_login_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.IntegerField()),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minor.login')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minor.product')),
            ],
        ),
    ]
