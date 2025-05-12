import MySQLdb
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login 
from django.contrib.auth import get_user_model 
from .models import CustomUser
import os
from authappdjango.models import Avatar
from django.conf import settings
from django.contrib.auth.decorators import login_required
import base64
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
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
        image_file = request.FILES.get('image_file') 

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
        if image_file:
            image_data = image_file.read()
        else:
            def_path = os.path.join(settings.BASE_DIR,'authappdjango','static','avatar.jpg')
            with open(def_path,'rb') as f:
                image_data = f.read()
        avatar = Avatar.objects.create(user = user, image = image_data)
        return JsonResponse({'success': 'Регистрация прошла успешно'})
    
    
@login_required(login_url='/login/')
@ensure_csrf_cookie
def home_view(request):
    avatar_base64 = None
    try:
        avatar = request.user.avatar.image
        avatar_base64 = base64.b64encode(avatar).decode('utf-8')
    except Exception as e:
        print(e)
        pass
    return render(request, 'authapp/home.html', {
        'avatar_base64': avatar_base64
    })

@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({'status': 'success', 'message': 'Logged out'})