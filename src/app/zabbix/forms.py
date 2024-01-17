from django import forms
from .models import ZabbixIntegration, Customer, ZabbixSLA


# Integration Form
class ZabbixIntegrationForm(forms.ModelForm):
    pass
    class Meta:
        model = ZabbixIntegration
        fields = '__all__'
        


# Customer Form
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class ZabbixSLAForm(forms.ModelForm):
    class Meta:
        model = ZabbixSLA
        fields = '__all__'


