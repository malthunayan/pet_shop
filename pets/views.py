from django.shortcuts import render, redirect
from .models import Pet
from .forms import PetForm, SigninForm, SignupForm, PetUpdateForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def pet_list(request):
	pets = Pet.objects.all()
	order = request.GET.get("o")
	if order=='Alphabetical Order':
		pets = pets.order_by('name')
	elif order=='Reverse Alphabetical Order':
		pets = pets.order_by('-name')
	elif order=='Most Recently Updated':
		pets = pets.order_by('-last_updated','name')
	elif order=='Least Recently Updated':
		pets = pets.order_by('last_updated','name')
	elif order=='Most Expensive to Least Expensive':
		pets = pets.order_by('-price','name')
	elif order=='Least Expensive to Most Expensive':
		pets = pets.order_by('price','name')
	else:
		pets = pets
	query = request.GET.get("q")
	if query:
		pets = pets.filter(
			Q(name__icontains=query)|
			Q(species__iexact=query)|
			Q(gender__iexact=query)
		).distinct()
	view = request.GET.get('view')
	if view:
		pets = pets.filter(owner=request.user)
	context = {
		'pets': pets,
		'sort': [
			'Alphabetical Order',
			'Reverse Alphabetical Order',
			'Most Recently Updated','Least Recently Updated',
			'Most Expensive to Least Expensive',
			'Least Expensive to Most Expensive'
		],
	}
	return render(request, 'list.html', context)

def pet_detail(request, pet_id):
	pet = Pet.objects.get(id=pet_id)
	context = {
		'pet': pet,
	}
	return render(request, 'detail.html', context)

def pet_add(request):
	if request.user.is_anonymous:
		messages.warning(request, 'Please login before trying to perform this action.')
		return redirect('signin')
	form = PetForm()
	if request.method == 'POST':
		form = PetForm(request.POST, request.FILES)
		if form.is_valid():
			pet = form.save(commit=False)
			pet.owner = request.user
			pet.save()
			messages.success(request, 'Pet successfully added!')
			return redirect('pet-list')
	context = {
		'form': form,
	}
	return render(request, 'add_pet.html', context)

def pet_update(request, pet_id):
	pet = Pet.objects.get(id=pet_id)
	if not (request.user.is_staff or request.user==pet.owner):
		messages.warning(request, 'You are not the owner of this pet.')
		return redirect('pet-list')
	form = PetUpdateForm(instance=pet)
	if request.method == 'POST':
		form = PetUpdateForm(request.POST, request.FILES, instance=pet)
		if form.is_valid():
			pet = form.save()
			messages.success(request, 'Pet details updated!')
			return redirect(pet)
	context = {
		'form': form,
		'pet': pet,
	}
	return render(request, 'update_pet.html', context)

def pet_delete(request, pet_id):
	Pet.objects.get(id=pet_id).delete()
	messages.warning(request, 'The pet has been successfully deleted from the database.')
	return redirect('pet-list')

def signup(request):
	form = SignupForm()
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user_obj = form.save(commit=False)
			user_obj.set_password(user_obj.password)
			user_obj.save()
			login(request, user_obj)
			messages.success(request, 'Welcome to our humble PetShop')
			return redirect('pet-list')
	context = {
		'form': form,
	}
	return render(request, 'signup.html', context)

def signin(request):
	form = SigninForm()
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				messages.success(request, 'Welcome back!')
				return redirect('pet-list')
			messages.warning(request, 'Invalid username/password combination.')
	context = {
		'form': form,
	}
	return render(request, 'signin.html', context)

def signout(request):
	logout(request)
	return redirect('pet-list')

