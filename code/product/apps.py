from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'


class ProductcategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'productcategory'
