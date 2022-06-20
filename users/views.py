import json
import pandas as pandas
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from users.models import User, Location

################################################################################
# заполнение таблицы локаций, используя данные из файла
class AddToLo(View):
    def get(self, request):
        csv_data = pandas.read_csv('users/data/location.csv', sep=",").to_dict()
        i = 0
        while max(csv_data['id'].keys()) >= i:
            Location.objects.create(
                name=csv_data["name"][i],
                lat=csv_data["lat"][i],
                lng=csv_data["lng"][i],
            )
            i += 1
        return JsonResponse("Add to table Location - Ok", safe=False, status=200)


################################################################################
# заполнение таблицы локаций, используя данные из файла
class AddToUsr(CreateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "locations"]
    def get(self, request):
        csv_data = pandas.read_csv('users/data/user.csv', sep=",").to_dict()
        i = 0
        while max(csv_data['id'].keys()) >= i:
            try:
                location_obj = Location.objects.get(id=csv_data["location_id"][i])
            except Location.DoesNotExist:
                return JsonResponse("Локация не найдена!", status=404)

            print("***")
            print(dir(location_obj))
            print("***")
            new_u = User.objects.create(
                first_name=csv_data["first_name"][i],
                last_name=csv_data["last_name"][i],
                username=csv_data["username"][i],
                password=csv_data["password"][i],
                role=csv_data["role"][i],
                age=csv_data["age"][i],
            )
            new_u.locations.add(location_obj)
            i += 1
        return JsonResponse("Add to table User - Ok", safe=False, status=200)


# посмотр всех пользователей
class UserView(ListView):
    models = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.annotate(total_ads=Count('ad'))

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "total_ads": user.total_ads,
                "location": list(map(str, user.locations.all())),
            })
        responce = {
            "items": users,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count,
        }
        return JsonResponse(responce, safe=False, json_dumps_params={"ensure_ascii": False})


# детальный просмотр
class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse(({
            "id": ad.id,
            "username": ad.username,
            "first_name": ad.first_name,
            "last_name": ad.last_name,
            "role": ad.role,
            "age": ad.age,
            "location": list(map(str, ad.locations.all())),
        }), safe=False, json_dumps_params={"ensure_ascii": False})


# создание
@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ["username", "password", "first_name", "last_name", "role", "age", "locations"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            username=user_data["username"],
            password=user_data["password"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            role=user_data["role"],
            age=user_data["age"],
        )
        for location_name in user_data["locations"]:
            location, _ = Location.objects.get_or_create(name=location_name)
            user.locations.add(location)

        return JsonResponse(({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "location": list(map(str, user.locations.all())),
        }), safe=False, json_dumps_params={"ensure_ascii": False})


# обновление
@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ["username", "password", "first_name", "last_name", "role", "age", "locations"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        self.object.username=user_data["username"]
        self.object.password=user_data["password"]
        self.object.first_name=user_data["first_name"]
        self.object.last_name=user_data["last_name"]
        self.object.role=user_data["role"]
        self.object.age=user_data["age"]

        for location_name in user_data["locations"]:
            location, _ = Location.objects.get_or_create(name=location_name)
            self.object.locations.add(location)

        self.object.save()
        return JsonResponse(({
            "id": self.object.id,
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "age": self.object.age,
            "location": list(map(str, self.object.locations.all())),
        }), safe=False, json_dumps_params={"ensure_ascii": False})


# удаление
@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({
            "Удаление из Users": "успешно",
        }, json_dumps_params={"ensure_ascii": False}, status=200)


