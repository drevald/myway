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
        response = self.client.post("/trips/create", data={"name": "Trip One"}, follow = True)
        self.assertEqual(response.status_code, 200)
        trips = response.context['object_list']
        self.assertEqual(1, len(trips))
        trip = list(trips).pop()
        print(trip.id)
        
        # #3 points creation
        # response = self.client.post("/point/create", data={"longitude": 55.0, "latitude":37, "name":"noname"}, follow = True)
        # response = self.client.post("/point/create", data={"longitude": 55.0, "latitude":37, "name":"noname"}, follow = True)
        # response = self.client.post("/point/create", data={"longitude": 55.0, "latitude":37, "name":"noname"}, follow = True)
        # self.assertEqual(response.status_code, 200)
        # points = response.context['object_list']
        # self.assertEqual(3, len(points))
        # point = list(points).pop()
        # print(f"point.id={point.id} trip.id={trip.id}")

        #3 trip points creation
        # print("adding all 3 points to trip")
        # for point in points:
        #     response = self.client.post(f'/trips/{trip.id}/trip_point_add/{point.id}', follow = True)
        # trip_points = response.context['trip_points']
        # for trip_point in trip_points:
        #     print(f"id={trip_point.id} order={trip_point.order}")
        # self.assertEquals(models.TripPoint.objects.get(id = 1).order, 0)
        # self.assertEquals(models.TripPoint.objects.get(id = 2).order, 1)
        # self.assertEquals(models.TripPoint.objects.get(id = 3).order, 2)

        # #point down
        # print("moving down point with id = 2")
        # response = self.client.post(f'/trips/{trip.id}/trip_point_down/2', follow = True)
        # trip_points = response.context['trip_points']
        # for trip_point in trip_points:
        #     print(f"id={trip_point.id} order={trip_point.order}")          
        # self.assertEquals(models.TripPoint.objects.get(id = 2).order, 0)
        # self.assertEquals(models.TripPoint.objects.get(id = 1).order, 1)
        # self.assertEquals(models.TripPoint.objects.get(id = 3).order, 2)

        # #point up
        # print("moving up point with id = 2")
        # response = self.client.post(f'/trips/{trip.id}/trip_point_up/2', follow = True)
        # trip_points = response.context['trip_points']
        # for trip_point in trip_points:
        #     print(f"id={trip_point.id} order={trip_point.order}")                 
        # self.assertEquals(models.TripPoint.objects.get(id = 1).order, 0)
        # self.assertEquals(models.TripPoint.objects.get(id = 2).order, 1)
        # self.assertEquals(models.TripPoint.objects.get(id = 3).order, 2)

        # #point deletion
        # print("deleting point with id = 2")
        # response = self.client.post(f'/trips/{trip.id}/trip_point_delete/2', follow = True)
        # trip_points = response.context['trip_points']
        # self.assertEquals(len(trip_points), 2)
        # for trip_point in trip_points:
        #     print(f"id={trip_point.id} order={trip_point.order}")
        # self.assertEquals(len(list(models.TripPoint.objects.filter(trip = models.Trip.objects.get(id=trip.id)))), 2)
        # self.assertEquals(models.TripPoint.objects.get(id = 1).order, 0)
        # self.assertEquals(models.TripPoint.objects.get(id = 3).order, 1)

    def test_object_picture(self):

        reset_sequences = True
        #adding show object
        print("adding sample object")
        response = self.client.post(f'/object/create', data={"name":"Object one", "longitude":55, "latitude":37}, follow = True)
        self.assertEqual(response.status_code, 200)
        object = list(response.context['objects_list']).pop()
        self.assertTrue(object.photo is None)

        file = open('thumbnail.jpg', "rb")
        image_data = base64.b64encode(file.read()).decode('utf-8')    
        photo = models.Photo(id=1, thumbnail=image_data)
        photo.save()

        file = open('thumbnail.jpg', "rb")
        image_data = base64.b64encode(file.read()).decode('utf-8')    
        photo_new = models.Photo(id=2, thumbnail=image_data)
        photo_new.save()

        print("adding photo to the object")
        with open('thumbnail.jpg', "rb") as fp:            
            response = self.client.post(f'/object/{object.id}/photo/1', {"file": fp,"title":"title", "save":"Save"}, follow = True)
        updated_object = models.ShowObject.objects.get(id = object.id)
        self.assertTrue(updated_object.photo is not None)

        print("reject to add photo to the object")
        with open('thumbnail.jpg', "rb") as fp:            
            response = self.client.post(f'/object/{object.id}/photo/2', {"file": fp,"title":"title", "cancel":"Cancel"}, follow = True)
        updated_object = models.ShowObject.objects.get(id = object.id)
        self.assertEqual(updated_object.photo.id, 1)

        print("add photo to the object")
        with open('thumbnail.jpg', "rb") as fp:            
            response = self.client.post(f'/object/{object.id}/photo/2', {"file": fp,"title":"title", "save":"Save"}, follow = True)
        updated_object = models.ShowObject.objects.get(id = object.id)
        self.assertEqual(updated_object.photo.id, 2)

class ImageTest(TestCase):
 
    def test_image_conversion(self):

        #test_image_to_db
        file = open('thumbnail.jpg', "rb")
        image_data = base64.b64encode(file.read()).decode('utf-8')    
        stored_data = models.Photo(id=1, thumbnail=image_data)
        stored_data.save()
        retrieved_data = models.Photo.objects.get(id=1)
        retrieved_data.thumbnail
        print(type(retrieved_data.thumbnail))
        print(type(image_data))
        print(retrieved_data.thumbnail[0:10])
        print(image_data[0:10])
        assert(retrieved_data.thumbnail == image_data)
    
        #test_db_to_image
        retrieved_data = models.Photo.objects.get(id=1).thumbnail
        print(retrieved_data[0:10])
        image_arr = base64.b64decode(retrieved_data)
        print(image_arr[0:10])
        in_memory_file = io.BytesIO(image_arr)
        img = Image.open(in_memory_file)

    def test_image_rotation(self):        
        image = Image.open('thumbnail.jpg')
        rotated_image = image.rotate(-90, expand=1)
        assert(image.width == rotated_image.height)
        assert(image.height == rotated_image.width)



