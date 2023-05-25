from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
# add categories from database
from .models import Categorie , Product, Profile, Expedition, Payment_method, Order, OrderItem

def index(request):
    categorie = Categorie.objects.all()
    product = Product.objects.all()
    context = {
        "categories": categorie,
        "products": product,
        }
    return render(request, 'index.html', context)

from django.contrib import messages

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
            # Tambahkan pesan kesalahan ke dalam alert
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}", extra_tags='alert-danger')

            return render(request, 'register.html', {'form': form})
    elif request.method == 'GET':
        return render(request, 'register.html')


def loginview(request):
    form = UserCreationForm(request.POST)
    # if request.user.is_authenticated:
    #     return redirect('index')
    
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
    else:
        return render(request, 'profile.html')

    
def edit_image(request):
    if request.method == 'POST':
        if 'profile_image' in request.FILES:
            profile = Profile.objects.get(User=request.user)
            profile.image = request.FILES['profile_image']
            profile.save()
            return redirect('profile')

    return render(request, 'profile.html')

@login_required(login_url='login')
def payment(request):
    if request.method == 'GET':
        expedition = Expedition.objects.all()
        payment_method = Payment_method.objects.all()
        context = {
            "expeditions": expedition,
            "payment_methods": payment_method,
            }
        return render(request, 'payment.html', context)
    elif request.method == 'POST':
        user = request.user
        full_name = request.POST['full_name']
        phone = request.POST['phone']
        address = request.POST['address']
        email = request.POST['email']
        city = request.POST['city']
        province = request.POST['province']
        zipcode = request.POST['zipcode']   
        
        payment_method = request.POST.get('payment_method')
        
        category_id = request.POST.get('category_id')
        
        

@login_required(login_url='login')
def cart(request):
    user = request.user
    order, created = Order.objects.get_or_create(user=user, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_total_items    
    context = {'items': items, 'order': order, 'cartItems': cartItems}

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
        
        return redirect('product', product_id=product.id)
    elif request.method == 'GET':
        product = Product.objects.get(id=product_id)
        context = {
            "products": product,
            }
        return render(request, 'product.html', context)


def updateItem2(request):
    data = json.loads(request.body)
    itemId = data['productId']
    action = data['action']

    print('Action:', action)
    print('itemId:', itemId)

    user = request.user
    orderItem = OrderItem.objects.get(id=itemId)

    product = orderItem.product
    order, created = Order.objects.get_or_create(user=user, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        # messages.success(request, f'Item was successfully added')
        orderItem.save()
        # Render message item suces fully added
        # return JsonResponse({'success': 'Item was added'}, status=200)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        orderItem.save()
        
    elif action == 'delete_this_item':
        orderItem.delete()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
