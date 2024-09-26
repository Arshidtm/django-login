from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import EditUserForm, DeleteUserForm,AddUserForm,UserSearchForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache,cache_control



@login_required(login_url='login')
def home_page(request):
    return render(request, 'home.html')

@never_cache
def signup_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        usname = request.POST.get('username')
        usmail = request.POST.get('email')
        uspass = request.POST.get('password1')
        uspassconf = request.POST.get('password2')

        if uspass != uspassconf:
            messages.error(request, "Passwords do not match!")
        else:
            my_user = User.objects.create_user(usname, usmail, uspass)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')

@never_cache
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        ussname = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=ussname, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials!")

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    request.session.flush() 
    return redirect('login')

# Decorator to ensure user is an admin
def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view




  
@admin_required
def adminn(request):
    users = User.objects.all().order_by('-is_superuser', 'username')
    return render(request, 'admin.html', {'users': users})

@admin_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User details updated successfully')
            return redirect('adminn')  # Ensure 'admin' is the correct URL name
    else:
        form = EditUserForm(instance=user)

    return render(request, 'admin.html', {'form': form, 'user': user})

@admin_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully')
        return redirect('adminn')

    form = DeleteUserForm(initial={'user_id': pk})
    return render(request, 'admin.html', {'delete_form': form, 'user_to_delete': user})

@admin_required
def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        user=request.POST.get('username')
        if user.isdigit():
            messages.info(request,' cannot contain number')
            return redirect('adminn')

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('adminn')
            if User.objects.filter(email=email).exists():
                messages.warning(request,'Email already used')
                return redirect('adminn')

            User.objects.create(
                username=username,
                email=email,
                password=make_password(password)
            )
            messages.success(request, 'User added successfully')
            return redirect('adminn')
    else:
        form = AddUserForm()

    return render(request, 'admin.html', {'add_form': form})

@admin_required
def user_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        users = User.objects.filter(username__icontains=search_query) 
    else:
        users = User.objects.all()

    context = {
        'users': users,
    }
    return render(request, 'admin.html', context)

@admin_required
def admin_logout(request):
    logout(request)
    request.session.flush()  # Clear the session data
    return redirect('login')