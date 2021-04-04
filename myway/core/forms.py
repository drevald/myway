from django import forms
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Field, Div, Column, Row, Button

class TripForm (forms.ModelForm):    
    name = forms.CharField()
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
    address = forms.TextInput()
    helper = FormHelper()
    helper.layout = Layout(
        Row(
            Column(HTML('<img src="data:image/jpg;base64,{{ image }}"/>'), 'name', 'address', 'status', 'style',         
            Submit('submit', 'Save'), Button('button', 'Cancel'), css_class='col', style='vertical-align:top; background-color: green;'),
            Column('description', css_class='col', style='vertical-align:top; background-color: coral;')
        )
    )

    # helper.layout = Layout(
    #     Div(
    #         Div('longitude', wrapper_class='col'),
    #         Div('latitude', wrapper_class='col'),  
    #         Div('name', wrapper_class='col'),
    #         Div('address', wrapper_class='col')),
    #     Div(
    #         Field('description', wrapper_class='col')
    #     )
    # )
    class Meta:
        model = models.ShowObject
        fields = ['name','address', 'last_version_date', 'status', 'style', 'longitude','latitude', 'description']

class TripPointForm(forms.ModelForm):
    longitude = forms.FloatField(widget=forms.HiddenInput())
    latitude = forms.FloatField(widget=forms.HiddenInput())
    name = forms.TextInput()
    class Meta:
        model = models.TripPoint
        fields = ['name','longitude','latitude']        

class PersonForm(forms.ModelForm):
    birth_date = forms.DateField(input_formats=['%Y-%m-%d','%Y'])
    death_date = forms.DateField(required=False, input_formats=['%Y-%m-%d','%Y'])
    photo = forms.FileField(required=False, widget=forms.FileInput())
    class Meta:
        model = models.Person
        fields = '__all__'              

# ['%Y-%m-%d',      # '2006-10-25'
# '%m/%d/%Y',       # '10/25/2006'
# '%m/%d/%y']   