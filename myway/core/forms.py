from django import forms
from . import models

class TripForm (forms.ModelForm):    
    name = forms.CharField();
    class Meta:
        model = models.Trip
        fields = ['name']

class PhotoForm (forms.ModelForm):    
    class Meta:
        model = models.Photo
        fields = '__all__'

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()