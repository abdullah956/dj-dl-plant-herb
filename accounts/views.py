from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import History
from django.contrib.auth.decorators import login_required

# Signup view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            login(request, user)  # Log the user in after successful signup
            messages.success(request, "Account created and logged in successfully!")
            return redirect('home')  # Redirect to the home page after signup and login
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a homepage or dashboard after login
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'accounts/login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logging out

# @login_required
# def history(request):
#     search_query = request.GET.get('search', '')  # Get the search query from the URL parameter
#     history_records = History.objects.filter(user=request.user)

#     if search_query:
#         history_records = history_records.filter(action__icontains=search_query)

#     return render(request, 'accounts/history.html', {'history_records': history_records, 'search_query': search_query})

@login_required
def history(request):
    search_query = request.GET.get('search', '')  # Search filter
    history_records = History.objects.filter(user=request.user)

    if search_query:
        history_records = history_records.filter(action__icontains=search_query)

    return render(request, 'accounts/history.html', {
        'history_records': history_records,
        'search_query': search_query
    })

@login_required
def delete_history(request):
    History.objects.filter(user=request.user).delete()
    messages.success(request, "All history records deleted successfully.")
    return redirect('history')

@login_required
def delete_single_history(request, record_id):
    History.objects.filter(id=record_id, user=request.user).delete()
    messages.success(request, "History record deleted successfully.")
    return redirect('history')