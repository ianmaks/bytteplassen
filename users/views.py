from django.shortcuts import render, redirect
from django.contrib.auth import login
from users.forms import RegistrationForm

# Create your views here.
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    return render(request, 'registration/register.html', {'form': form})