from django.shortcuts import render
from django.http import request, response, HttpRequest, HttpResponse, HttpResponseRedirect
from zabbix.models import Customer, ZabbixSLA
import requests
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import ZabbixIntegration
from .forms import ZabbixIntegrationForm, CustomerForm, ZabbixSLAForm

# Create your views here.


#
@login_required
def integracao_zabbix(request):
    if ZabbixIntegration.objects.all().count() == 0:
        zabbix_integration = ZabbixIntegration(api_url="https://zabbix.exemplo.com.br/api_jsonrpc.php", zabbix_auth_token="abc123!@#")
    else:
        zabbix_integration = ZabbixIntegration.objects.first()
    
    if request.method == "POST":
        form = ZabbixIntegrationForm(request.POST, instance=zabbix_integration)
        if form.is_valid():
            form.save()
    else:
        form = ZabbixIntegrationForm(instance=zabbix_integration)

    form.fields['zabbix_auth_token'].widget.input_type = "password"
    return render(request, 'zabbix/preferencias_zabbix.html', context={'form': form})



# ---- CLIENTES VIEWS  
@login_required
def clientes(request):
    if request.method == 'GET':
        clientes = Customer.objects.all()
        return render(request, 'zabbix/clientes.html', context={'clientes': clientes})
    elif request.method == 'POST':
        return HttpResponse('clientes view form sent')

# Clientes_add
@login_required
def clientes_add(request):
    submitted = False
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return HttpResponseRedirect(f'/zabbix/clientes/')
    else:
        form = CustomerForm()
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request, 'zabbix/clientes_add.html', context={'form':form, 'submitted':submitted})
        



# Clientes_edit
@login_required
def clientes_edit(request, id):
    if request.method == "GET":
        cliente = Customer.objects.get(id=id)
        form = CustomerForm(instance=cliente)
        return render(request, "zabbix/clientes_edit.html", {'form': form, 'cliente': cliente})
    elif request.method == "POST":
        cliente = Customer.objects.get(id=id)
        form = CustomerForm(request.POST, instance=cliente)
        submitted = False
        if form.is_valid():
            form.save()
            submitted = True
            return render(request, "zabbix/clientes_edit.html", {'form': form, 'submitted': submitted, 'cliente': cliente })
        else:
            return render(request, "zabbix/clientes_edit.html", {'form': form})
        



# Clientes_delete
@login_required
def clientes_delete(request, id):
    cliente = Customer.objects.get(id=id)
    cliente.delete()
    return render(request, "zabbix/clientes_delete.html", {'cliente': cliente, 'submitted': True})



# ---- SLAS VIEWS  
@login_required
def slas(request):
    if request.method == 'GET':
        slas = ZabbixSLA.objects.all()
        return render(request, 'zabbix/slas.html', context={'slas': slas})
    elif request.method == 'POST':
        return HttpResponse('slas view form sent')


# slas_add
@login_required
def slas_add(request):
    submitted = False
    if request.method == "POST":
        form = ZabbixSLAForm(request.POST)
        if form.is_valid():
            sla = form.save()
            return HttpResponseRedirect(f'/zabbix/slas/')
    else:
        form = ZabbixSLAForm()
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request, 'zabbix/slas_add.html', context={'form':form, 'submitted':submitted})
        



# slas_edit
@login_required
def slas_edit(request, id):
    if request.method == "GET":
        sla = ZabbixSLA.objects.get(id=id)
        form = ZabbixSLAForm(instance=sla)
        return render(request, "zabbix/slas_edit.html", {'form': form, 'slas': sla})
    elif request.method == "POST":
        sla = ZabbixSLA.objects.get(id=id)
        form = ZabbixSLAForm(request.POST, instance=sla)
        submitted = False
        if form.is_valid():
            form.save()
            submitted = True
            return render(request, "zabbix/slas_edit.html", {'form': form, 'submitted': submitted, 'sla': sla })
        else:
            return render(request, "zabbix/slas_edit.html", {'form': form})
        



# slas_delete
@login_required
def slas_delete(request, id):
    sla = ZabbixSLA.objects.get(id=id)
    sla.delete()
    return render(request, "zabbix/slas_delete.html", {'sla': sla, 'submitted': True})
    



# View: report1
@login_required
def report1(request):

    if request.method == 'POST':
        data_inicio = datetime.fromisoformat(request.POST['data_inicio'])
        data_fim    = datetime.fromisoformat(request.POST['data_fim'])
        cliente_id  = request.POST['customer_id']

        cliente = Customer.objects.get(id=cliente_id)
        customer_filter_slaname = [ x.name for x in cliente.zabbixsla_set.iterator()]

        zabbix = ZabbixIntegration.objects.first()

        
        #url = 'https://zabbix.citrait.com.br/api_jsonrpc.php'
        headers = {'Content-Type': 'application/json-rpc', 'Authorization': f'Bearer {zabbix.zabbix_auth_token}'}
        data = {
            "jsonrpc": "2.0",
            "method": "sla.get",
            "params": {
                "filter": {
                    'name': customer_filter_slaname
                },
                "selectServiceTags": ["tag","operator","value"]
            },
            "id": 1
        }
        r = requests.post(zabbix.api_url, headers=headers, json=data)
        sla_list = r.json()['result']


        # adiciona cabeçalho
        report_data = "['Mês'"
        for i in sla_list:
            #report_data += f"""{'i["name"]}'"""
            report_data += ",'{}'".format(i['name'])
        report_data += "],"


        sli_list = {}
        for sla in sla_list:
            data = {
                "jsonrpc": "2.0",
                "method": "sla.getsli",
                "params": {
                    "slaid": sla['slaid'],
                    "period_from": int(data_inicio.timestamp()),
                    "period_to": int(data_fim.timestamp())
                },
                "id": 1
            }

            r = requests.post(zabbix.api_url, headers=headers, json=data)
            sli_json = r.json()['result']
            sli_list[sla['name']] = []
            for sli_index in range(len(sli_json['sli'])):
                sli_list[sla['name']].append({
                    'month': sli_json['periods'][sli_index]['period_from'],
                    'sli':   sli_json['sli'][sli_index][0]['sli']
                })


        # Percorre os dados de sla/sli e controi a matriz para ser usada no google charts.
        matrix_depth = len(sli_list[sla_list[0]['name']])
        matrix_data = []
        for depth in range(matrix_depth):
            tmp = []
            isFirst = True
            for sla in sla_list:
                sla_name = sla['name']
                if isFirst:
                    time_stamp = sli_list[sla_name][depth]['month']
                    month = month_translate( datetime.fromtimestamp(time_stamp).month )
                    tmp.append(month)
                    isFirst = False
                tmp.append(int(sli_list[sla_name][depth]['sli']))
            matrix_data.append(tmp)
        return render(request, 'zabbix/sla_period_report.html', context={'sla_list': sla_list, 'matrix_data': matrix_data, 'cliente': cliente})   
    else: 
        customer_list = Customer.objects.all()
        return render(request, 'zabbix/form_report1.html', context={'customer_list': customer_list})   


    
def month_translate(month):
    months = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }
    return months[month]

    
