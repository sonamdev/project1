from django.shortcuts import render

# Create your views here.
# dashboard/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, UploadFileForm

# Registration view
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# Login view
# ...

# File upload view
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'File uploaded successfully.')
            return redirect('dashboard')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})

# Dashboard view
@login_required
def dashboard(request):
    user_files = UploadedFile.objects.filter(user=request.user).order_by('-upload_date')
    context = {'user_files': user_files}
    return render(request, 'dashboard.html', context)
