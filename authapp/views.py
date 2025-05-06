import MySQLdb
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def get_db_connection():
    return MySQLdb.connect(
        host='localhost',
        user='msadmin',
        passwd ='1234',
        db = 'test',
        charset ='utf8mb4'
    )
@ensure_csrf_cookie
def login_view(request):
    if request.method == 'GET':
        return render(request, 'authapp/login.html')
    
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        if not login or not password:
            return JsonResponse({'error':'Пустой логин или пароль'},status=400)
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE login =%s AND password=%s",(login,password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
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

        if not login or not password:
            return JsonResponse({'error':'Пустой логин или пароль'}, status = 400) 

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE login = %s ",(login,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return JsonResponse({'error':'Логин уже существует'}, status = 400)
        cursor.execute("INSERT INTO users (login,password) VALUES (%s,%s)",(login,password))
        conn.commit()

        cursor.close()
        conn.close()

        return JsonResponse({'success': 'Регистрация прошла успешно'})
