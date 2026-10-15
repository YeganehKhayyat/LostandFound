from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import logout
# Create your views here.

def register(requests):
    if requests.method == "POST":
        form = RegisterForm(requests.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            messages.success(
                requests ,
                f"{username} با موفیقت وارد سایت شدید."
            )
            form.save()
            return redirect(
                "login"
            )
    else:
        form = RegisterForm()
        
    data = {
        'form' : form
    }
    
    return render(
        requests ,
        "authentication/register.html",
        data
    )
    
def logout_view(requests):
    logout(requests)
    return redirect('login')

