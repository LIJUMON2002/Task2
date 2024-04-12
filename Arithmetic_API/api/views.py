from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.conf import settings
import jwt
from django.contrib.sessions.models import Session
from datetime import datetime, timedelta

def register(request):
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not username or not email or not password:
            return HttpResponse('Some fields are empty')
        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()
        return redirect('login')
    return render(request,'register.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
                
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            token = jwt.encode({'username': username, 'exp': datetime.utcnow() + timedelta(minutes=5)}, settings.SECRET_KEY, algorithm='HS256')
            request.session['token'] = token
            return redirect('user')
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        
    return render(request,'login.html')


@csrf_exempt
def arithmetic_operation(request):
    if request.method == 'POST':
        
        token = request.session.get('token')
        if not token:
            return JsonResponse({'error': 'Token is missing'}, status=401)
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        operation = request.POST.get('operation')
        num1 = float(request.POST.get('num1'))
        num2 = float(request.POST.get('num2'))
        
        if operation not in ['add', 'subtract', 'multiply', 'divide']:
            return JsonResponse({'error': 'Invalid operation'}, status=400)
        
        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                return JsonResponse({'error': 'Cannot divide by zero'}, status=400)
            result = num1 / num2
        return JsonResponse({'result': result})
    
    return render(request,'user.html')
