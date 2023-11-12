from django.shortcuts import render
from .forms import UserForm,LoginForm
from django.http import HttpResponse,HttpResponseRedirect
from .models import User
# Create your views here.

def register(request):
    if request.method=="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("login")
    form1 = UserForm()
    context={'form':form1}
    return render(request,"reg_form.html",context)

def login(request):
    if request.method == 'POST':
        form2 = LoginForm(request.POST)
        if form2.is_valid():
            test = form2.cleaned_data
            u = test.get("username")
            # print(u)
            p = test.get("password")
            # print(p)
            try:
                a = User.objects.raw("SELECT username,password FROM login_user WHERE username=%s and password=%s",[str(u),str(p)])
                # print("fs-----")
                # print(a[0].password)
                if a[0].password==p:
                    return HttpResponseRedirect("login_home")
            except:
                return HttpResponse("Invalid Username or Password")
        else:
            return HttpResponse("Invalid!")
    else:
        form3 = LoginForm()
        context={'log':form3}
        return render(request,"login_form.html",context)
    
def login_home(request):
    return render(request,"login_home.html")