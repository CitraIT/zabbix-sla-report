from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from zabbix.models import Customer, ZabbixSLA
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from .forms import LoginForm



@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login")
    else:
        return redirect("/dashboard")


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return redirect(index)
            else:
                return render(request, "core/login.html", context={'form': form, 'error': 'Usuários ou senha inválidos.'})
        else:
            return render(request, "core/login.html", context={'form': form, 'error': 'Usuários ou senha inválidos.'})
    else:
        form = LoginForm()
        return render(request, "core/login.html", context={'form': form})



@login_required
def home(request):
    customer_list = [x for x in Customer.objects.all()]
    return render(request, 'core/home.html', context={'customer_list': customer_list})
    




