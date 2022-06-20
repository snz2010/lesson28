from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import DetailView
from django.views import View
from ads.models import Category, Ad
import json
import pandas as pandas


# стартовая страница
class IndexView(View):
    def get(self, request, *args, **kwargs):
        responce = {"status": "ok"}
        return JsonResponse(responce, safe=False, json_dumps_params={"ensure_ascii": False})


# просмотр/добавление объявления
@method_decorator(csrf_exempt, name='dispatch')  # @csrf_exempt
class AdSimpleView(View):  # def index(request):
    def get(self, request):  # if request.method == "GET":
        ads = Ad.objects.all()
        # search_text = request.GET.get["text",None]
        # if search_text:
        #     ads = ads.filter(name=search_text ) # поиск по имени!
        responce = []
        for ad in ads:
            responce.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
            })
        return JsonResponse(responce, safe=False, json_dumps_params={"ensure_ascii": False})

    def post(self, request):  # if request.method == "POST":
        ad_data = json.loads(request.body)
        ad = Ad.objects.create(
            name=ad_data["name"],
            author=ad_data["author"],
            price=ad_data["price"],
            description=ad_data["description"],
            address=ad_data["address"],
            is_published=ad_data["is_published"],
        )
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        })


# детальный просмотр объявления
class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse(({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        }), safe=False, json_dumps_params={"ensure_ascii": False})


# просмотр/добавление категории
@method_decorator(csrf_exempt, name='dispatch')
class CatSimpleView(View):
    def get(self, request):
        cats = Category.objects.all()
        responce = []
        for cat in cats:
            responce.append({
                "name": cat.name,
            })
        return JsonResponse(responce, safe=False, json_dumps_params={"ensure_ascii": False})

    def post(self, request):
        add_data = json.loads(request.body)
        cat = Category.objects.create(
            name=add_data["name"],
        )
        return JsonResponse({
            "id": cat.id,
            "name": cat.name,
        })


# детальный просмотр категории
class CatDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse(({
            "id": cat.id,
            "name": cat.name,
        }), safe=False, json_dumps_params={"ensure_ascii": False})


# заполнение таблицы категорий, используя данные из файла
class AddToCat(View):
    def get(self, request):
        csv_data = pandas.read_csv('ads/data/categories.csv', sep=",").to_dict()
        i = 0
        while max(csv_data['id'].keys()) >= i:
            Category.objects.create(
                name=csv_data["name"][i],
            )
            i += 1
        return JsonResponse("Add to Table Category - Ok", safe=False, status=200)


# заполнение таблицы объявлений, используя данные из файла
class AddToAd(View):
    def get(self, request):
        csv_data = pandas.read_csv('ads/data/ads.csv', sep=",").to_dict()
        i = 0
        while max(csv_data['Id'].keys()) >= i:
            Ad.objects.create(
                name=csv_data["name"][i],
                author=csv_data["author"][i],
                price=csv_data["price"][i],
                description=csv_data["description"][i],
                address=csv_data["address"][i],
                is_published=csv_data["is_published"][i],
            )
            i += 1
        return JsonResponse("Add to Table Ad - Ok", safe=False, status=200)