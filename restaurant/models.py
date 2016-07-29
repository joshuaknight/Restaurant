from django.db import models 
import re
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

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
	(1,'Onion'),
	(2,'Cheese'),
	(3,'MaxCheese'),
	(4,'TomatoSauce'),
	(5,'ItalianSauce'),
}
s = {
	(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),
}
sort_topping = sorted(Toppings, key=lambda x: x[1])
Num = sorted(s, key=lambda x: x[1])

class OrderSpecial(models.Model):
	Quantity = models.IntegerField()
	Select = models.CharField(max_length = 100)
	Flavour = models.CharField(max_length = 100)
	Toppings = models.CharField(max_length=100)
	Describe = models.TextField(max_length=100,validators = [validate_describe])

class Payment_Process(models.Model):
	card_number = IntegerRangeField(min_value=15,max_value=16)
	name_in_card = models.CharField(max_length=100,validators=[validate_name])
	expiry_date = models.DateField()
	email_id = models.EmailField(blank=True)

