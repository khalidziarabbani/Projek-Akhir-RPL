from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
# add categories from database
from .models import Categorie , Product, Profile, Expedition, Payment_method

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
    expedition = Expedition.objects.all()
    payment_method = Payment_method.objects.all()
    context = {
        "expeditions": expedition,
        "payment_methods": payment_method,
        }
    return render(request, 'payment.html', context)

@login_required(login_url='login')
def cart(request):
    return render(request, 'cart.html')

def categoryPage(request, category_id):
    category = Categorie.objects.get(id=category_id)
    product = Product.objects.filter(category=category)
    context = {
        "categories": category,
        "products": product,
        }
    return render(request, 'categoryPage.html', context)

def product(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        "products": product,
        }
    return render(request, 'product.html', context)
