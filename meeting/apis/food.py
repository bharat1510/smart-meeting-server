from django.shortcuts import render, redirect

from meeting.models import *
from meeting.helpers.customResponse import Custom
from meeting.helpers.constant import Constant
from meeting.helpers.serializer import *

# from django.contrib.sessions.models import Session
   
from datetime import timedelta
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework import status

from django.contrib.auth.models import User,auth
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model
User = get_user_model()

@api_view(['POST',])
def addMyFoodItem(request):
    # Add New Food Category
    itemName = request.POST['name']
    itemCuisine = request.POST['foodCuisine']
    itemType = request.POST['foodType']

    if Food.objects.filter(name=itemName,foodCuisine_id=itemCuisine,foodType_id=itemType):
        cuisineName = FoodCuisine.objects.get(id=itemCuisine).name
        typeName = FoodType.objects.get(id=itemType).type
        return Custom.errorResponse([], Constant.varError, status.HTTP_400_BAD_REQUEST, "Food item {} with cuisine {} and type {} already exists".format(itemName, cuisineName, typeName))

    foodSerializerData = FoodSerializer(data=request.data)

    if foodSerializerData.is_valid():
        foodSerializerData.save()
        return Custom.dataResponse(foodSerializerData.data, Constant.varSuccess, status.HTTP_201_CREATED, "Food item {} Added Successfully.".format(itemName))

    return Custom.errorResponse(foodSerializerData.errors, Constant.varError, status.HTTP_400_BAD_REQUEST, "Something wents wrong.")

@api_view(['GET','PUT','DELETE'])
def getMyFoodItem(request, pk):
    try:
        userData = User.objects.get(id=request.user.id)
        restaurantId = userData.restaurants.id
    except:
        return Custom.errorResponse([], Constant.varError, status.HTTP_404_NOT_FOUND, "Cannot find restaurant with requested user.")
    
    try:
        foodData = Food.objects.get(id=pk)
    except:
        return Custom.errorResponse([], Constant.varError, status.HTTP_404_NOT_FOUND, "Cannot find food item with given details.")

    if not restaurantId == foodData.restaurants_id:
        return Custom.errorResponse([], Constant.varError, status.HTTP_403_FORBIDDEN, "Access Denied! You're trying to access authorized data.")

    if request.method == 'GET':
        foodSerializerData = FoodSerializer(foodData)
        return Custom.dataResponse(foodSerializerData.data, Constant.varSuccess, status.HTTP_200_OK, "Record found.")

    elif request.method == 'PUT':
        itemName = request.data['name']
        itemCuisine = request.data['foodCuisine']
        itemType = request.data['foodType']
        if not (itemName == foodData.name and itemCuisine == foodData.foodCuisine_id and itemType == foodData.foodType_id):
            if Food.objects.filter(name=itemName,foodCuisine_id=itemCuisine,foodType_id=itemType):
                cuisineName = FoodCuisine.objects.get(id=itemCuisine).name
                typeName = FoodType.objects.get(id=itemType).type
                return Custom.errorResponse([], Constant.varError, status.HTTP_400_BAD_REQUEST, "Food item {} with cuisine {} and type {} already exists".format(itemName, cuisineName, typeName))

        foodSerializerData = FoodSerializer(foodData, data=request.data)
        if foodSerializerData.is_valid():
            foodSerializerData.save()
            return Custom.dataResponse(foodSerializerData.data, Constant.varSuccess, status.HTTP_200_OK, "Food item {} updated Successfully.".format(itemName))
        return Custom.errorResponse(foodSerializerData.errors, Constant.varError, status.HTTP_400_BAD_REQUEST, "Something wents wrong.")

    elif request.method == 'DELETE':
        itemName = foodData.name
        foodData.delete()
        return Custom.successResponse([], Constant.varSuccess, status.HTTP_200_OK, "Food item {} deleted successfully.".format(itemName))


@api_view(['GET','DELETE'])
def getMyFoodItems(request):
    try:
        userData = User.objects.get(id=request.user.id)
        restaurantId = userData.restaurants.id
    except:
        return Custom.errorResponse([], Constant.varError, status.HTTP_404_NOT_FOUND, "Cannot find restaurant with requested user.")

    foodData = Food.objects.filter(restaurants_id=restaurantId)
    if request.method == 'GET':
        foodSerializerData = FoodSerializer(foodData, many=True)
        return Custom.dataResponse(foodSerializerData.data, Constant.varSuccess, status.HTTP_200_OK, "Record found.")
    elif request.method == 'DELETE':
        foodData.delete()
        return Custom.successResponse([], Constant.varSuccess, status.HTTP_200_OK, "All food items deleted successfully.")
    
    
