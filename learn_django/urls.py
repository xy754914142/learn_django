"""learn_django URL Configuration

The `urlpatterns` list routes URLs to viewss. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function viewss
    1. Add an import:  from my_app import viewss
    2. Add a URL to urlpatterns:  path('', viewss.home, name='home')
Class-based viewss
    1. Add an import:  from other_app.viewss import Home
    2. Add a URL to urlpatterns:  path('', Home.as_views(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from app01 import views




urlpatterns = [

    path('login.html', views.Login.as_view(), name='login'),
    path('management.html', views.management,name='mian_html'),

    path('classes.html',views.classes,name='classes'),
    path('add_class/',views.add_class,name='add_class'),
    path('del_class/<int:nid>/', views.del_class, name='del_class'),
    path('edit_class/<int:nid>/', views.edit_class, name='edit_class'),

    path('teacher/', views.teacher),

    path('student/', views.student),
    path('add_student/', views.add_student),
    path('del_student/', views.del_student),
    path('edit_student/', views.edit_student),

    path('modal_add_class/', views.modal_add_class),
    path('modal_edit_class/', views.modal_edit_class),
    path('modal_del_class/', views.modal_del_class),

    path('modal_add_student/', views.modal_add_student),
    path('modal_edit_student/', views.modal_edit_student),
    path('modal_del_student/', views.modal_del_student),

    path('add_teacher/', views.add_teacher),
    path('edit_teacher/', views.edit_teacher),
    path('del_teacher/', views.del_teacher),

    path('modal_add_teacher/', views.modal_add_teacher),
    path('modal_edit_teacher/', views.modal_edit_teacher),
    path('modal_del_teacher/', views.modal_del_teacher),

    path('get_class_list/', views.get_class_list),
    path('get_teacher2class_list/', views.get_teacher2class_list),

    path('logout/', views.logout),



    path('admin/', admin.site.urls),
]
