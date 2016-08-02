from django.utils import timezone
from django.shortcuts import render
from django.http import *
from django.core.paginator import *
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
		return reverse('render_recepie')

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
		return reverse('render_table')	

class about(home,TemplateView):
	template_name = 'about_us.html'		

def render_recepie(request):
    recepie_list = recepie.objects.all().order_by('-id')
    paginator = Paginator(recepie_list,4) 
    try:
    	page = request.GET.get('page')
        recepie_all = paginator.page(page)
    except PageNotAnInteger:
        recepie_all = paginator.page(1)
    except EmptyPage:
        recepie_all = paginator.page(paginator.num_pages)
    return render(request, 'recepie_list.html', {'all': recepie_all,
    											  'key1':'RecepieName',
    											  'key2':'EmailID',
    											  'key3':'Date'})


def render_table(request):
	book_list = order_table.objects.all().order_by('-id')
	paginator = Paginator(book_list,2) 
	try:
		page = request.GET.get('page')
	   	book = paginator.page(page)
	except PageNotAnInteger:
	    book = paginator.page(1)
	except EmptyPage:
	    book = paginator.page(paginator.num_pages)
	return render(request, 'book_list.html', {'all': book,})