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
    path('updateItem/', views.updateItem, name='updateItem'),
    path('purchase/', views.purchase, name='purchase'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('categories/', views.categories, name='categories'),
    path('all_products/', views.all_products, name='all_products'),
    path('change_password/', views.change_password, name='change_password'),
]
