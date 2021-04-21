from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decoraters import unauthenticated_user, allowed_users
from django.contrib import messages
from .models import *
from .forms import CreateUserForm


@unauthenticated_user
def sign_in(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        password1 = request.POST.get('password')
        user = authenticate(username=user, password=password1)
        if user is not None:
            try:
                account = Account.objects.get(username=user)
                login(request, user)
                return redirect('index')
            except Account.DoesNotExist:
                messages.error(request, 'UserName or Password is incorrect!')
                return redirect('Signin')
        else:
            messages.error(request, 'UserName or Password is incorrect!')
            return redirect('Signin')
    params = {}
    return render(request, 'fund/Sign_in.html', params)
    context={}
    return render(request, 'fund/Sign_in.html', context)


@unauthenticated_user
def sign_up(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            fullname = form.cleaned_data.get('fullname')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            new_user = form.save()

            group = Group.objects.get(name='Account')
            new_user.groups.add(group)
            account = Account()
            account.username = User.objects.get(username=username)
            account.email = email
            account.fullname = fullname
            account.phone = phone
            account.save()

            messages.success(request, 'Account has been created for ' + username)
            return redirect('Signin')
    params = {
        'form': form
    }
    return render(request, 'fund/Sign_up.html', params)


@unauthenticated_user
def admin_sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        user = authenticate(username=username, password=password1)
        if user is not None:
            try:
                admin = Admin.objects.get(admin_username=user)
                login(request, user)
                return redirect('Admin')
            except Admin.DoesNotExist:
                messages.error(request, 'You are not an Admin')
                return redirect('AdminSignin')
        else:
            messages.error(request, 'UserName or Password is incorrect!')
            return redirect('AdminSignin')
    params = {}
    return render(request, 'fund/admin_sign_in.html', params)


@login_required(login_url='Signin')
def sign_out(request):
    logout(request)
    return redirect('Signin')


@login_required(login_url='AdminSignin')
def admin_sign_out(request):
    logout(request)
    return redirect('AdminSignin')


@login_required(login_url='Signin')
def access_denied(request):
    return render(request, 'fund/access-deny.html')


def index(request):
    context={}
    return render(request, 'fund/index.html', context)

def about(request):
    context={}
    return render(request, 'fund/about.html', context)

def contact(request):
    context={}
    return render(request, 'fund/contact.html', context)

@login_required(login_url='Signin')
@allowed_users(allowed_roles=['Account'])
def causes(request):
    context={}
    return render(request, 'fund/causes.html', context)

@login_required(login_url='Signin')
@allowed_users(allowed_roles=['Account'])
def causes_details(request):
    context={}
    return render(request, 'fund/causes-details.html', context)

@login_required(login_url='AdminSignin')
@allowed_users(allowed_roles=['Admin'])
def admin(request):
    context={}
    return render(request, 'fund/admin_index.html', context)


@login_required(login_url='AdminSignin')
@allowed_users(allowed_roles=['Admin'])
def admin_profile(request):
    context={}
    return render(request, 'fund/admin_profile.html', context)


@login_required(login_url='AdminSignin')
@allowed_users(allowed_roles=['Admin'])
def admin_requests(request):
    admin = Admin.objects.get(admin_username=request.user)
    req = Request.objects.all().filter(status='PENDING')
    params = {
        "requests": req
    }
    return render(request, 'fund/admin_requests.html', params)

