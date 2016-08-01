from django.utils import timezone
from django.shortcuts import render
from django.http import *
import requests
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from .forms import *
from django.core.urlresolvers import reverse
from django.contrib.gis.geoip import GeoIP
	

class home(TemplateView):
	template_name = 'base.html'
	def get_context_data(self,**kwargs):
		context = super(home, self).get_context_data(**kwargs)
		context['time'] = timezone.now()
		return context


class Form(home,FormView):
	template_name  = 'form.html'
	form_class = OrderForm

	def get_context_data(self,**kwargs):
		context = super(Form, self).get_context_data(**kwargs)
		context['key'] = 'ORDER'
		return context

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

	def get_context_data(self,**kwargs):
		context = super(Order_Pay, self).get_context_data(**kwargs)
		context['key'] = 'PAY'
		return context
	
class add_recepie(Form,FormView):
	template_name = 'form.html'
	form_class = RecepieForm

	def get_context_data(self,**kwargs):
		context = super(add_recepie, self).get_context_data(**kwargs)
		context['key'] = 'ADD RECEPIE'
		return context

	def get_success_url(self):
		return reverse('home')

class contact(Form,FormView):
	template_name = 'form.html'
	form_class = ContactForm

	def get_context_data(self,**kwargs):
		context = super(contact, self).get_context_data(**kwargs)
		context['key'] = 'SEND'
		return context

	def get_success_url(self):
		return reverse('contact_send')

class contact_send(TemplateView):
	template_name = 'base.html'
	def get_context_data(self,**kwargs):
		context = super(contact_send, self).get_context_data(**kwargs)
		context['message'] = "Please Wait We Will Contact You ASAP Regarding Your Query"
		return context	

	
class Order_Table(Form,FormView):
	template_name = 'form.html'
	form_class = Order_table_Form	

	def get_context_data(self,**kwargs):
		context = super(Order_Table, self).get_context_data(**kwargs)
		context['key'] = 'BOOK'
		return context

	def get_success_url(self):
		return reverse('home')	

class about(home,TemplateView):
	template_name = 'about_us.html'		

class render_recepie(DetailView):
	template_name = 'detailview.html'
	model = recepie
