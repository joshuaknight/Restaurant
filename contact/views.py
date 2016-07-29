from django.utils import timezone
from .forms import *
from django.shortcuts import *
from django.http import *
from django.core.urlresolvers import reverse
from django.views.generic.edit import *

class contact(FormView):
	template_name = 'contact.html'
	form_class = Contact

	def get_context_data(self,**kwargs):
		context = super(contact,self).get_context_data(**kwargs)
		context['time'] = timezone.now()
		return context
	
	def form_valid(self,form):
		form.save()
		return super(contact,self).form_valid(form)

	def get_success_url(self):
		return reverse('home')