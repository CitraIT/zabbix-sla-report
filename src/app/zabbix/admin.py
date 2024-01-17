from django.contrib import admin
from .models import ZabbixSLA, Customer

# Register your models here.
admin.site.register(ZabbixSLA)
admin.site.register(Customer)

