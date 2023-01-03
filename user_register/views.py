from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache

from .forms import CreateForm, CreateUserForm

# Create your views here.
"""1.function for SignUp
   2.function for Login
   3.function for HomeUser
   4.function for Logout
   5.function for AdminLogin
   6.function for Adminhome
   7.function for AdminUserSearch
   8.function for AdminUserDelete
   9.function for AdminAddUser
   10.function for AdminLogout
   11.function for AdminSearch""" 


@never_cache
def signup_user(request):
  if request.user.is_authenticated:
    return redirect('home_user')
  form = CreateForm(request.POST)
  if request.method == 'POST':
    form = CreateForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request,user)
      messages.success(request,'Account has been created')
      return redirect('home_user')
  context = {'form':form}
  return render(request,'user_register/sign_up.html',context)


@never_cache
def login_user(request):
  if request.user.is_authenticated:
    return redirect('home_user')
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username,password=password)
    if user is not None:
      if user.is_superuser is False:
        login(request,user)
        return redirect('home_user')
      else:
        return redirect('login')
    else:
      messages.info (request,'Username or Password is Incorrect')
      return redirect('login')
  return render(request,'user_register/user_login.html')


@never_cache
@login_required(login_url = 'login')
def home_user(request):
  if request.user.is_authenticated:
      if request.user.is_superuser is False:
        return render(request,'user_register/home.html')
      else:
        return redirect('admin_home')



@never_cache
def logout_user(request):
  logout(request)
  return redirect('login')


@never_cache
def admin_login(request):
  if request.user.is_superuser:
    return redirect('admin_home')
  if request.method =='POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request,username =username,password = password)
    if user is not None:
      if user.is_superuser:
        login(request,user)
        return redirect(admin_home)
      else: 
        return redirect('user_login')
    else:
      messages.info(request,'Username or Password is Incorrect')
      return redirect('admin_login')
  return render(request,'user_register/admin_login.html')


@never_cache
@login_required(login_url = 'admin_login')
def admin_home(request):
  if request.user.is_superuser:
    data = User.objects.all()
    context = {'data':data}
    return render(request,'user_register/admin_home.html',context)
  return redirect('admin_login')


def admin_user_delete(request,id):
  user = User.objects.get(id=id)
  user.delete()
  return HttpResponseRedirect(reverse('admin_home'))


def admin_add_user(request):
  # if request.method=='POST':
  #   user=User()
  #   name = request.POST.get('username')
  #   mail = request.POST.get('email')
  #   password = request.POST.get('pass')
  #   user=User.objects.create(username=name,email=mail,password=password)
  #   user.save()
  #   return redirect('admin_home')

  form=CreateForm()
  if request.method=='POST':
    form=CreateForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('admin_home')
  return render(request,'user_register/add_user.html',{'form':form,})


def update_user(request,id):
  user=User.objects.get(id=id)
  if request.method=='POST':
    name = request.POST.get('username')
    mail = request.POST.get('email')
    password = user.password
    user.email=mail
    user.username=name
    user.save()
    return redirect('admin_home')
  return render(request,'user_register/update_user.html',{'user':user})


def admin_logout(request):
  logout(request)
  return redirect('admin_login')


def admin_search(request):
  if request.user.is_superuser:
    query = request.GET['a']
    data=User.objects.filter(username__icontains = query)
    context ={'data': data}
    return render(request,'user_register/admin_search.html',context)