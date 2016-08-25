from django.db import models 
from django.contrib.auth.models import User,UserManager
import re
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser
import datetime
from time import time 
from markdown_deux import *
from django.utils import timezone
from django.utils.safestring import mark_safe

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


def validate_describe(value,length=30):
	regex = r"([a-zA-Z])"
	if (len(str(value)) <= length or not re.search(regex,value)):
    		raise ValidationError("Be More Specific")

def validate_name(value,length=5):
	regex = r"([a-zA-Z])"
	if (len(str(value)) <= length or not re.search(regex,value)):
    		raise ValidationError(u'%s is not a Valid Name' % value)

def validate_len(value,length=20):
	regex = r"([a-zA-Z]+)"
	if not re.search(regex,value) or len(str(value)) < length:
		raise ValidationError(u"Not Valid Be More Specific")
		
def validate_recepie(value):
	regex = r"([a-zA-Z])"
	if not re.search(regex,value):
		raise ValidationError('Please Select a Recepie')

def validate_pass(value,length=8):
	if len(str(value)) < length:
		raise ValidationError('Minimum 8 character')

Menu = {('....','....'),
		('Burger','Burger'),
		('Pizza','Pizza',),
		('Sandwich','Sandwich',),
		('Pasta','Pasta',),
		}

Flavour_Menu = {
		('....','....'),
		('Veg','Veg'),
		('NonVeg','NonVeg'),
		('Mixed','Mixed'),
}
Toppings = {
	('....','....'),
	('Onion','Onion'),
	('Cheese','Cheese'),
	('MaxCheese','MaxCheese'),
	('TomatoSauce','TomatoSauce'),
	('ItalianSauce','ItalianSauce'),
}

TITLE_CHOICES = {
	('....','....'),
	('Mr','Mr'),
	('Mrs' , 'Mrs'),
	('Ms','Ms'),
}

special_occasion ={
	(1,'Yes'),(2,'No'),(3,'Maybe')
}
number_of_people = {
	(1,'1'),(2,'2'),(3,'3-5'),(4,'5-10'),(5,'More Than 10')
}
class_of_booking = {
	('Business','Business'),
	('Couples','Couples'),
	('Family','Family'),
	('Friends','Friends'),
	('Party','Party')
}

Mode_Choice = {(1,'CASH ON DELIVERY'),
				(2,'INTERNET BANKING'),
				(3,'DEBIT CARD'),
				}

sorted_class_of_booking = sorted(class_of_booking,key= lambda x:x[1])
sorted_number_of_people = sorted(number_of_people,key = lambda x:x[1])
sorted_special_occasion = sorted(special_occasion,key=lambda x:x[1])
sort_topping = sorted(Toppings, key=lambda x: x[1])
s = {
	(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),
}

Num = sorted(s, key=lambda x: x[1])

def get_upload_file_name(instance, filename):
	return "uploaded_files/%s_%s"%(str(time()).replace('.','_'),filename)	

class OrderSpecial(models.Model):
	Quantity = models.IntegerField()
	Select = models.CharField(max_length = 100,validators=[validate_recepie])
	Flavour = models.CharField(max_length = 100,validators=[validate_recepie])
	Toppings = models.CharField(max_length=100,validators=[validate_recepie])
	Describe = models.TextField(max_length=100,validators = [validate_describe])
	photo = models.ImageField(upload_to = 'order_pics/')
	
	def __unicode__(self):
		return "%s %s"%(self.photo)

class Payment_Process(models.Model):
	card_number = IntegerRangeField(min_value=15,max_value=16)
	name_in_card = models.CharField(max_length=100,validators=[validate_name])
	expiry_date = models.DateField()
	email_id = models.EmailField(blank=True)

class recepie(models.Model):
	recepie_name = models.CharField(max_length=15) 
	ingredients = models.TextField(max_length=200)
	reference = models.URLField(blank=True)
	emailid = models.EmailField()
	date = models.DateField()


	def __unicode__(self):
		return "%s"%(self.recepie_name)


	def save(self,*args,**kwargs):
		self.date = timezone.now()
		return super(recepie,self).save(*args,**kwargs)


class Contact_all(models.Model):
	name  = models.CharField(validators=[validate_name],max_length = 100) 
	email = models.EmailField()
	query = models.TextField(validators = [validate_len],max_length = 400)
	date = models.DateField(null=True)	

	def __unicode__(self):
		return "%s"%(self.name)

class order_table(models.Model):
	table_name = models.CharField(max_length=10,validators=[validate_name])
	booking_date = models.DateField()
	duration_booking_in_hours = models.PositiveIntegerField()
	class_of_booking = models.CharField(max_length=100)
	number_of_people = models.CharField(max_length=100)
	is_it_a_special_occasion = models.CharField(max_length=10)

	def __unicode__(self):
		return "%s"%(self.table_name)

class Mode(models.Model):
	mode_of_payement = models.CharField(max_length=100)

class Login(models.Model):
	username = models.CharField(max_length=10) 
	password = models.CharField(max_length=16)

class Signup(models.Model):
	firstname = models.CharField(max_length=10)
	lastname = models.CharField(max_length= 10)
	username = models.CharField(max_length=10) 
	password = models.CharField(max_length=16,validators=[validate_pass])
	confirm_password = models.CharField(max_length=16,validators=[validate_pass])
	emailid = models.EmailField()
	date = models.DateField(null = True)
	photo = models.ImageField(upload_to = get_upload_file_name,blank = True)
	
	def __unicode__(self):
		return "%s %s"%(self.username,self.photo)

class Profile(models.Model):
	email = models.EmailField(null=True)
	firstname = models.CharField(max_length=30,null=True)
	fullname = models.CharField(max_length=30,null=True)
	lastname = models.CharField(max_length=30,null=True)
	username = models.CharField(max_length=30,null=True)

class Comment(models.Model):
	name = models.CharField(max_length=30,validators=[validate_name])
	email = models.EmailField(blank = True)
	comment_new = models.TextField(max_length=250)
	date = models.DateField()
	parent = models.ForeignKey('self',null = True)
	photo = models.ImageField(upload_to = 'get_upload_file_name',blank = True)

	def save(self,*args,**kwargs):
		today = datetime.datetime.today()
		avail_user = Signup.objects.filter(username = self.name).exists()
		if avail_user:
			get_user = Signup.objects.get(username = self.name)
			self.photo = get_user.photo			
		self.date = '%d-%d-%d'%(today.year,today.month,today.day)		
		super(Comment,self).save(*args,**kwargs)
	
	def get_markdown(self):
		content = self.comment_new
		markdown_text = markdown(content)
		return mark_safe(markdown_text)	
	
	def children(self): #replies
		return Comment.objects.filter(parent=self)
	
	@property
	def is_parent(self):
		if self.parent is not None:
			return False
		return True

	#def save(self, *args, **kwargs):
	#	if self.photo:
	#		small = rescale_image(self.photo,width=100,height=100)
	#		self.image_small = SimpleUploadedFile(name,small_pic)			
	#	super(Signup, self).save(*args, **kwargs)		

class added_user(models.Model):
	order_name = models.CharField(max_length=100)
	quantity = IntegerRangeField()
	price = IntegerRangeField
