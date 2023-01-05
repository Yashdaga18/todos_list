from django.shortcuts import render,redirect
from datetime import date
from .models import Task
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    if request.method == 'POST':
        t = Task(title=request.POST["title"],user = request.user)
        t.save()
        return redirect('index')
        
    if request.method == 'GET':
        tasks = Task.objects.all()
        print(tasks)
        current_year = date.today().year
        return render(request, 'todo/index.html',{
            "current_year": current_year,
            "tasks": tasks
        })

def delete(request, id):
    dell = Task.objects.get(id= id)
    dell.delete()
    return redirect('/')

def edit(request, id):

    if request.method == 'POST':
        t = Task.objects.get(id= id)
        t.title = request.POST.get('title')
        t.is_complete = False
        t.save()
        return redirect('/')

    if request.method == 'GET':
        current_year = date.today().year
        task = Task.objects.get(id= id)
        return render(request, 'todo/edit.html', {'task':task,"current_year": current_year})

def completed(request, id):
    task = Task.objects.get(id= id)
    task.is_complete = True
    task.save()
    return redirect('/')

#....................user.........................

def register(request):

    if request.method == 'POST':
        if request.POST.get('password') != request.POST.get('repassword'):
            return render(request, 'todo/register.html', {
                'samepassworderror':"Enter same password",
                
                })
        if len(request.POST.get('password'))< 5:
            return render(request, 'todo/register.html', {
                "lengtherror":"Password must be at least 5 characters"
                })

        else:
            username = request.POST.get('username')
            firstname = request.POST.get('fname')
            lastname = request.POST.get('lname')
            password = request.POST.get('password')
            user = User.objects.create_user(username=username, password=password)
            user.firstname = firstname
            user.lastname = lastname
            user.save()
            return redirect('login')
            

    if request.method == 'GET':
        return render(request, 'todo/register.html')

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return render(request,'todo/index.html')
        else:
            return render(request, 'todo/login.html',{'error':"Bad Credentials"})

    if request.method == 'GET':
        return render(request, 'todo/login.html')

def logoutPage(request):
    logout(request)
    return redirect('index')