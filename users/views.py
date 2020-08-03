from django.shortcuts import render,redirect
from .forms import UserRegForm
from django.contrib import messages

# UserRegForm is subclass of ModelForm UserCreationForm
#https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/#django.forms.ModelForm

def register(request):
    #checks if the form is empty(when false) or not(when true)
    if request.method == 'POST':
        f = UserRegForm(request.POST)#variable that stores the forms
        if f.is_valid():
            f.save()
            username = f.cleaned_data.get('username')
            messages.success(request, f'Your Account has been created ! You are now able to login')
            return redirect('login')
    else:
        f=UserRegForm()
    return render(request, 'users/register.html', {'form': f})
