from django.shortcuts import render,redirect
from django.views.generic import View 
from todoapp.forms import TodoForm,RegistrationForm,LoginForm
from todoapp.models import Todo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from django.db.models import Sum,Count
from django.utils.decorators import method_decorator
from todoapp.decorator import signin_required
from django.contrib import messages
from django.views.decorators.cache import never_cache

decs=[signin_required,never_cache]
@method_decorator(decs,name="dispatch")
class TodoCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TodoForm()
        return render(request,'todo_add.html',{'form':form})

    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            form.instance.user_object=request.user
            form.save()
            messages.success(request,'Todo has been added')
            return redirect('todo-list')
        messages.error(request,'failed to add todo ')
        return render(request,'todo_add.html',{'form':form})

@method_decorator(decs,name="dispatch")
class TodoListView(View):
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        cur_month=timezone.now().month
        cur_year=timezone.now().year
        qs=Todo.objects.filter(user_object=request.user)
        group_by_qs=Todo.objects.filter(
            user_object=request.user,
            created_date__month=cur_month,
            created_date__year=cur_year
        ).values("status").annotate(number=Count("status"))
        print(group_by_qs)
        return render(request,'todo_list.html',{'data':qs,"status_count":group_by_qs})

@method_decorator(decs,name="dispatch")
class TodoUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todo.objects.get(id=id)
        form=TodoForm(instance=todo_object)
        return render(request,'todo_edit.html',{'form':form})

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todo.objects.get(id=id)
        form=TodoForm(request.POST,instance=todo_object)
        if form.is_valid():
            form.save()
            messages.success(request,'Todo updated')
            return redirect('todo-list')
        messages.error(request,'failed to change')
        return render(request,'todo_edit.html',{'form':form})

@method_decorator(decs,name="dispatch")
class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todo.objects.get(id=id).delete()
        messages.success(request,'Todo deleted')
        return redirect('todo-list')

@method_decorator(decs,name="dispatch")
class TodoDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todo.objects.get(id=id)
        return render(request,'todo_detail.html',{'data':qs})

class SignupView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,'register.html',{'form':form})

    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'user registered')
            # User.objects.create_user(**form.cleaned_data)
            return redirect("signin")
        messages.error(request,'User registration failed')
        return render(request,'register.html',{'form':form})

class SigninView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,'login.html',{'form':form})

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            uname=data.get("username")
            pwd=data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                messages.success(request,'Logged In')
                return redirect("todo-list")
        messages.error(request,'login failed')
        return render(request,'login.html',{'form':form})

@method_decorator(decs,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.success(request,'logged out')
        return redirect("signin")
    