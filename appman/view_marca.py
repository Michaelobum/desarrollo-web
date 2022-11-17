from django.contrib import messages
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from appman.forms import MarcaForm
from appman.models import Marca
from django.contrib.auth.decorators import login_required


def viewmarca(request):
    data = {'empresa': 'Michael', 'nombre': 'Marca', 'ruta': '/Marca/'}

    if request.method == 'POST':

        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'agregar':
                with transaction.atomic():
                    try:
                        if Marca.objects.filter(descripcion=request.POST['descripcion']).exists():
                            messages.error(request, 'Registro ya existe')
                            return redirect('{}?action=agregar'.format(request.path))

                        else:
                            form = MarcaForm(request.POST)
                            try:
                                if form.is_valid():
                                    marca = Marca(descripcion=form.cleaned_data['descripcion'])
                                    marca.save()
                                    marca.mediopago.set(form.cleaned_data['mediopago'])
                                    marca.save()
                                    messages.success(
                                        request, 'Registro Guardado Correctamente')
                            except Exception as ex:
                                messages.error(request, ex)
                    except Exception as ex:
                        messages.error(request, ex)

            elif action == 'editar':
                with transaction.atomic():
                    try:
                        id = request.POST['id']
                        marca = Marca.objects.get(id=id)
                        form = MarcaForm(request.POST, instance=marca)
                        if form.is_valid():
                            form.save()
                            messages.success(request, 'El registro se editó correctamente')
                        else:
                            messages.error(request, 'error')
                    except Exception as ex:
                        messages.error(request, ex)

            elif action == 'pdflistado':
                with transaction.atomic():
                    try:
                        data['pdf'] = Marca.objects.get(id=request.GET['id'])
                        template = get_template('pdf/marca/listadoM.html')
                        return JsonResponse({'data': template.render(data)})
                    except Exception as ex:
                        mensaje = ex
                        return JsonResponse({"mensaje": mensaje})

            elif action == 'eliminar':
                with transaction.atomic():
                    try:
                        data['id'] = id = request.GET['id']
                        data['marca'] = marca = Marca.objects.get(id=id)
                        marca.status = False
                        marca.save()
                        messages.success(request, 'se eliminó correctamnete')
                    except Exception as ex:
                        messages.error(request, ex)

            return redirect(request.path)

    else:
        if 'action' in request.GET:
            data['action'] = action = request.GET['action']

            if action == 'agregar':
                form = MarcaForm()
                data['formulario'] = form
                return render(request, 'marca/formulario.html', data)

            elif action == 'editar':
                data['id'] = id = request.GET['id']
                marca = Marca.objects.get(id=id)
                form = MarcaForm(initial=model_to_dict(marca))
                data['formulario'] = form
                return render(request, 'marca/formulario.html', data)

            elif action == 'eliminar':
                data['id'] = id = request.GET['id']
                data['marca'] = marca = Marca.objects.get(id=id)
                return render(request, 'marca/eliminar.html', data)

            elif action == 'pdflistado':
                data['listado'] = Marca.objects.filter(status=True).order_by('descripcion')
                return render(request, 'pdf/marca/listadoM.html', data)

            elif action == 'consultar':
                try:
                    resultado = True
                    data['marca'] = marca = Marca.objects.get(id=request.GET['id'])
                    template = get_template('marca/listadoajax.html')
                    return JsonResponse({'result': resultado, 'data': template.render(data)})
                except Exception as ex:
                    resultado = False
                    mensaje = ex
                    return JsonResponse({'result': resultado, 'mensaje': mensaje})

            return redirect('/Marca/')
    try:
        data['listado'] = Marca.objects.filter(status=True).order_by('descripcion', 'mediopago')
    except Exception as ex:
        print(ex)
    return render(request, 'marca/listado.html', data)
