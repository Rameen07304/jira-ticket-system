from .models import CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            dob = form.cleaned_data.get('dob')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            city = form.cleaned_data.get('city')
            country = form.cleaned_data.get('country')
            pincode = form.cleaned_data.get('pincode')
            address = form.cleaned_data.get('address')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'register.html', {'form': form})

            with transaction.atomic():
                user = User.objects.create_user(
                    username=username, password=password, email=email
                )
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                CustomUser.objects.create(
                    user=user, dob=dob, city=city,
                    country=country, pincode=pincode, address=address
                )

            messages.success(request, 'Registration successful. Please login')
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user =form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('homepage')

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required
def profile_view(request):
    user = request.user
    try:
        profile = CustomUser.objects.get(user=user)
    except CustomUser.DoesNotExist:
        profile = None  # superuser or missing profile
    return render(request, 'profile.html', {
        'user': user,
        'profile': profile
    })

@login_required
def update_profile_view(request):
    user= request.user
    try:
        profile = CustomUser.objects.get(user=user)
    except CustomUser.DoesNotExist:
        profile = None
    return render(request, 'update.html', {'user': user, 'profile': profile})

@require_POST
@login_required
def update_profile_ajax(request):
    user = request.user

    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')

    user.first_name = first_name
    user.last_name = last_name
    password = request.POST.get('password')

    if user.is_superuser:
        if password:
            user.set_password(password)
        user.save()
        return JsonResponse({'status': 'success', 'message': 'Admin profile updated successfully. (Password changed if provided)'})
    dob = request.POST.get('dob')
    city = request.POST.get('city')
    country = request.POST.get('country')
    pincode = request.POST.get('pincode')
    address = request.POST.get('address')

    if not all([first_name, last_name, dob, city, country, pincode, address]):
        return JsonResponse({'status': 'error', 'message': 'All fields are required.'})

    user.save()

    profile = CustomUser.objects.get(user=user)
    profile.dob = dob
    profile.city = city
    profile.country = country
    profile.pincode = pincode
    profile.address = address
    profile.save()

    return JsonResponse({'status': 'success', 'message': 'Profile updated successfully.'})


@login_required
def delete_profile(request):
    if request.method == 'POST':
        try:
            request.user.customuser.delete()
        except:
            pass  
        logout(request)
        request.user.delete()
        messages.success(request, 'Profile deleted successfully.')
        return redirect('register')
    return render(request, 'delete.html')

def view_user(request, user_id):
    profile = get_object_or_404(CustomUser, user__id=user_id)
    return render(request, 'view_user.html', {'profile': profile})

def edit_user(request, user_id):
    profile = get_object_or_404(CustomUser, user__id=user_id)
    user = profile.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        profile.dob = request.POST.get('dob')
        profile.city = request.POST.get('city')
        profile.country = request.POST.get('country')
        profile.pincode = request.POST.get('pincode')
        profile.address = request.POST.get('address')

        user.save()
        profile.save()

        messages.success(request, 'User profile updated successfully.')
        return redirect('home')

    return render(request, 'edit_user.html', {'profile': profile})


@csrf_exempt  
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect('home')

    profile = get_object_or_404(CustomUser, user__id=user_id)
    return render(request, 'confirm_delete.html', {'profile': profile})
