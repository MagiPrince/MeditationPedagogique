from django.http import HttpResponse
from django.shortcuts import  render, redirect
from .forms import CustomUserForm
from django.contrib.auth import login
from django.contrib import messages


# Create your views here.
def index(request):
    # Get all lectures in the DB
    context = {
        'test': 'CECI EST UN TEST'
    }
    return render(request, 'index.html', context)


def register_request(request):
    context = {}
    form = CustomUserForm(request.POST or None)
    context['form'] = form
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.' )
            return redirect(index)
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    form = CustomUserForm()
    return render(request,'registration/inscription.html', context)


def change_password_success(request):
	return render(request, 'registration/change_password_success.html')
