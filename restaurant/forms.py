import requests
from django.forms import ModelForm 
from .models import * 
from django import forms 
from django.utils.translation import ugettext_lazy as _
from bootstrap3_datetime.widgets import *

import datetime 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from django.http import *
from nltk import tokenize

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
	def __init__(self,user,emailid,*args,**kwargs):
		super(RecepieForm,self).__init__(*args,**kwargs)
		self.emailid = emailid
		self.fields['emailid'].initial = emailid 
		if not user.is_anonymous():		
			self.fields['emailid'].widget.attrs['readonly'] = 'true'

	class Meta:
		model = recepie
		fields = '__all__'
		exclude = ('date',)		

		widgets = {
			'date' : DateTimePicker(options={"format": "YYYY-MM-DD","pickTime": False}),
		}

class ContactForm(ModelForm):
	def __init__(self,name,email,*args,**kwargs):
		super(ContactForm,self).__init__(*args,**kwargs)
		self.name = name 
		self.email = email 
		if not name.is_anonymous():			
			self.fields['name'].initial = name
			self.fields['email'].initial = email
			fields = ['name','email']
			for i in fields:
				self.fields[i].widget.attrs['readonly'] = 'true'

	class Meta:
		model = Contact_all
		fields = '__all__'
		exclude = ('date',)

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
			'is_it_a_special_occasion' : forms.Select(choices = sorted_special_occasion),
			'booking_date' : DateTimePicker(options={"format": "YYYY-MM-DD","pickTime": False}),
		}
		initial = {'booking_date': 'hello'}

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

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		user  = authenticate(username = username,password =password)
		if user is None:
			raise ValidationError('Password and Username Doesnt match')


class SignUpForm(ModelForm):
	class Meta:
		model = Signup
		fields = '__all__'

		widgets = {
			'password' : forms.PasswordInput(),
			'confirm_password' : forms.PasswordInput(),
			'date' : DateTimePicker(options={"format": "YYYY-MM-DD","pickTime": False}),
		}

	def clean(self):
		if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
			raise ValidationError('Password Doesnt Match')

	def clean_date(self):
		today = datetime.datetime.today()
		date = '%d-%d-%d'%(today.year,today.month,today.day)
		date_of_birth = self.cleaned_data['date']
		if date_of_birth.year > today.year-10 or date_of_birth.year >= today.year:
			raise ValidationError('Not a Valid Birth Date must be utleast 14Years')
		else:
			return self.cleaned_data['date']			

	def clean_username(self):
		username =  self.cleaned_data['username']
		user = User.objects.filter(username = username).exists()
		if user:
			raise ValidationError('User Already Exist')
		else:
			return self.cleaned_data['username']			

	def clean_emailid(self):
		email =  self.cleaned_data['emailid']
		mail = User.objects.filter(email = email).exists()
		if mail:
			raise ValidationError('This Email Address Already Exist')	
		else:
			return self.cleaned_data['emailid']				

class searchtableform(forms.Form):
	search_table = forms.CharField(max_length = 10)

class searchrecepieform(forms.Form):
	search_recepie = forms.CharField(max_length = 10)

class CommentForm(ModelForm):
	def __init__(self,user,email,*args, **kwargs):	
		super(CommentForm, self).__init__(*args, **kwargs)	
		self.user = user
		if not user.is_anonymous():
			self.email = email
			self.fields['name'].initial = user
			self.fields['email'].initial = email
			fields = ['name','email']
			for i in fields:
				self.fields[i].widget.attrs['readonly'] = 'true'
	
	class Meta:
		model = Comment
		fields = '__all__'
		exclude = ('date','photo','parent')
		
	def clean_comment(self):
		comment = self.cleaned_data['comment']				
		regex = r"([a-zA-Z])"
		whitespace = r"([\S])"
		length = 30
		if (comment.__len__() <= length or not re.search(regex,comment) or not re.findall(whitespace,comment)):			
    			raise ValidationError("Comment is Not Valid")    			
		else:
			return self.cleaned_data['comment']    			
	
	#def clean_date(self):    
	#	instance = getattr(self, 'instance', None)        
	#	if instance and instance.pk:            
	#		return instance.date
	#	else:            
	#		return self.cleaned_data['date']
#class picform(ModelForm):
#	class Meta:
#		model = pic
#		fields = '__all__'			