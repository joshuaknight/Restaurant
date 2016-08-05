from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import render
from django.http import *
from django.core.paginator import *
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from .forms import *
from django.core.urlresolvers import reverse
from django.contrib.gis.geoip import GeoIP
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.cache import cache_control
from django.core import cache 

	
class home(TemplateView):
	template_name = 'base.html'
	def get_context_data(self,**kwargs):
		context = super(home, self).get_context_data(**kwargs)
		context['time'] = timezone.now()
		context['user'] = self.request.user
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

class mode_of_pay(Form,FormView):
	template_name = 'form.html'
	form_class = ModeForm	

	def get_context_data(self,**kwargs):
		context = super(mode_of_pay, self).get_context_data(**kwargs)
		context['key'] = 'NEXT'
		return context	
	
	def get_success_url(self):
		if self.request.POST['mode_of_payement'] == '3':
			return reverse('payement')			
		if self.request.POST['mode_of_payement'] == '1':
			return reverse('home')			
		if self.request.POST['mode_of_payement'] == '2':			
			return reverse('internet')

class Order_Pay(Form,FormView):
	template_name = 'form.html'
	form_class = PaymentForm

	def get_context_data(self,**kwargs):
		context = super(Order_Pay, self).get_context_data(**kwargs)
		context['key'] = 'PAY'
		return context

class internet(home,TemplateView):
	template_name = 'base.html'
	def get_context_data(self,**kwargs):
		context = super(internet, self).get_context_data(**kwargs)
		context['message'] = 'Internet Banking Is Down at the Momment Sorry for the Inconvenience !'
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
	#@login_required('/accounts/login')
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

@login_required()
def render_recepie(request):
    recepie_list = recepie.objects.all().order_by('-id')
    form = searchrecepieform
    paginator = Paginator(recepie_list,4) 
    try:
    	page = request.GET.get('page')
        recepie_all = paginator.page(page)
    except PageNotAnInteger:
        recepie_all = paginator.page(1)
    except EmptyPage:
        recepie_all = paginator.page(paginator.num_pages)
    return render(request, 'recepie_list.html', {'all': recepie_all,
    		                                     'form':form,
    											  'key1':'RecepieName',
    											  'key2':'EmailID',
    											  'key3':'Date',
    											  'time': timezone.now()})

@login_required()
def render_table(request):
	book_list = order_table.objects.all().order_by('-id')
	paginator = Paginator(book_list,2) 
	form = searchtableform
	try:
		page = request.GET.get('page')
	   	book = paginator.page(page)
	except PageNotAnInteger:
	    book = paginator.page(1)
	except EmptyPage:
	    book = paginator.page(paginator.num_pages)
	return render(request, 'book_list.html', {'all': book,	
										      'form' : form,		  
											  'time' : timezone.now()})

def book_search(request):
	book_list = ''
	q = ''
	if request.method == 'POST':
		if request.POST['search_table']:
			q = request.POST['search_table']
			book_list = order_table.objects.filter(table_name__icontains = q)
	return render(request,'search.html',{
										 'q' : q,
		                                 'search':book_list,})		

def recepie_search(request):
	recepie_list = ''
	q = ''
	if request.method == 'POST':
		if request.POST['search_recepie']:
			q = request.POST['search_recepie']
			recepie_list = recepie.objects.filter(recepie_name__icontains = q)
	return render(request,'new_recepie.html',{
										 'q' : q,
		                                 'search':recepie_list,})				                                 	

def render_order(request):
	order_list = []
	order_list.append(OrderSpecial.objects.all().order_by('-id'))

	if order_list:
		return render(request, 'order_list.html', {'i': order_list[0],
												'time' : timezone.now()})
			


def delete(request):
	order = OrderSpecial.objects.filter()[0]
	order.delete()
	return HttpResponseRedirect('/order/current')



class Login(FormView):
	template_name = 'login.html'
	form_class = LoginForm
	
	def form_valid(self,form):
		username = self.request.POST['username']
		password = self.request.POST['password']
		user = authenticate(username = username,password=password)
   		if user is None:
   			raise ValidationError('Password and Username Doesnt Match')
		if user:   			
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(self.request,user)
   			return super(Login,self).form_valid(form)		
   	
	def get_context_data(self,**kwargs):
		context = super(Login, self).get_context_data(**kwargs)
		context['user'] = self.request.user
		context['key'] = 'LOGIN'
		context['time'] = timezone.now()
		return context

	def save_profile(backend, user, response, *args, **kwargs):
		profile = user.get_profile()
		if profile is None:
			profile = Profile(user_id=user.id)
		profile.gender = response.get('gender')
  		profile.link = response.get('link')
		profile.timezone = response.get('timezone')
   		profile.save()

	def get_success_url(self):
		return reverse('home')

class signup(FormView):
	template_name = 'login.html'
	form_class = SignUpForm

	
	def get_context_data(self,**kwargs):
		context = super(signup, self).get_context_data(**kwargs)
		context['user'] = self.request.user
		context['key'] = 'REGISTER'
		context['time'] = timezone.now()
		return context
	
	def form_valid(self,form):
		msg = []
		if self.request.POST['password'] != self.request.POST['confirm_password']:
			raise ValidationError('Password Doesnt Match')			
		username = self.request.POST['username']	
		password = self.request.POST['password']
		email = self.request.POST['emailid']		
		user = authenticate(username = username,password = password)
		if user is None:
			new_user = User.objects.create_user(username,email,password)
			new_user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(self.request,new_user)
			msg.append('Successfully Logged In')
			return super(signup,self).form_valid(form)
		if user is not None:
			raise ValidationError("User Already Exsist")			

	def get_success_url(self):
		return reverse('home')			

def logout_(request):	
	logout(request)

	message= "You are Successfully Logged Out"
	time = timezone.now()
	request.session.flush()
 	if hasattr(request, 'user'):
 		request.user = AnonymousUser()
	return render(request,'base.html',{'message' : message,'time':time})

