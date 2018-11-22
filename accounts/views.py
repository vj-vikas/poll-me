from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistraionForm


# Create your views here.
def login_user(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username=username,password=password)
		print(user)
		if user is not None:
			login(request,user)
			redirect_url = request.GET.get('next','home')
			return redirect(redirect_url)

		else:
			messages.error(request,'wrong username or password')


	return render(request,'accounts/login.html',{})


def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))


def user_registration(request):
	if request.method == "POST":
		form = UserRegistraionForm(request.POST) 		
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			email = form.cleaned_data['email']
			user = User.objects.create_user(username,email=email,password=password1)
			messages.success(request,'user added')
			return HttpResponseRedirect(reverse('accounts:login'))
			print("form is valid")
	else:
		form = UserRegistraionForm() 
	return render(request,'accounts/register.html',{'form':form})