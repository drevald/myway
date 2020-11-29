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
    title = forms.CharField(max_length = 50)
    # file = forms.FileField(widget=forms.FileInput(attrs={
    #     'onchange': 'name=this.value;this.form["title"].value = value.substring(1 + value.lastIndexOf("\\\\"), value.lenght)'
    #     }))
    #file = forms.FileField()
    file = forms.FileField(widget=forms.FileInput(attrs={'onchange':'var name=this.value;this.form["title"].value = value.substring(1 + value.lastIndexOf("\\\\"), value.lenght)'}))
    