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
    title = forms.CharField(max_length = 50, initial='title')
    file = forms.FileField(required=False, widget=forms.FileInput(attrs={'onchange':'preview(this.form)'}))
    
class ObjectForm(forms.ModelForm):
    longitude = forms.FloatField(widget=forms.HiddenInput())
    latitude = forms.FloatField(widget=forms.HiddenInput())
    name = forms.TextInput()
    class Meta:
        model = models.ShowObject
        fields = ['name','longitude','latitude']