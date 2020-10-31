from django.db import models


class Category (models.Model):
    name = models.CharField(max_length=250, unique=True)
    isMacro = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product (models.Model):
    picture = models.ImageField(default='default.jpg', upload_to='product_pics')
    name = models.CharField(max_length=250)
    sku = models.IntegerField(unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    description = models.TextField(blank=True)
    isReference = models.BooleanField(default=True)
    macroCategories = models.ManyToManyField(Category, related_name='macroProduct', limit_choices_to={'isMacro': True})
    subCategories = models.ManyToManyField(Category, related_name='subProduct', limit_choices_to={'isMacro': False})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['sku']


class ProductVariant(models.Model):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductSearchTag (models.Model):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
