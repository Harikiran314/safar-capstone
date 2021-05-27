from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decoraters import unauthenticated_user, allowed_users
from django.contrib import messages
from .models import *
from .forms import CreateUserForm
from django.db.models import Q
from django.http import Http404


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
def profile(request):
    if request.method == 'POST':
        acc = Account.objects.get(username=request.user)
        request_category = request.POST['category']
        amount = request.POST['amount']
        deadline = request.POST['deadline']
        desc = request.POST['desc']
        identityImage = request.FILES['image']
        image1 = request.FILES['image1']
        image2 = request.FILES['image2']
        req = Request(  account_id=acc,
                        request_category=request_category,
                        amount=amount,
                        deadline=deadline,
                        desc=desc,
                        identity_image=identityImage,
                        image1=image1,
                        image2=image2
                        )
        req.save()


    acc = Account.objects.get(username=request.user)
    req = Request.objects.all().filter(account_id=acc)
    params = {
        "account": acc,
        "requests": req
    }
    return render(request, 'fund/profile.html', params)


@login_required(login_url='Signin')
@allowed_users(allowed_roles=['Account'])
def causes(request):
    category = request.GET.get("category", "")
    if category:
        req = Request.objects.all().filter(status='ACCEPTED')
        req = req.filter(request_category=category)
    else:
        req = Request.objects.all().filter(status='ACCEPTED')
    params = {
        "requests": req
    }
    return render(request, 'fund/causes.html', params)

@login_required(login_url='Signin')
@allowed_users(allowed_roles=['Account'])
def causes_details(request, pk):
    if request.method == 'POST':
        requestId = request.POST['requestId']
        donation = request.POST['amount']
        try:
            req = Request.objects.get(id=requestId)
        except Request.DoesNotExist:
            raise Http404("Cause request does not exist")
        amount = req.collected + float(donation)
        req.collected=amount
        req.save()
        return redirect('payment')

    try:
        req = Request.objects.get(id=pk)
    except Request.DoesNotExist:
        raise Http404("Cause request does not exist")
    params = {
        "request": req
    }
    return render(request, 'fund/causes-details.html', params)


@login_required(login_url='Signin')
@allowed_users(allowed_roles=['Account'])
def myRequest(request, pk):
    if request.method == 'POST':
        requestId = request.POST['requestId']
        amount = request.POST['amount']
        account_no = request.POST['Bank-details']
        account_name = request.POST['account-name']
        IFSC = request.POST['IFSC']
        acc = Account.objects.get(username=request.user)
        req = Request.objects.get(id=requestId)
        bank = Bank_details(account_id=acc,
                            request_id=req,
                            bank_account_no=account_no,
                            bank_account_name=account_name,
                            IFSC=IFSC
                            )
        payment = Payment(  account_id=acc,
                            request_id=req,
                            amount=amount,
                            )
        req.status = 'COMPLETED'
        payment.save()
        bank.save()
        req.save()

    try:
        req = Request.objects.get(id=pk)
    except Request.DoesNotExist:
        raise Http404("Cause request does not exist")
    acc = Account.objects.get(username=request.user)
    if req.account_id!=acc:
        raise Http404("Cause request does not exist")
    params = {
        "request": req
    }
    return render(request, 'fund/myRequest.html', params)


def payment(request):
    context={}
    return render(request, 'fund/payment.html', context)


@login_required(login_url='AdminSignin')
@allowed_users(allowed_roles=['Admin'])
def admin(request):
    if request.method == 'POST':
        admin = Admin.objects.get(admin_username=request.user)
        requestId = request.POST['requestId']
        action = request.POST['action']
        admin_message = request.POST['desc']
        req = Request.objects.get(id=requestId)
        pay = Payment.objects.get(request_id=req)
        pay.status = action
        if action == "SUCCESSFUL":
            req.status = "PAYMENT SUCCESSFUL"
        else:
            req.status = "PAYMENT FAILED"
        req.save()
        pay.save()

    admin = Admin.objects.get(admin_username=request.user)
    req = Request.objects.all().filter(status='COMPLETED')
    details = []
    for r in req:
        p = Bank_details.objects.get(request_id=r)
        details.append((r,p))
    params = {
        "details": details,
    }
    return render(request, 'fund/admin_index.html', params)


@login_required(login_url='AdminSignin')
@allowed_users(allowed_roles=['Admin'])
def admin_profile(request):
    admin = Admin.objects.get(admin_username=request.user)
    acc = admin.accept_set.all().filter(Q(request_id__status='ACCEPTED') | Q(request_id__status='CANCELLED') | Q(request_id__status='COMPLETED'))
    
    params = {
        "requests": acc
    }
    return render(request, 'fund/admin_profile.html', params)


@login_required(login_url='AdminSignin')
@allowed_users(allowed_roles=['Admin'])
def admin_requests(request):
    if request.method == 'POST':
        admin = Admin.objects.get(admin_username=request.user)
        requestId = request.POST['requestId']
        action = request.POST['action']
        admin_message = request.POST['desc']
        req = Request.objects.get(id=requestId)
        acc, created = Accept.objects.get_or_create(request_id=req)
        acc.admin_id = admin
        acc.save()
    
        if action == 'UPDATE':
            req.admin_msg = admin_message
        else:
            if action == 'APPROVE':
                req.status='ACCEPTED'
                req.admin_msg = admin_message
            else:
                req.status = 'CANCELLED'
                req.admin_msg = admin_message
        req.save()

    admin = Admin.objects.get(admin_username=request.user)
    req = Request.objects.all().filter(status='PENDING')
    params = {
        "requests": req
    }
    return render(request, 'fund/admin_requests.html', params)

