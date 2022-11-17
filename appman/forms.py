from django import forms
from appman.models import Producto, Marca, medioPago


class MedioPagoForm(forms.ModelForm):
    class Meta:
        model = medioPago
        fields = ['codigo', 'descripcion']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control',
                                             "placeholder": 'Ingrese Codigo'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control',
                                                  "placeholder": 'Ingrese Descripción'}),
        }
        labels = {'codigo': 'Codigo', 'descripcion': 'Descripción'}


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['descripcion', 'mediopago']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control',
                                                  "placeholder": 'Ingresa la descripcion'}),
            'mediopago': forms.SelectMultiple(attrs={'class': 'form_control select2'}),
        }
        labels = {'descripcion': 'Descripcion', 'mediopago': 'Medios de Pago'}


class ProductForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'precio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {'nombre': 'Nombre', 'marca': 'Marca', 'precio': 'Precios'}
