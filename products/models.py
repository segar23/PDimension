from django.db import models
from PIL import Image


class Product(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    image = models.ImageField(default='default.jpg', upload_to='product_images')

    def __str__(self):
        return f'{self.code} : {self.name}'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            width = 300
            height = (width * img.height) / img.width
            output_size = (width, height)
            img.thumbnail(output_size)
            img.save(self.image.path)
