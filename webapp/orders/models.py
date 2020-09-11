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



