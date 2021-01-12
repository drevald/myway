import django
import hashlib
import unittest
import base64
import io
from django.test import Client
from django.test import TestCase
from django.test import TransactionTestCase
from django.template import RequestContext
from myway.core import views
from myway.core import models
from PIL import Image, ImageFilter

class SimpleTest(TransactionTestCase):

    reset_sequences = True

    def setUp(self):
        self.client = Client()

    def test_trips(self):
        response = self.client.get('/trips')
        self.assertEqual(response.status_code, 200)
        print(response.context['object_list'])
        print(len(response.context['object_list']))

    def test_add_trip(self):
        
        #trip creation            
        response = self.client.post("/trips/create", Pillowdata={"name": "Trip One"}, follow = True)
        self.assertEqual(response.status_code, 200) 

        #trip name change            
        response = self.client.post("/trips/1/edit", data={"name": "Trip One Edited"}, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Trip One Edited", list(response.context['object_list']).pop().name)

        #adding points to the trip
        response = self.client.post("/trips/1/points/add", data={"longitude":55, "latitude":37, "name":"Point 1"}, follow = True)        
        response = self.client.post("/trips/1/points/add", data={"longitude":55, "latitude":34, "name":"Point 2"}, follow = True)                
        response = self.client.post("/trips/1/points/add", data={"longitude":55, "latitude":31, "name":"Point 3"}, follow = True)                        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list(response.context['object'].points.all())), 3)

        #edit trip point
        response = self.client.post("/trips/1/points/1/edit", data={"longitude":56, "latitude":36, "name":"Point Edited"}, follow = True)        
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Point Edited", response.context['object'].points.get(id=1).name)

        #moving trip points
        response = self.client.get("/trips/1/points/2/up", follow = True)        
        self.assertEqual(response.status_code, 200)
        # print(list(response.context['object'].points.order.all()))
        response = self.client.get("/trips/1/points/1/down", follow = True)        
        self.assertEqual(response.status_code, 200)
        # print(list(response.context['object'].points.order.all()))

        #delete trip point
        response = self.client.post("/trips/1/points/3/delete", follow = True)
        self.assertEqual(len(list(response.context['object'].points.all())), 2)
        self.assertEqual(response.status_code, 200)

################################################################################################################

    def test_set_object_photo(self):

        print("TEST SET OBJECT PHOTO")

        #create object
        response = self.client.post("/objects/create", data={"name":"Object One", "longitude":56, "latitude":36},follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Object One", list(response.context['objects_list']).pop().name)

        #set object photo
        with open('myway/test/sample.jpg', "rb") as fp:            
            response = self.client.post(f'/object/1/photo/0', data = {"file": fp,"title":"title"}, follow = True)
        response = self.client.post(f'/object/1/photo/1', {"title":"title", "cancel":"cancel"}, follow = True)            
        self.assertEqual(response.context['object'].photo, None)
        response = self.client.post(f'/object/1/photo/1', {"title":"title", "save":"save"}, follow = True)            
        self.assertNotEqual(response.context['object'].photo, None)
        self.assertEqual(response.status_code, 200)

        #rotate photo
        photo = response.context['object'].photo
        img = Image.open(io.BytesIO(base64.b64decode(photo.thumbnail)))
        size_before = img.size
        response = self.client.get(f'/object/1/photo/1/rotate/90', follow = True)   
        response = self.client.post(f'/object/1/photo/1', {"title":"title", "save":"save"}, follow = True)              
        photo = response.context['object'].photo
        img = Image.open(io.BytesIO(base64.b64decode(photo.thumbnail)))
        size_after = img.size
        self.assertEqual(size_after[1], size_before[0])
        self.assertEqual(size_after[0], size_before[1])

################################################################################################################    
    
    def test_add_point_object(self):
        
        #trip creation            
        response = self.client.post("/trips/create", data={"name": "Trip One"}, follow = True)
        self.assertEqual(response.status_code, 200) 

        #trip name change            
        response = self.client.post("/trips/1/edit", data={"name": "Trip One Edited"}, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Trip One Edited", list(response.context['object_list']).pop().name)

        #adding points to the trip
        response = self.client.post("/trips/1/points/add", data={"longitude":55, "latitude":37, "name":"Point 1"}, follow = True)        
        response = self.client.post("/trips/1/points/add", data={"longitude":55, "latitude":34, "name":"Point 2"}, follow = True)                
        response = self.client.post("/trips/1/points/add", data={"longitude":55, "latitude":31, "name":"Point 3"}, follow = True)                        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list(response.context['object'].points.all())), 3)

        #creating objects
        response = self.client.post("/objects/create", data={"longitude":55, "latitude":37, "name":"Object 1"}, follow = True)        
        response = self.client.post("/objects/create", data={"longitude":55, "latitude":37, "name":"Object 2"}, follow = True)                       
        response = self.client.post("/objects/create", data={"longitude":55, "latitude":37, "name":"Object 3"}, follow = True)                               
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list(response.context['objects_list'])), 3)

        #assigning object to point
        response = self.client.get("/trips/1/points/1/objects/1/add", follow = True)
        self.assertEqual(response.status_code, 200)