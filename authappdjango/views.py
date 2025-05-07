import MySQLdb
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login 
from django.contrib.auth import get_user_model 
from .models import CustomUser

# Create your views here.
def get_db_connection():
    return MySQLdb.connect(
        host='localhost',
        user='msadmin',
        passwd ='1234',
        db = 'test2',
        charset ='utf8mb4'
    )
@ensure_csrf_cookie
def login_view(request):
    if request.method == 'GET':
        return render(request, 'authapp/login.html')
    
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({'error':'Пустой логин или пароль'},status=400)
        
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request,user)
            return JsonResponse({'succcess':'Успешный вход'})
        else:
            return JsonResponse({'error':'Неверный логин или пароль'},status = 400)

@ensure_csrf_cookie
def register_view(request):
    if request.method == 'GET':
        return render(request,'authapp/register.html')

    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        gender = request.POST.get('gender')

        if not login or not password:
            return JsonResponse({'error':'Пустой логин или пароль'}, status = 400) 

    

    if CustomUser.objects.filter(username=login).exists():   
            return JsonResponse({'error':'Логин уже существует'}, status = 400)
    else:
        user = CustomUser.objects.create_user(
        username=login,
        password=password,
        gender = gender
        )
        return JsonResponse({'success': 'Регистрация прошла успешно'})
