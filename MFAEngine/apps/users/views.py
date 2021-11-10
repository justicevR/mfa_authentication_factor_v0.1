
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from apps.users.forms import AccountAuthenticationForm, RegistrationForm
from ..dashboard import decorators
from ..self_service.models import Profile






@decorators.unauthenticated_user
def registration_view(request):
    
    context={}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            Profile.objects.create(user=user)
            
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password) 
            login(request, account)
            return redirect('login')

        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form']= form
    return render(request, 'register.html', context)



def logout_view(request):
    logout(request)
    return redirect('login')


@decorators.unauthenticated_user
def login_view(request):
    context = {}

    user = request.user

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
            try:
                if request.GET['next']:
                    return redirect(request.GET['next'])
            except Exception as e:
                return redirect('home')

    else:
        form = AccountAuthenticationForm

    context['login_form'] = form
    return render(request, 'login.html', context)


















# Create your views here.


