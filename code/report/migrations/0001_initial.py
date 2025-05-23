# Generated by Django 5.2.1 on 2025-05-18 20:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField()),
                ('freshdesk_info', models.JSONField(blank=True, null=True, verbose_name='Freshdesk info: Item 5.1')),
                ('checkpoint_info', models.JSONField(blank=True, null=True, verbose_name='Checkpoint info: Item 7.1')),
                ('harmony_info', models.JSONField(blank=True, null=True, verbose_name='Harmony: Item 8.2')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.customer')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
