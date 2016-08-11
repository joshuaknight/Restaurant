from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from .models import Profile

def save_profile(stratergy,user=None, *args, **kwargs):
	if user is None:
		profile = Profile()
		profile.email = strategy.session_get('email')
		profile.firstname = response.get('first_name')
		profile.fullname = response.get('fullname')		
		profile.lastname = response.get('last_name')		
		profile.username = response.get('username')		
		profile.save()
