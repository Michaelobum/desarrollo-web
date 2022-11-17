from django.db.models import Sum, Count, Avg
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from appman.models import *
from django.contrib.auth.decorators import login_required



def menuinicial(request):
    data = {
        'ruta': '/',
        'empresa': 'Michael',
        'nombre': 'Inicio',
        'totalmed': medioPago.objects.all().count()
    }

    return render(request, 'menu.html', data)
