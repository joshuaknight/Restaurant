from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from .models import *

def save_profile(user,response,*args, **kwargs):	
    username = kwargs['details']['username']
    first_name = kwargs['details']['first_name']
    last_name = kwargs['details']['last_name']
    email = kwargs['details']['email']    
    if Signup.objects.filter(username=username).exists():
        pass
    else:
        new_profile = Profile(username = username,
        	firstname = first_name,
        	lastname =last_name,email = email)        
        new_profile.save()
        
        new_signup = Signup(username=username,
        		firstname = first_name,lastname = last_name ,emailid = email)
        new_signup.save()
    return kwargs

    