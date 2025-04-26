from django.db import models

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Product categories"

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
