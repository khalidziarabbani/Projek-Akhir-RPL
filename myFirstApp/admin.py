from django.contrib import admin

from .models import Categorie, Product, Profile
admin.site.register(Categorie)
admin.site.register(Product)
admin.site.register(Profile)