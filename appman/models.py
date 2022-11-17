from django.db import models

# Create your models here.


class ModeloBase(models.Model):
    fecha_registro = models.DateField(
        verbose_name="Fecha Registro", auto_now_add=True)
    hora_registro = models.TimeField(
        verbose_name="Hora Registro", auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True


class medioPago(ModeloBase):
    codigo = models.CharField(null=True, blank=True, max_length=200)
    descripcion = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.codigo


class Marca(ModeloBase):
    descripcion = models.CharField(null=True, blank=True, max_length=10)
    mediopago = models.ManyToManyField(
        medioPago, verbose_name=u'medios de pago')

    def __str__(self):
        return self.descripcion


class Producto(ModeloBase):
    nombre = models.CharField(null=True, blank=True, max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    precio = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre
