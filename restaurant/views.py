from django.contrib.auth.models import User,AnonymousUser
from django.utils import timezone
from django.shortcuts import render
from django.http import *
from django.core.paginator import *
from django.core.exceptions import ValidationError
from django.forms import formset_factory,modelformset_factory
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from .forms import *
from django.core.urlresolvers import reverse
from django.contrib.gis.geoip import GeoIP
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.cache import cache_control
from django.core import cache 
from django.core.mail import send_mail
from .settings import *
import sqlite3 
import re 
from django.db import IntegrityError
from django.views.decorators.cache import *
from django.forms.utils import ErrorList

class home(TemplateView):
	template_name = 'home.html'

	def get_context_data(self,**kwargs):
		context = super(home, self).get_context_data(**kwargs)
		avail = Signup.objects.filter(username = self.request.user).exists()
		if avail:
			get_pic = Signup.objects.get(username = self.request.user)
			context['all'] =  get_pic.photo
		context['time'] = timezone.now()
		context['user'] = self.request.user		
		return context


class Form(home,FormView):
	template_name  = 'form.html'


	def get_context_data(self,**kwargs):
		context = super(Form, self).get_context_data(**kwargs)
		context['key'] = 'ORDER'
		return context

	def form_valid(self,form):
		form.save()
		return super(Form,self).form_valid(form)



class new_order(home,TemplateView):
	template_name = 'order.html'

	def get_context_data(self,**kwargs):
		context = super(new_order,self).get_context_data(**kwargs)
		context['order'] = OrderSpecial.objects.all()
		return context



class create_order(Form,FormView):
	template_name = 'form.html'
	form_class = OrderForm

	def get_context_data(self, **kwargs):
		context = super(create_order, self).get_context_data(**kwargs)
		context['time'] = timezone.now()
		context['key'] = 'ADD ORDER'
		return context

	def get_success_url(self):
		return reverse('order')

def delete_order(request):
	s = OrderSpecial.objects.filter()[0]
	s.delete()
	return HttpResponseRedirect('/order/')


def add_order(request):
	pass

class cart(ListView):
	template_name = 'cart.html'
	model = added_user
	context_objectname = 'cart_list'



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

class contact(home,FormView):
	template_name = 'form.html'
	form_class = ContactForm

	def get_context_data(self,**kwargs):
		context = super(contact, self).get_context_data(**kwargs)
		context['key'] = 'SEND'
		return context

	def form_valid(self,form):
		name = self.request.POST['name']
		email = self.request.POST['email']
		query = self.request.POST['query']
		message = """Hello %s and Welcome,Please Feel Free to reply to this mail
					Your Query is Processed and will be responded with the solution
					in the next working hours Thank You

					This is Your Following Query 

					%s 
					Thank You Regards 
						Owner"""%(name,query)
		mymail = EMAIL_HOST_USER
		send_mail(name,message,mymail,[email],fail_silently = False)
		return super(contact,self).form_valid(form)

	def get_success_url(self):		
		return reverse('contact_send')

def contact_send(request):
	get_pic = Signup.objects.all()
	for i in get_pic:pass
	response = HttpResponse()
	get_name = response.get('name')
	message = "Please Check Your Mail and Wait %s We Will Contact You ASAP Regarding Your Query"%get_name
	time = timezone.now()
	return render(request,'base.html',{'message':message,'time':time,'all' : i.photo})

	
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

	def get_context_data(self,**kwargs):
		context = super(Login, self).get_context_data(**kwargs)
		context['user'] = self.request.user
		context['key'] = 'LOGIN'
		context['header'] = 'Login'
		context['time'] = timezone.now()
		return context

	
	def form_valid(self,form):
		username = self.request.POST['username']
		password = self.request.POST['password']
		user = authenticate(username = username,password=password)
		if user:   			
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(self.request,user)
   			return super(Login,self).form_valid(form)		
		if user is None:
			raise ValidationError('Username and Password doesnt match')		
   		
	def get_success_url(self):
		return reverse('home')

class signup(FormView):
	template_name = 'login.html'
	form_class = SignUpForm

	
	def get_context_data(self,**kwargs):
		context = super(signup, self).get_context_data(**kwargs)
		context['user'] = self.request.user
		context['key'] = 'REGISTER'
		context['header'] = 'Signup'
		context['time'] = timezone.now()
		return context
	
	def form_valid(self,form):
		username = self.request.POST['username']	
		password = self.request.POST['password']
		email = self.request.POST['emailid']
		date = self.request.POST['date']		
		emailcheck = User.objects.filter(email=email).exists()
		user = authenticate(username = username,password = password)
		if user is None and not emailcheck:
			new_user = User.objects.create_user(username,email,password)
			new_user.backend = 'django.contrib.auth.backends.ModelBackend'
			query = """Hi %s Welcome To this Restaurant Hope Your have a Good Time
					   and please Make Sure to Click the activation Link Below To 
					   activate Your Account"""%username				
			mymail = EMAIL_HOST_USER
			send_mail(username,query,mymail,[email],fail_silently=False)
			login(self.request,new_user)
			form.save()
			message_login = 'Successfully Logged In'
			return super(signup,self).form_valid(form)
		else: 
			raise ValidationError("User already Exist")
			return super(signup,self).form_valid(form)
		
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

def activate(request):
	id=int(request.GET.get('id'))
	user = User.objects.get(id=id)
	user.is_active=True
	user.save()
	return render(request,'activation.html')


class user_view(TemplateView):
	template_name =  'user_view.html'

	def get_context_data(self,**kwargs):
		context = super(user_view,self).get_context_data(**kwargs)
		get_user = User.objects.get(username = self.request.user)
		user = User.objects.get(username = self.request.user)
		get_email = user.email 
		avail = Signup.objects.filter(username = self.request.user).exists()
		if avail:
			get_pic = Signup.objects.get(username = self.request.user)
			context['photo'] =  get_pic.photo
		get_date = Signup.objects.get(username = self.request.user)
		context['age'] = get_date.date							
		context['time']  = timezone.now()
		context['username'] = get_user
		context['email'] = get_email		
		return context 

	def get_success_url(self):
		return reverse('user_view')		

@never_cache
def edit_view(request):
	username = Signup.objects.get(username = request.user)
	get_form = modelformset_factory(Signup,fields = '__all__',
				exclude=('password','confirm_password','photo',),max_num =1)
	form = get_form(queryset=Signup.objects.filter(username = request.user))

	if request.method == 'POST':
		new_username = request.POST['form-0-username']
		new_date = request.POST['form-0-date']
		new_email = request.POST['form-0-emailid']
		regex = r"([a-zA-Z])"			
		if new_username or new_date:		
			if re.search(regex,new_username):
				length = len(str(new_username)) 
				if length > 4 and length < 12:
					user = User.objects.get(username = request.user)					
					get_user = Signup.objects.get(username = request.user)
					get_user.username = new_username			
					get_user.emailid = new_email
					get_user.date = new_date
					user.username = new_username
					user.email = new_email
					user.save() 
					get_user.save()
					message_user = 'User Is Successfully Update'
					return render(request,'edit.html',{'form':form,'message_user':message_user})
				else:
					message_user = 'Username Should be Not Lesser than 4 or Greater Than 12'
					return render(request,'edit.html',{'form':form,'message_user':message_user})						
			else:
				message_user = 'Not a Valid Username'
				return render(request,'edit.html',{'form':form,'message_user':message_user})
		else:	
			message_user = "%s Already Exsist"%new_username			
		return render(request,'edit.html',{'message_user':message_user})					
	
	return render(request,'edit.html',{'form':form,'time' : timezone.now()})


def get_page(request):
	comment_list = Comment.objects.all().order_by('-id')
	paginator = Paginator(comment_list,4)
	try:
		page = request.GET.get('page')
		get_page = paginator.page(page)	   		
	except PageNotAnInteger:
		get_page = paginator.page(1)
	except EmptyPage:
		get_page = paginator.page(paginator.num_pages)		
	return get_page			    				


class comment(FormView):
	form_class = CommentForm
	template_name = 'comment.html'

	def get_context_data(self,**kwargs):
		context = super(comment,self).get_context_data(** kwargs)		
		context['page'] = get_page(self.request)
		context['time'] = timezone.now()
		context['user'] = self.request.user				
		return context

	def get_form_kwargs(self):
		kwargs = super(comment,self).get_form_kwargs()		
		kwargs['user'] = self.request.user
		if kwargs['user'].is_anonymous():
			kwargs['email'] = ''
		else:			
			user = User.objects.get(username = self.request.user)
			kwargs['email'] = user.email
		return kwargs	

	def form_valid(self,form):
		form.save()
		return super(comment,self).form_valid(form)	

	def get_success_url(self):
		return reverse('comment')		

