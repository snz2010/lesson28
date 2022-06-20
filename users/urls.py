from django.urls import path
from .views import UserView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView, AddToLo, AddToUsr

urlpatterns = [
    path('', UserView.as_view(),name='user_index_url'),
    path('<int:pk>/', UserDetailView.as_view(),name='user_detail_url'),
    path('create/', UserCreateView.as_view(),name='user_create_url'),
    path('<int:pk>/update/', UserUpdateView.as_view(),name='user_update_url'),
    path('<int:pk>/delete/', UserDeleteView.as_view(),name='user_delete_url'),
    path('addlo/', AddToLo.as_view(),name='location_add_url'),
    path('addusr/', AddToUsr.as_view(),name='users_add_url'), # пока не работает?
]
