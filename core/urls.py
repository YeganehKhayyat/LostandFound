"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from core.views import (
                        create_item,
                        list_items,
                        item_detail,
                        update_item,
                        delete_item,
                        change_status
                        )


urlpatterns = [
    path("create/" ,create_item , name = 'create_item'),
    path("list/" ,list_items , name='list_item'),
    path("<int:pk>/" , item_detail , name = 'item_detail'),
    path("<int:pk>/edit/" ,update_item , name='update_item' ),
    path("<int:pk>/delete/" , delete_item, name= 'delete_item'),
    path("<int:pk>/change_status/" , change_status , name="change_status_item")
]
