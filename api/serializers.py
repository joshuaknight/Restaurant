from rest_framework import *
from restaurant.models import *

class commentserializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'

class listserializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name = 'detail',
			#look_field = '',
		)
	delete_url = serializers.HyperlinkedIdentityField(
			view_name = 'delete',
			#look_field = '',
		)
	update_url = serializers.HyperlinkedIdentityField(
			view_name = 'update',
			#look_field = '',
		)
	photo = serializers.SerializerMethodField()
	html = serializers.SerializerMethodField()
	def get_photo(self, obj):
		try:
			photo = obj.photo.url 
		except:
			photo = None
		return photo
			
	class Meta:
		model = Comment
		fields = ['url',
				'name',
				'date',
				'photo',
				'delete_url',
				'update_url',
				'html',]

	def get_html(self,obj):
		return obj.get_markdown()	
