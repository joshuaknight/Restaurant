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

class RecepieForm(ModelForm):
	class Meta:
		model = recepie
		fields = '__all__'		

class ContactForm(ModelForm):
    class Meta:
        model = Contact_all
        fields = '__all__'
        widgets = {
        	'title': forms.Select(choices = TITLE_CHOICES),
        	}
       	help_texts = {
          'title' : _('select a proper title'),
       		'query' : _('Please Be Brief about your Query'),
       		'name'  : _('Name should be valid'),
       		'email' : _('The way to contact you back'),
       	}

class Order_table_Form(ModelForm):
	class Meta:
		model= order_table
		fields = '__all__'

		widgets = {
			'class_of_booking' : forms.Select(choices = sorted_class_of_booking),
			'number_of_people' : forms.Select(choices= sorted_number_of_people),
			'is_it_a_special_occasion' : forms.Select(choices = sorted_special_occasion)

		}

class ModeForm(ModelForm):
	class Meta:
		model = Mode
		fields = '__all__'

		widgets = {
			'mode_of_payement' : forms.RadioSelect(choices=Mode_Choice)
		}		

class LoginForm(ModelForm):
	class Meta:
		model = Login
		fields = '__all__'

		widgets = {
			'password' : forms.PasswordInput()
		}

class SignUpForm(ModelForm):
	class Meta:
		model = Signup
		fields = '__all__'

		widgets = {
			'password' : forms.PasswordInput(),
			'confirm_password' : forms.PasswordInput()
		}

class searchtableform(forms.Form):
	search_table = forms.CharField(max_length = 10)

class searchrecepieform(forms.Form):
	search_recepie = forms.CharField(max_length = 10)
