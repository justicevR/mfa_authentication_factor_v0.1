
from ..api.models import App
from django.contrib.auth import decorators
from django.shortcuts import render, redirect
from apps.self_service.service_forms import RegisterAppForm, InviteAppForm
from .models import ApplicationRequest, Profile
from django.contrib.auth.decorators import login_required
from ..dashboard import decorators as dash_decorators

# Create your views here.

@login_required(login_url='login')
def profile_view(request):

    return render(request, 'accounts/profile.html',)
    
	
#@dash_decorators.admin_only
@login_required(login_url='login')
def registerApp_view(request):
    
    context={}
    user = request.user

    if request.POST:
        application = ApplicationRequest(developer=user)
        form = RegisterAppForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return render(request, 'home.html')

    else:
        form = RegisterAppForm()
        context['Request_registration_form'] = form   
    return render(request, 'accounts/register_app.html', context)


@login_required(login_url='login')
def appSummary_view(request):

    context = {}
    applications =ApplicationRequest.objects.all().filter(developer = request.user)

    total_requests = applications.count()
    registered_apps = applications.filter(status=1).count()
    pending_apps = applications.filter(status=0).count
    rejected_apps = applications.filter(status=2).count


    #context['applications'] = applications

    context = {'total_requests':total_requests, 
    'registered_apps':registered_apps, 'pending_apps':pending_apps, 'rejected_apps':rejected_apps}

    print(applications)
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
def applications_view(request):
    context = {}
    applications = ApplicationRequest.objects.all().filter(developer = request.user)




    context = {'applications':applications}

    return render(request, 'accounts/applications.html', context)

#for developers to view details of their applications
def applicationDetails_view(request, pk):
    context = {}
    app = ApplicationRequest.objects.get(id=pk)
    form = RegisterAppForm(instance=app)

    context['application_details_form'] = form

    return render(request, 'accounts/application_details.html', context)







@dash_decorators.admin_only
def applicationsAdmin_view(request):
    context = {}
    applications = ApplicationRequest.objects.all()

    total_requests = applications.count()
    registered_apps = applications.filter(status= 1).count()
    pending_apps = applications.filter(status=0).count()
    rejected_apps = applications.filter(status=2).count()

    context = {'applications':applications, 'total_requests':total_requests, 
    'registered_apps':registered_apps, 'pending_apps':pending_apps, 'rejected_apps':rejected_apps}

    return render(request, 'dashboard/applications.html', context)


@dash_decorators.admin_only
def applicationDetailsAdmin_view(request, pk):
    context = {}
    app = ApplicationRequest.objects.get(id=pk)
    form = RegisterAppForm(instance=app)

    context = {'application_details_form':form, 'app':app}
    

    return render(request, 'dashboard/application_details.html', context)






@dash_decorators.admin_only
def inviteApp_view(request, pk):
    app = ApplicationRequest.objects.get(id=pk)
    context={}

    initial_dict = {
    "name":app.name_of_app,
    "domain":app.domain,
    "org_name":app.org_name,
    "redirect_uris":app.redirect_uris,
    "user":app.developer
}
    form = InviteAppForm(initial=initial_dict)
    if request.POST:
        form=InviteAppForm(request.POST)
        if form.is_valid():
            form.save()
            app.status=1
            app.save()
            return redirect('view_apps')

    
    

    context['invite_app_form'] = form   
    return render(request, 'invite_app.html', context)




#def rejectApp_view(request):
@dash_decorators.admin_only
def rejectApp_view(request, pk):
    app = ApplicationRequest.objects.get(id=pk)
    app.status=2
    app.save()
    return redirect('view_apps')






    


