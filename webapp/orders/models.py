from decimal import Decimal

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
    products = models.ManyToManyField(OrderItem)
    isBusinessUser = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    enterprise = models.CharField(max_length=100, null=True)
    verification_digit = models.IntegerField(null=True)
    person_id = models.IntegerField()
    address = models.CharField(max_length=100)
    needsEReceipt = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    isFinalized = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    total = models.DecimalField(decimal_places=2, max_digits=14, default=Decimal(0))
    shipping = models.DecimalField(decimal_places=2, max_digits=7, default=Decimal(4500))

    class CityChoices(models.TextChoices):
        MEDELLIN = 'MDE', 'Medellín'
        ENVIGADO = 'ENV', 'Envigado'
        SABANETA = 'SBT', 'Sabaneta'
        ITAGUI = 'ITG', 'Itagüí'
        ESTRELLA = 'EST', 'La Estrella'
        BELLO = 'BLO', 'Bello'
        GIRARDOTA = 'GIR', 'Girardota'
        COPACABANA = 'COP', 'Copacabana'
        CALDAS = 'CAL', 'Caldas'

    city = models.CharField(max_length=100, choices=CityChoices.choices, default=CityChoices.MEDELLIN)

    class PaymentMethod(models.TextChoices):
        CASH = 'EFECTIVO', 'Pago contra entrega en efectivo'
        TRANSFER = 'TRANSFERENCIA', 'Transferencia cuando llegue el pedido'
        QR = 'QR', 'Código QR al mensajero'

    payment = models.CharField(max_length=140, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    comments = models.TextField()

    class OrderStatus(models.TextChoices):
        UNREAD = 'Sin Leer', 'Sin Leer'
        OPEN = 'Abierta', 'Abierta'
        FACTURADA = 'Facturada', 'Facturada'
        CLOSED = 'Cerrada', 'Cerrada'

    status = models.CharField(max_length=140, choices=OrderStatus.choices, default=OrderStatus.UNREAD)

    def adjust_shipping(self):
        if self.city in (self.CityChoices.GIRARDOTA, self.CityChoices.COPACABANA, self.CityChoices.CALDAS):
            if self.total > 100000:
                self.shipping = Decimal(0)
            else:
                self.shipping = Decimal(6000)
        elif self.total > 60000:
            self.shipping = Decimal(0)
        else:
            self.shipping = Decimal(4500)

    def get_total_order(self):
        self.total = 0
        for product in self.products.all():
            self.total += product.get_sub_total()
        self.adjust_shipping()
        return self.total
