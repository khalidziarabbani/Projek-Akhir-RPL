from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile_img/', views.edit_image, name='edit_image'),
    path('payment/', views.payment, name='payment'),
    path('cart/', views.cart, name='cart'),
    path('category/<int:category_id>/', views.categoryPage, name='category'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('update_item2/', views.updateItem2, name='update_item2'),
    path('purchase/', views.purchase, name='purchase'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
