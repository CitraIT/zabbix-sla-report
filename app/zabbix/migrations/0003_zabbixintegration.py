# Generated by Django 5.0.1 on 2024-01-14 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zabbix', '0002_customer_zabbixsla_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZabbixIntegration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_url', models.CharField(max_length=120)),
                ('zabbix_auth_token', models.CharField(max_length=64)),
            ],
        ),
    ]
