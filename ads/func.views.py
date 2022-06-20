from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import DetailView
from django.views import View
from ads.models import Category, Ad
import json


#@method_decorator(csrf_exempt, name='dispatch')
@csrf_exempt
def index(request):
    if request.method == "GET":
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
    if request.method == "POST":
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


def index1(request, ad_id):
    if request.method == "GET":
        ad = Ad.objects.get(pk=ad_id)
        return JsonResponse(({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
        }), safe=False, json_dumps_params={"ensure_ascii": False})


class AdDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        }, safe=False, json_dumps_params={"ensure_ascii": False})


class SimpleView1(DetailView):
    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse(200, {"status": "ok"})
