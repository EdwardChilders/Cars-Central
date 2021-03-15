from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    # renders
    path('', views.index),
    path('new_user', views.new_user),
    path('homepage', views.homepage),
    path('cars', views.cars),
    path('sell_car', views.sell_car),
    path('edit_car/<int:c_id>', views.edit_car),
    # path('parts', views.parts),
    # path('advice', views.advice),

    # redirects
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('post_car', views.post_car),
    path('update_car/<int:c_id>', views.update_car),
    path('destroy_car/<int:c_id>', views.destroy_car),
    path('message_car_owner/<int:c_id>', views.message_car_owner),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
