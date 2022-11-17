from django.contrib import messages
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from appman.forms import MedioPagoForm
from appman.models import medioPago
from django.contrib.auth.decorators import login_required





def viewmediopago(request):
    data = {'empresa': 'Michael', 'nombre': 'Medio Pago', 'ruta': '/mediopago/'}
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'agregar':
                with transaction.atomic():
                    try:
                        if medioPago.objects.filter(codigo=request.POST['codigo']).exists():
                            messages.error('El codigo ya existe')
                            return redirect('mediopago/?action=agregar')
                        else:
                            form = MedioPagoForm(request.POST)
                            if form.is_valid():
                                form.save()
                                messages.success(request, 'Éxito al guardar!!!!!!')
                    except Exception as ex:
                        messages.error(request, ex)
            elif action == 'editar':
                with transaction.atomic():
                    try:
                        id = request.POST['id']
                        mediopago = medioPago.objects.get(id=id)
                        form = MedioPagoForm(request.POST, instance=mediopago)
                        if form.is_valid:
                            form.save()
                            messages.success(request, 'nuestro registro se guardó correctamente')
                    except Exception as ex:
                        messages.error(request, ex)
            elif action == 'eliminar':
                with transaction.atomic():
                    try:
                        id = request.GET['id']
                        mediopago = medioPago.objects.get(id=id)
                        mediopago.status = False
                        mediopago.save()
                        messages.success(request, 'Eliminado correctamente')
                    except Exception as ex:
                        messages.error(request, ex)

            elif action == 'pdflistado':
                with transaction.atomic():
                    try:
                        data['id'] = medioPago.objects.get(request.GET['id'])
                        template = get_template('pdf/mediopago/listadopago.html')
                        return JsonResponse({'data': template.render(data)})
                    except Exception as ex:
                        messages.error(request, ex)

    else:
        if 'action' in request.GET:
            data['action'] = action = request.GET['action']

            if action == 'agregar':
                form = MedioPagoForm()
                data['formulario'] = form
                return render(request, 'mediopago/formulario.html', data)

            elif action == 'editar':
                try:
                    data['id'] = id = request.GET['id']
                    mediopago = medioPago.objects.get(id=id)
                    form = MedioPagoForm(initial=model_to_dict(mediopago))
                    data['formulario'] = form
                    return render(request, 'medioPago/formulario.html', data)
                except Exception as ex:
                    messages.error(request, ex)
                    return render(request, ex)

            elif action == 'consultar':
                try:
                    resultado = True
                    data['id'] = id = request.GET['id']
                    data['mediopago'] = mediopago = medioPago.objects.get(id=id)
                    template = get_template('medioPago/listadoajax.html')
                    return JsonResponse({'result': resultado, 'data': template.render(data)})
                except Exception as ex:
                    resultado = False
                    mensaje = ex
                    return JsonResponse({'result': resultado, 'mensaje': mensaje})

            elif action == 'pdflistado':
                data['listado'] = medioPago.objects.filter(status=True).order_by('descripcion')
                return render(request, 'pdf/mediopago/listadopago.html', data)

            elif action == 'eliminar':
                data['id'] = id = request.GET['id']
                data['mediopago'] = medioPago.objects.filter(id=id)
                return render(request, 'medioPago/eliminar.html', data)

            return redirect('/mediopago/')

    try:
        data['listado'] = medioPago.objects.filter(status=True).order_by('codigo')
    except Exception as ex:
        print(ex)
    return render(request, 'mediopago/listado.html', data)
