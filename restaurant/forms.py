from django.forms import ModelForm 
from .models import * 
from django import forms 
from django.utils.translation import ugettext_lazy as _
class OrderForm(ModelForm):
	class Meta:
		model = OrderSpecial
		fields = '__all__'
		
		
		widgets = {
			'Select': forms.Select(choices = Menu),
			'Flavour': forms.Select(choices=Flavour_Menu),
			'Quantity' : forms.Select(choices=Num),
			'Toppings' : forms.Select(choices=sort_topping)
		}

		help_texts = {
			'Describe' : _('Describe Us Your Own recepie')
		}

class PaymentForm(ModelForm):	
	class Meta:
		model = Payment_Process		
		fields = '__all__'

		