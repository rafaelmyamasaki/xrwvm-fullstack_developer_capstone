# Uncomment the required imports before adding the code
from .models import CarMake, CarModel
from .populate import initiate
from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request

from django.views.decorators.http import require_POST


# Função para login
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            # Autenticar o usuário
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                return JsonResponse({"status": "Error", "message": "Invalid credentials"}, status=401)
        except Exception as e:
            return JsonResponse({"status": "Error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "Error", "message": "Invalid request method"}, status=400)

# Função para logout
@require_POST
@csrf_exempt
def logout_request(request):
    try:
        logout(request)
        return JsonResponse({"userName": "", "status": "Logged out"})
    except Exception as e:
        return JsonResponse({"status": "Error", "message": str(e)}, status=500)
# ...

# Create a `registration` view to handle sign up request
# @csrf_exempt
@csrf_exempt
def registration(request):
    context = {}

    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

def get_cars(request):
    # Conta quantos objetos CarMake existem no banco de dados
    count = CarMake.objects.count()
    print(f"Number of CarMake objects: {count}")  # Debugging: imprime o número de objetos

    # Se não houver nenhum CarMake, chama a função initiate para popular o banco de dados
    if count == 0:
        initiate()

    # Obtém todos os objetos CarModel com relacionamento pre-carregado para CarMake
    car_models = CarModel.objects.select_related('car_make')

    # Cria uma lista de dicionários contendo os nomes dos modelos e suas marcas associadas
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    # Retorna os dados como uma resposta JSON
    return JsonResponse({"CarModels": cars})
# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):


# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration` view to handle sign up request
# @csrf_exempt
# def registration(request):
# ...

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
