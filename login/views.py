from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    
    if request.method == "GET":
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #register user
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return HttpResponse("User create succesfully")  
            except:
                return HttpResponse("Username already exist")
        else:
            return HttpResponse("Password does not match")
    
    