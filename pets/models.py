from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone

class Pet(models.Model):
	name = models.CharField(max_length=105)
	age = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
	available = models.BooleanField(default=True)
	image = models.ImageField(null=True, blank=True)
	price = models.DecimalField(
		max_digits=7, decimal_places=3,
		validators=[MinValueValidator(0),MaxValueValidator(5000)]
	)
	GENDER_CHOICES = (
		('Male', 'Male'),
		('Female', 'Female'),
	)
	SPECIES_CHOICES = (
		('Dog', 'Dog'),
		('Cat', 'Cat'),
		('Bird', 'Bird'),
	)
	gender = models.CharField(
		max_length=6,
		choices=GENDER_CHOICES,
		default='Male',
	)
	species = models.CharField(
		max_length=4,
		choices=SPECIES_CHOICES,
		default='Dog'
	)
	breed = models.CharField(max_length=105, null=True, blank=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	last_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('pet-detail', kwargs={'pet_id': self.id})