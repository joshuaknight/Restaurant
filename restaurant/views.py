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

class Form(FormView):
	template_name  = 'order.html'
	form_class = OrderForm

	def get_context_data(self,**kwargs):
		context = super(Form,self).get_context_data(**kwargs)
		context['time'] = timezone.now()
		return context
	
	def get_success_url(self):
		return reverse('mode_of_pay')

	def form_valid(self,form):
		form.save()
		return super(Form,self).form_valid(form)

class mode_of_pay(TemplateView):
	template_name = 'mode_of_pay.html'

	def get_context_data(self,**kwargs):
		context = super(mode_of_pay,self).get_context_data(**kwargs)
		context['time'] = timezone.now()
		return context		

class Order_Pay(FormView):
	template_name = 'pay.html'
	form_class = PaymentForm
	
	def get_context_data(self,**kwargs):
		context = super(Order_Pay,self).get_context_data(**kwargs)
		context['time'] = timezone.now()
		return context 

	def form_valid(self,form):
		form.save()
		return super(Order_Pay,self).form_valid(form)

	def get_success_url(self):
		return reverse('home')