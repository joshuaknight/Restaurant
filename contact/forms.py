from django import forms 
from django.forms import ModelForm,Textarea
import re 
from django.utils.translation import ugettext_lazy as _
from contact.models import *

class Contact(ModelForm):
    class Meta:
        model = Contact_all
        fields = ('title','name','email','query')
        widgets = {
            'query': Textarea(attrs={'cols': 50, 'rows': 10}),
        	'title': forms.Select(choices = TITLE_CHOICES),
        	}
       	help_texts = {
          'title' : _('select a proper title'),
       		'query' : _('Please Be Brief about your Query'),
       		'name'  : _('Name should be valid'),
       		'email' : _('The way to contact you back'),
       	}

	
