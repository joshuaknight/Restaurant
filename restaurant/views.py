from django.utils import timezone
from django.shortcuts import render
from django.http import *
from django.views.generic import *
from .forms import *
from django.core.urlresolvers import reverse

class home(TemplateView):
	template_name = 'base.html'

	def get_context_data(self,**kwargs):
		context = super(home, self).get_context_data(**kwargs)
		context['time'] = timezone.now()
		return context

class Form(home,FormView):
	template_name  = 'form.html'
	form_class = OrderForm

	def get_success_url(self):
		return reverse('mode_of_pay')

	def form_valid(self,form):
		form.save()
		return super(Form,self).form_valid(form)

class mode_of_pay(home,TemplateView):
	template_name = 'mode_of_pay.html'	

class Order_Pay(Form,FormView):
	template_name = 'form.html'
	form_class = PaymentForm
	
class add_recepie(Form,FormView):
	template_name = 'form.html'
	form_class = RecepieForm

	def get_success_url(self):
		return reverse('home')

class contact(Form,FormView):
	template_name = 'form.html'
	form_class = ContactForm

	def get_success_url(self):
		return reverse('home')
	
class Order_Table(FormView):
	template_name = 'form.html'
	form_class = Order_table_Form	

	def get_success_url(self):
		return reverse('home')	