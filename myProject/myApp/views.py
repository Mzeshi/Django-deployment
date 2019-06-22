from django.shortcuts import render
from myApp.forms import UserForm,UserProfileInfoForm
from myApp.models import UserProfileInfo

# LOGIN PACKAGES
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def index(request):
    return render(request,'myApp/index.html',context={'index':'Home page'})

def registration(request):
    registered = False
    
    
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors) 

    else:
        
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    
    return render(request,'myApp/registration.html',{'registered':registered,'user_form':user_form,'profile_form':profile_form})
@login_required
def special(request):
    return HttpResponse('You are logged in')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:

                login(request,user)

                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('User is not active')

        else:
            print('Failed to login')
            print('Used Username: {} and Password: {}'.format(username,password))
            return HttpResponse('Invalid Login Details')
    
    else:
        return render(request,'myApp/login.html',{})