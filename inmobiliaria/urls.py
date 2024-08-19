from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index , name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('update_account/', views.update_account, name='update_account'),
    path('profile/', views.profile, name='perfil'),
    path('add_property/', views.add_property, name='add_property'),
    path('get_comunas/<int:region_id>/', views.get_comunas, name='get_comunas'),
    path('property/edit/<int:property_id>/', views.edit_property, name='edit_property'),
    path('property/delete/<int:property_id>/', views.delete_property, name='delete_property'),

]