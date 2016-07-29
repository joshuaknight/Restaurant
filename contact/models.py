from django.db import models
from django.core import validators 
from django.core.exceptions import *
import re
def validate_name(value,length=5):
	regex = r"([a-zA-Z]+)"
	if not re.search(regex,value) or len(str(value)) < length:
		raise ValidationError("Not a Valid Name")

def validate_len(value,length=20):
	regex = r"([a-zA-Z]+)"
	if not re.search(regex,value) or len(str(value)) < length:
		raise ValidationError(u"Not Valid Be More Specific")
		
TITLE_CHOICES = {
	('....','....'),
	('Mr','Mr'),
	('Mrs' , 'Mrs'),
	('Ms','Ms'),
}
class Contact_all(models.Model):
	name  = models.CharField(validators=[validate_name],max_length = 100) 
	title = models.CharField(max_length=3)
	email = models.EmailField()
	query = models.CharField(validators = [validate_len],max_length = 400)
	date = models.DateField(null=True)