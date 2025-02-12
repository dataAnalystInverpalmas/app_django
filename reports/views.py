from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.shortcuts import redirect

@login_required
def index(request):
    return render(request , 'index.html', {
        'message': 'Generador de Consultas'
    })
    
def redirect_to_login_or_index(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        return redirect('login')

def login_view(request):
    print(request.method)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')#None
        
        user = authenticate(username=username, password=password)#None
        
        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'users/login.html',{
                'error': 'Usuario o contraseña incorrectos'
            })
        
    return render(request, 'users/login.html',{
        
    })