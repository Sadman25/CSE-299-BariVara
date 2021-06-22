from django.shortcuts import render , redirect
from django.contrib import messages
from .forms import UserSignUpForm , UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

# Function for user signup
def signup(request):
    if request.method =='POST':
        form=UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form=UserSignUpForm()
    return render(request, 'users/signup.html',{'form':form})

def HomePage(request):
    return render(request, 'users/Login.html')

#Function for user profile
@login_required
def profile(request):
    if request.method=='POST':
        #data = Profile.objects.filter(user=request.user)
        update_form=UserUpdateForm(request.POST, instance=request.user)
        profile_form=ProfileUpdateForm(request.POST, request.FILES ,instance=request.user.profile)
        if update_form .is_valid() and profile_form.is_valid():
            update_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        else:
            return render(request, 'users/profile.html')
    else:
        update_form=UserUpdateForm(instance=request.user)
        profile_form=ProfileUpdateForm(instance=request.user)
    context={
        'update_form': update_form,
        'profile_form':profile_form,
    }
    return render(request, 'users/profile.html', context)

