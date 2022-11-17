from django.contrib import messages
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from appman.forms import ProductForm
from appman.models import Producto
from django.contrib.auth.decorators import login_required




def viewproducto(request):
    data = {'empresa': 'Michael', 'nombre': 'Producto', 'ruta': '/Producto/'}

    if request.method == 'POST':

        if 'action' in request.POST:
            data['action'] = action = request.POST['action']

            if action == 'agregar':
                with transaction.atomic():
                    try:
                        if Producto.objects.filter(nombre=request.POST['nombre']).exists():
                            messages.error(request, 'El nombre está repetido')
                            return redirect('/Producto/?action=agregar')
                        else:
                            form = ProductForm(request.POST)
                            if form.is_valid():
                                producto = Producto(nombre=form.cleaned_data['nombre'],
                                                    marca=form.cleaned_data['marca'],
                                                    precio=form.cleaned_data['precio'])
                                producto.save(request)
                                messages.success(
                                    request, 'Registro Guardado Correctamente chingadamadre')
                    except Exception as ex:
                        messages.error(request, ex)

            elif action == 'editar':
                with transaction.atomic():
                    try:
                        id = request.POST['id']
                        producto = Producto.objects.get(id=id)
                        form = ProductForm(request.POST, instance=producto)
                        if form.is_valid():
                            form.save()
                            messages.success(request, 'Registro guardado exitosamente chingadamadre!')
                    except Exception as ex:
                        messages.error(request, ex)

            elif action == 'eliminar':
                with transaction.atomic():
                    try:
                        id = request.POST['id']
                        producto = Producto.objects.get(id=id)
                        producto.status = False
                        producto.save()
                        messages.success(request, 'registro eliminado')
                    except Exception as ex:
                        messages.error(request, ex)

            elif action == 'pdflistado':
                try:
                    data['action'] = Producto.objects.get(id=request.GET['id'])
                    template = get_template("pdf/producto/listadoP.html")
                    return JsonResponse({'data': template.render(data)})
                except Exception as ex:
                    messages.error(request, ex)
            return redirect(request.path)

    else:
        if 'action' in request.GET:
            data['action'] = action = request.GET['action']

            if action == 'agregar':
                form = ProductForm
                data['formulario'] = form
                return render(request, 'producto/formulario.html', data)

            elif action == 'editar':
                try:
                    data['id'] = id = request.GET['id']
                    producto = Producto.objects.get(id=id)
                    form = ProductForm(initial=model_to_dict(producto))
                    data['formulario'] = form
                    return render(request, 'producto/formulario.html', data)
                except Exception as ex:
                    messages.error(request, ex)
                    return redirect('/Producto/')

            elif action == 'eliminar':
                try:
                    data['id'] = id = request.GET['id']
                    data['producto'] = producto = Producto.objects.get(id=id)
                    return render(request, 'producto/eliminar.html', data)
                except Exception as ex:
                    messages.error(request, ex)
                    return redirect(request, '/Producto/')

            elif action == 'pdflistado':
                data['listado'] = Producto.objects.filter(status=True).order_by('nombre')
                return render(request, 'pdf/producto/listadoP.html', data)

            elif action == 'consultar':
                try:
                    resultado = True
                    data['id'] = id = request.GET['id']
                    data['producto'] = producto = Producto.objects.get(id=id)
                    template = get_template('producto/listadoajax.html')
                    return JsonResponse({"result": resultado, 'data': template.render(data)})

                except Exception as ex:
                    resultado = False
                    mensaje = ex
                    return JsonResponse({"result": resultado, 'mensaje': mensaje})

            return redirect('/Producto/')

    try:
        data['listado'] = Producto.objects.filter(status=True).order_by(
            'nombre', 'marca', 'precio')
    except Exception as ex:
        print(ex)
    return render(request, 'producto/listado.html', data)
