from django import forms
from . import models
from .models import Comment
from django.forms import ModelForm

# Form for creating new advertisement
class advertisementForm(forms.ModelForm):
    class Meta:
        model= models.advertisements
        fields=['place','address','bedroom','bathroom','rent','size','number',]

# Form for editing advertisement
class advertisementEditForm(forms.ModelForm):
    class Meta:
        model= models.advertisements
        fields=['place','address','bedroom','bathroom','rent','size','number',]        

# Form for comment section in particular advertisement
class commentForm(forms.ModelForm):


	content = forms.CharField(label="" , widget = forms.Textarea(attrs={'class': 'form-control' , 'placeholder': 'text goes here' , 'rows':'2' , 'cols': '60'}))

	class Meta:

		model = Comment
		fields = ('content',)

       


     