from django.contrib import admin
from .models import *

model_list = [OrderSpecial,
				Payment_Process,
				recepie,
				Contact_all,
				order_table,
				Mode,
				Login,
				Signup,
				Profile,
				Comment,
				added_user,]

for i in model_list:				
	admin.site.register(i)