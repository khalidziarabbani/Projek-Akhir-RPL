from django.contrib import admin

from .models import Categorie, Product, Profile, Expedition, Payment_method, Order, OrderItem, Shipment
admin.site.register(Categorie)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Expedition)
admin.site.register(Payment_method)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Shipment)