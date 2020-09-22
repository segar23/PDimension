from django.db import models
from django.contrib.auth.models import User
from control_panel.models import Product


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_sub_total(self):
        return self.product.price * self.quantity


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderItem)

    def get_total(self):
        total = 0
        for oder_item in self.products.all():
            total += oder_item.get_sub_total()
        return total

    def clear_cart(self):
        return self.products.clear()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isBusinessUser = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    enterprise = models.CharField(max_length=100, null=True)
    verification_digit = models.IntegerField(max_length=1, null=True)
    person_id = models.IntegerField(max_length=12)
    address = models.CharField(max_length=100)
    needsEReceipt = models.BooleanField(default=False)

    class City(models.TextChoices):
        MEDELLIN = 'Medellín'
        ENVIGADO = 'Envigado'
        SABANETA = 'Sabaneta'
        ITAGUI = 'Itagüí'
        BELLO = 'Bello'
        ESTRELLA = 'La Estrella'

    city = models.CharField(max_length=100, choices=City.choices)

    class PaymentMethod(models.TextChoices):
        CASH = 'Pago contra entrega en efectivo'
        TRANSFER = 'Transferencia cuando llegue el pedido'
        QR = 'Código QR al mensajero'

    payment = models.CharField(choices=PaymentMethod.choices)
    comments = models.TextField
