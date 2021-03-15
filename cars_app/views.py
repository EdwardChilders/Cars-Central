from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
import bcrypt
from django.core.files.storage import FileSystemStorage


# renders

def index(request):
    return render(request, 'login.html')

def new_user(request):
    return render(request, 'registration.html')

def homepage(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['uuid']),
        'cars': Car.objects.all(),
        'parts': Part.objects.all()
    }
    return render(request, 'homepage.html', context)


def cars(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['uuid']),
        'cars': Car.objects.all()
    }
    return render(request, "cars.html", context)


def sell_car(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['uuid']),
        'cars': Car.objects.all()
    }
    return render(request, "sell_car.html", context)


def edit_car(request, c_id):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['uuid']),
        'car': Car.objects.get(id=c_id)
    }
    return render(request, 'edit_car.html', context)

# redirects
# CHANGE REDIRECT ROUTE. IT SHOULD NOT BE BOOKS

def register(request):
    print(request.POST)
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hash_browns = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(hash_browns)
        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hash_browns
        )
        print(user)
        # redirect to a success route
        request.session['uuid'] = user.id
        return redirect('/homepage')


def login(request):
    print(request.POST)
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        print(user)
        # redirect to a success route
        request.session['uuid'] = user.id
        return redirect('/homepage')


def logout(request):
    request.session.flush()
    return redirect('/')


def post_car(request):
    print(request.POST)
    errors = User.objects.car_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/sell_car')
    else:
        Car.objects.create(
            title=request.POST['title'],
            desc=request.POST['desc'],
            make=request.POST['make'],
            model=request.POST['model'],
            year=request.POST['year'],
            mileage=request.POST['mileage'],
            salvage=request.POST['salvage'],
            user_id=User.objects.get(id=request.session['uuid']),
            price=request.POST['price'],
            img=request.FILES['image']
        )
    return redirect("/cars")


def update_car(request, c_id):
    print(request.POST)
    errors = User.objects.car_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/sell_car')
    else:
        c = Car.objects.get(id=c_id)
        c.title=request.POST['title']
        c.desc=request.POST['desc']
        c.make=request.POST['make']
        c.model=request.POST['model']
        c.year=request.POST['year']
        c.mileage=request.POST['mileage']
        c.salvage=request.POST['salvage']
        c.price=request.POST['price']
        c.save()
    return redirect("/cars")


def destroy_car(request, c_id):
    c = Car.objects.get(id=c_id)
    c.delete()
    return redirect('/cars')


def message_car_owner(request, c_id):
    user=request.session['uuid']
    car=Car.objects.get(id=c_id)
    car.message.add(user)
    messages.success(request, 'Successfully Sent The Message! They have been notified of your interest and we sent them your email so they can message you!')
    return redirect('/cars')
