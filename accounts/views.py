from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
# Create your views here.

def signupaccount(request):
    if request.method == "GET":
        return render(request, 'signupaccount.html', {'form':UserCreateForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupaccount.html', {'form':UserCreateForm, 
                                                              'error': 'Username is already taken.'})
        else:
            return render(request, 'signupaccount.html', {'form':UserCreateForm, 'error': 'Passwords don\'t match'})


def signinaccount(request):
    if request.method == 'GET':
        return render(request, 'signinaccount.html', {'form':AuthenticationForm})
    else:
        user = authenticate(request,
            username = request.POST['username'],
            password = request.POST['password']
        )

        if user is None:
            return render(request, 'signinaccount.html', {'form':AuthenticationForm, 
                                                          'error': 'Username or Password don\'t match'})
        else:
            login(request, user)
            return redirect('home')

@login_required          
def logoutaccount(request):
    logout(request)
    return redirect('home')
