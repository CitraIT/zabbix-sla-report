from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField('customer',max_length=100)

    def __str__(self) -> str:
        return self.name


class ZabbixSLA(models.Model):
    name = models.CharField('name', max_length=100)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.name


class ZabbixIntegration(models.Model):
    api_url = models.CharField(max_length=120)
    zabbix_auth_token = models.CharField(max_length=64)
