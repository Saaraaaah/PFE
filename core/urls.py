from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.index, name='index'),
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('get-less-rout/',views.get_less_rout,name='get-less-rout'),
    path('logout/',views.LogoutPage,name='logout'),
    path('signup/',views.testfunc,name='signup'),
    path('search/',views.api_view,name='search'),

]
