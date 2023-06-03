from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django import forms
from django.contrib.messages import get_messages
from django.contrib import messages
import random
import json
from django.http import JsonResponse
# add categories from database
from .models import Categorie , Product, Profile, Expedition, Payment_method, Order, OrderItem, Shipment, Wishlist

def index(request):
    categories = Categorie.objects.all()
    products = Product.objects.all()
    context = {
        "categories": categories,
        "products": products,
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        quantity = 1

        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        order_item.quantity += quantity
        order_item.save()

        return redirect('cart')
    elif request.method == 'GET':
        product = Product.objects.get(id=product_id)
        context = {
            "product": product,
        }
        return render(request, 'cart.html', context)

@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)

        if product in wishlist.products.all():
            wishlist.products.remove(product)
            messages.error(request, 'Product removed from wishlist.')
        else:
            wishlist.products.add(product)
            messages.success(request, 'Product added to wishlist.')

    return redirect('profile')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = request.POST['email']
            user.email = email
            user.save()
            login(request, user)
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    return render(request, 'register.html', {'form': form})

            return render(request, 'register.html', {'form': form})
    elif request.method == 'GET':
        # Hapus pesan-pesan dari request sebelumnya
        storage = get_messages(request)
        for message in storage:
            pass

        return render(request, 'register.html')


def loginview(request):
    form = UserCreationForm(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html')
    
    elif request.method == 'GET':
        return render(request, 'login.html', )

def logoutview(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('index')
    else:
        return render(request, 'profile.html')

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        user = request.user
        profile = Profile.objects.get(User=request.user)
        username = request.POST['username']
        email = request.POST['email']
        fullname = request.POST['fullname']
        nickname = request.POST['nickname']
        phone = request.POST['phone']
        address = request.POST['address']
        user.username = username
        user.email = email
        profile.fullname = fullname
        profile.nickname = nickname
        profile.phone = phone
        profile.address = address
        
        user.save()
        profile.save()
        return redirect('profile')
    elif request.method == 'GET':
        user = request.user
        try:
            wishlist = Wishlist.objects.get(user=user)
        except Wishlist.DoesNotExist:
            wishlist = None
        context = {
            "wishlist": wishlist.products.all() if wishlist else [],
        }
        return render(request, 'profile.html', context)

    
def edit_image(request):
    if request.method == 'POST':
        if 'profile_image' in request.FILES:
            profile = Profile.objects.get(User=request.user)
            profile.image = request.FILES['profile_image']
            profile.save()
            return redirect('profile')

    return render(request, 'profile.html')

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']

            if user.check_password(old_password):
                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Password changed successfully.')
                    return redirect('profile')
                else:
                    messages.error(request, 'New password confirmation does not match.')
            else:
                messages.error(request, 'Old password is invalid.')
    else:
        form = ChangePasswordForm()

    return render(request, 'profile.html', {'form': form})

@login_required(login_url='login')
def payment(request):
    if request.method == 'GET':
        user = request.user
        expedition = Expedition.objects.all()
        payment_method = Payment_method.objects.all()
        order, created = Order.objects.get_or_create(user=user, complete=False)
        order_items = order.orderitem_set.all()
        order.date_ordered = timezone.now()
        order_number = random.randint(100000, 999999)
        virtual_account = random.randint(100000000000, 999999999999)
        order.order_number = order_number
        order.virtual_account = virtual_account
        order.save()
        
        if not order_items:
            return redirect('cart')

        subtotal = order.get_total_cost
        total_price = order.get_total_payment
        context = {
            "expeditions": expedition,
            "payment_methods": payment_method,
            "order_items": order_items,
            "subtotal": subtotal,
            "order": order,
            "order_number": order_number,
            "virtual_account": virtual_account,
            "total_price": total_price,
        }
        return render(request, 'payment.html', context)
    elif request.method == 'POST':
        user = request.user
        delivery_address = request.POST['delivery_address']
        full_name = request.POST['full_name']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        total_cost = float(request.POST['total_cost'].replace('$', ''))

        expedition_id = request.POST.get('shipping_method')
        expedition = get_object_or_404(Expedition, price=expedition_id)  # Ganti 'id' dengan 'price' jika 'price' adalah kolom yang sesuai dalam model Expedition
        payment_method_id = request.POST.get('payment_method')
        payment_method = get_object_or_404(Payment_method, tax=payment_method_id)

        order, created = Order.objects.get_or_create(user=user, complete=False)
        order.full_name = full_name
        order.email = email
        order.address = address
        order.phone = phone
        order.expedition = expedition
        order.payment_method = payment_method
        order.total_cost = total_cost
        order.delivery_address = delivery_address
        if request.POST['type'] == 'now':
            order.complete = True
        order.save()
        
        

        Shipment.objects.create(
            user=user,
            order=order,
            delivery_address=delivery_address,
        )
        
        return redirect('purchase')


@login_required(login_url='login')
def cart(request):
    user = request.user
    order, created = Order.objects.get_or_create(user=user, complete=False)
    items = order.orderitem_set.all()
    subtotal = order.get_total_cost
    context = {
        'items': items,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'cart.html', context)

def categoryPage(request, category_id):
    category = Categorie.objects.get(id=category_id)
    product = Product.objects.filter(category=category)
    context = {
        "categories": category,
        "products": product,
        }
    return render(request, 'categoryPage.html', context)

def product(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        quantity = int(request.POST.get('quantity', 1))
        
        # Check if an order item with the same product and order already exists
        order_item = OrderItem.objects.filter(order=order, product=product).first()
        if order_item:
            # Order item already exists, update the quantity
            order_item.quantity += quantity
            order_item.save()
        else:
            # Create a new order item
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
            )
        
        return redirect('cart')
    elif request.method == 'GET':
        product = Product.objects.get(id=product_id)
        context = {
            "products": product,
            }
        return render(request, 'product.html', context)


def updateItem(request):
    data = json.loads(request.body)
    itemId = data['productId']
    action = data['action']
    
    user = request.user
    orderItem = OrderItem.objects.get(id=itemId)
    product = orderItem.product
    order, created = Order.objects.get_or_create(user=user, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        orderItem.save()
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        orderItem.save()  
    elif action == 'delete':
        orderItem.delete()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

@login_required(login_url='login')
def purchase(request):
    if request.method == 'GET':
        user = request.user
        orders = Order.objects.filter(user=user, complete=True).order_by('-date_ordered').distinct()
        order_items = []
        for order in orders:
            order_items.append(order.orderitem_set.all())

        shipment = Shipment.objects.filter(order__in=orders)
        payment_methods = orders.values('payment_method__id').distinct()
        expeditions = orders.values('expedition__id').distinct()
        full_name = orders.values('full_name').distinct()
        email = orders.values('email').distinct()
        phone = orders.values('phone').distinct()
        date_ordered = orders.values('date_ordered').distinct()
        
        context = {
            "orders": orders,
            "order_items": order_items,
            "shipment": shipment,
            "payment_methods": payment_methods,
            "expeditions": expeditions,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "date_ordered": date_ordered,
        }
        return render(request, 'purchase.html', context)

def categories(request):
    categories = Categorie.objects.all()
    products = Product.objects.all()
    context = {
        "categories": categories,
        "products": products,
    }
    return render(request, 'categories.html', context)

def all_products(request):
    categories = Categorie.objects.all()
    products = Product.objects.all()
    context = {
        "categories": categories,
        "products": products,
    }
    return render(request, 'all_products.html', context)