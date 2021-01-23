"""learn_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from app import view




urlpatterns = [
    path('login/', view.login),
    path('management/', view.management),

    path('classes/',view.classes),
    path('add_class/',view.add_class),
    path('del_class/', view.del_class),
    path('edit_class/', view.edit_class),

    path('teacher/', view.teacher),

    path('student/', view.student),
    path('add_student/', view.add_student),
    path('del_student/', view.del_student),
    path('edit_student/', view.edit_student),

    path('modal_add_class/', view.modal_add_class),
    path('modal_edit_class/', view.modal_edit_class),
    path('modal_del_class/', view.modal_del_class),

    path('modal_add_student/', view.modal_add_student),
    path('modal_edit_student/', view.modal_edit_student),
    path('modal_del_student/', view.modal_del_student),

    path('add_teacher/', view.add_teacher),
    path('edit_teacher/', view.edit_teacher),
    path('del_teacher/', view.del_teacher),

    path('modal_add_teacher/', view.modal_add_teacher),
    path('modal_edit_teacher/', view.modal_edit_teacher),
    path('modal_del_teacher/', view.modal_del_teacher),

    path('get_class_list/', view.get_class_list),
    path('get_teacher2class_list/', view.get_teacher2class_list),

    path('admin/', admin.site.urls),
]
