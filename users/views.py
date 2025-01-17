from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from users.forms import UserRegisterForm, UserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

# Create your views here.

def login_request(request):
    msg_login = ""
    if request.method == "POST":
        form = AuthenticationForm(request,data = request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")
            user = authenticate(username = usuario, password = contra)
            if user is not None:
                login(request, user)
                return render(request,"appfinalds/inicio.html",{"mensaje":f"Bienvenido {usuario}"})
            else:
                return render(request,"appfinalds/login_error.html")
        else:
            return render(request,"appfinalds/login_error.html")
        
    form = AuthenticationForm()
    return render(request,"appfinalds/login.html",{'form':form, "msg_login":msg_login})

def register(request):
    msg_register = ""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"appfinalds/registro_ok.html")
        else:
            msg_register = "Error en los datos ingresados"
        msg_register = "Error en los datos ingresados"
    form = UserRegisterForm()
     
    return render(request,"appfinalds/registro.html",{'form':form, "msg_register":msg_register})
    
def custom_logout(request):
    logout(request)
    return render(request,'appfinalds/logout.html')

def errorlogin(request):
    return render(request,"appfinalds/errorlogin.html")


@login_required
def editar_perfil(request):
    usuario = request.user
    
    if request.method == "POST":
        miformulario = UserEditForm(request.POST, instance=usuario)
        
        if miformulario.is_valid():
            miformulario.save()
            
            return render(request,"appfinalds/inicio.html")
        
    else:
        miformulario = UserEditForm(instance=usuario)
        
    return render(request,"appfinalds/editar_perfil.html",{"miformulario":miformulario,"usuario":usuario})


class CambiarPass(LoginRequiredMixin,PasswordChangeView):
    template_name = 'appfinalds/cambiar_pass.html'
    success_url = reverse_lazy('EditarPerfil')