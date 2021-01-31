from django.shortcuts import render, redirect, HttpResponse, reverse
from django.views import View
from app01 import models
from functools import wraps
import json
from django.utils.decorators import method_decorator
from utils.pager import PageInfo
from utils.connte_mysql import *


def check_login(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        ret = request.get_signed_cookie('liu', default='0', salt='abc')
        if ret == 'fenglin':
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    return inner


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        userinfo = models.Userdate.objects.filter(username=user).first()

        if userinfo == None:
            return redirect(reverse('login'))
        print(userinfo.username, userinfo.password)
        if userinfo.password == pwd:
            cook = redirect(reverse('mian_html'))
            cook.set_signed_cookie('liu', 'fenglin', salt='abc', max_age=10000)
            return cook
        else:
            return redirect(reverse('login'))


@check_login
def management(request):
    return render(request, 'management.html')


@check_login
def classes(request, page):
    # class_list = mysql_result('select id,class_name from class')
    # page = request.GET.get('page')
    page_info = PageInfo(page, models.Classes.objects.all().count(), 10, '/classes/', 11)

    class_list = models.Classes.objects.all()[page_info.start():page_info.end()]

    return render(request, 'classes.html', {"classes_list": class_list, 'page_info': page_info})


@method_decorator(check_login, name='dispatch')
class Add_class(View):
    def get(self, request):
        return render(request, 'add_class.html')

    def post(self, request):
        c_name = request.POST.get('class_name')
        add_c = models.Classes(class_name=c_name)
        add_c.save()
        return redirect(reverse('classes', kwargs={'page': 1}))


@check_login
def del_class(request, nid):
    models.Classes.objects.get(id=nid).delete()
    return redirect(reverse('classes', kwargs={'page': 1}))


@method_decorator(check_login, name='dispatch')
class Edit_class(View):
    def get(self, request, nid):
        class_list = models.Classes.objects.get(id=nid)
        return render(request, 'edit_class.html', {'nid': nid, 'class_list': class_list})

    def post(self, request, nid):
        class_name = request.POST.get('title')
        models.Classes.objects.filter(id=nid).update(class_name=class_name)
        return redirect(reverse('classes', kwargs={'page': 1}))


@check_login
def student(request, page):
    page_info = PageInfo(page, models.Student.objects.all().count(), 10, '/student/', 11)
    student_list = models.Student.objects.all()[page_info.start():page_info.end()]
    class_list = models.Classes.objects.all()
    return render(request, 'student.html',
                  {'student_list': student_list, 'class_list': class_list, 'page_info': page_info})


@method_decorator(check_login, name='dispatch')
class Add_student(View):
    def get(self, request):
        class_list = models.Classes.objects.all()
        return render(request, 'add_student.html', {'class_list': class_list})

    def post(self, request):
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        models.Student.objects.create(stu_name=name, classes_id=class_id)
        return redirect(reverse('student', kwargs={'page': 1}))


@check_login
def del_student(request):
    nid = request.GET.get('nid')
    mysql_commit('delete from student where id=%s', [nid, ])
    return redirect(reverse('student', kwargs={'page': 1}))


@method_decorator(check_login, name='dispatch')
class Edit_student(View):
    def get(self, request, nid):
        student_data = mysql_fetchone(
            'select student.id,student.stu_name,class.class_name from student left join class on student.class_id = class.id where student.id = %s',
            [nid, ])
        class_list = mysql_result('select * from class')
        return render(request, 'edit_student.html', {'student_data': student_data, 'class_list': class_list})

    def post(self, request, nid):
        stu_name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        mysql_commit('update student set stu_name=%s,class_id=%s where id=%s', [stu_name, class_id, nid, ])
        return redirect(reverse('student'))


@check_login
def modal_add_class(request):
    ret = {'status': True, 'message': None}
    message_erro = "处理erro"
    try:
        class_name = request.POST.get('class_name')
        if len(class_name) > 0:
            add_c = models.Classes(class_name=class_name)
            add_c.save()
        else:
            message_erro = "班级名不能为空"
            raise Exception()
    except Exception as e:
        ret['status'] = False
        ret['message'] = message_erro

    return HttpResponse(json.dumps(ret))


@check_login
def modal_edit_class(request):
    ret = {'status': True, 'message': None}
    message_erro = "处理erro"
    try:
        class_name = request.POST.get('class_name')
        nid = request.POST.get('nid')
        if len(class_name) > 0:
            models.Classes.objects.filter(id=nid).update(class_name=class_name)
        else:
            message_erro = "班级名不能为空"
            raise Exception()
    except Exception as e:
        ret['status'] = False
        ret['message'] = message_erro

    return HttpResponse(json.dumps(ret))


@check_login
def modal_del_class(request):
    ret = {'status': True, 'message': None}
    message_erro = "处理erro"
    try:
        nid = request.POST.get('nid')
        models.Classes.objects.filter(pk=nid).delete()
    except Exception as e:
        ret['status'] = False
        ret['message'] = message_erro

    return HttpResponse(json.dumps(ret))


@check_login
def modal_add_student(request):
    ret = {"status": True, 'message': None}
    message_erro = "处理erro"
    try:
        stu_name = request.POST.get('stu_name')
        class_id = request.POST.get('class_id')
        if len(stu_name) > 0:
            models.Student.objects.create(stu_name=stu_name, classes_id=class_id)

        else:
            message_erro = "学生姓名不能为空"
            raise Exception()
    except Exception as e:
        ret['status'] = False

    ret['message'] = message_erro
    return HttpResponse(json.dumps(ret))


@check_login
def modal_edit_student(request):
    ret = {'status': True, 'message': None}
    message_erro = "处理erro"
    try:

        stu_id = request.POST.get('stu_id')
        stu_name = request.POST.get('stu_name')
        class_id = request.POST.get('class_id')
        if len(stu_name) > 0:
            models.Student.objects.filter(pk=stu_id).update(stu_name=stu_name, classes=class_id)
        else:
            message_erro = "学生姓名不能为空"
            raise Exception()
    except Exception as e:
        ret['status'] = False

    ret['message'] = message_erro
    return HttpResponse(json.dumps(ret))


@check_login
def modal_del_student(request):
    ret = {'status': True, 'message': None}
    message_erro = '处理erro'
    try:
        stu_id = request.POST.get('nid')
        models.Student.objects.filter(pk=stu_id).delete()
    except Exception as e:
        message_erro = "删除失败请稍后再试！"
        ret['status'] = False

    ret['message'] = message_erro
    return HttpResponse(json.dumps(ret))


@check_login
def teacher(request, page):
    # obj = Mysql_Connet()
    # teacher_list = obj.mysql_result(
    #     'select teacher.id as t_id, teacher.th_name,class.class_name from teacher left join relationship on teacher.id=relationship.t_id left join class on relationship.c_id= class.id',[])
    #
    # teacher_lists = {}
    # for teacher_i in teacher_list:
    #     tid = teacher_i['t_id']
    #
    #     if  tid in teacher_lists:
    #         teacher_lists[tid]['classes_names'].append(teacher_i['class_name'])
    #
    #     else:
    #         teacher_lists[tid]={'t_id':teacher_i['t_id'],'th_name':teacher_i['th_name'],'classes_names':[teacher_i['class_name'],]}
    #
    # class_list = obj.mysql_result('select * from class',[])
    # obj.mysql_colse()
    # teacher.id as t_id, teacher.th_name,class .class_name
    page_info = PageInfo(page, models.Teacher.objects.all().count(), 10, '/teacher/', 11)

    teacher_list = models.Teacher.objects.values('id', 'th_name', 'classess__class_name')
    teacher_lists = {}
    for teacher_i in teacher_list:
        tid = teacher_i['id']

        if tid in teacher_lists:
            teacher_lists[tid]['classes_names'].append(teacher_i['classess__class_name'])

        else:
            teacher_lists[tid] = {'id': teacher_i['id'], 'th_name': teacher_i['th_name'],
                                  'classes_names': [teacher_i['classess__class_name'], ]}

    teacher_lists = list(teacher_lists.values())[page_info.start():page_info.end()]
    class_list = models.Classes.objects.all()
    return render(request, 'teacher.html',
                  {'teacher_list': teacher_lists, 'class_list': class_list, 'page_info': page_info})


@check_login
def add_teacher(request):
    if request.method == "GET":
        class_list = models.Classes.objects.all()
        return render(request, 'add_teacher.html', {'class_list': class_list})
    else:
        t_name = request.POST.get('teacher_name')
        add_class_list = request.POST.getlist('selete_class_id')
        print(add_class_list)
        a_teacher = models.Teacher.objects.create(th_name=t_name)
        for x in add_class_list:
            a_teacher.classess.add(x)
        #
        # t_id = obj.mysql_commit_return_id('insert into teacher(th_name) values(%s)',[t_name,])
        # t_2_c = []
        # for class_id in add_class_list:
        #     t_2_c.append((t_id,class_id))
        # obj.mysql_many_commit('insert into relationship(t_id,c_id) values(%s,%s)',t_2_c)
        # obj.mysql_colse()
        return redirect(reverse('teacher', kwargs={'page': 1}))


@check_login
def edit_teacher(request, nid):
    if request.method == "GET":
        class_list = models.Classes.objects.all()
        e_teacher = models.Teacher.objects.filter(pk=nid).first()
        old_class_list = []
        for i in e_teacher.classess.all():
            old_class_list.append(i.id)
        return render(request, 'edit_teacher.html',
                      {'class_list': class_list, 'e_teacher': e_teacher, 'old_class_list': old_class_list, 't_id': nid})
    else:
        teacher_name = request.POST.get('teacher_name')
        selete_class_id = request.POST.getlist('selete_class_id')
        models.Teacher.objects.filter(pk=nid).update(th_name=teacher_name)
        e_tea = models.Teacher.objects.filter(pk=nid).first()
        e_tea.classess.clear()
        for i in selete_class_id:
            e_tea.classess.add(i)
        return redirect(reverse('teacher', kwargs={'page': 1}))


@check_login
def del_teacher(request, nid):
    t = models.Teacher.objects.filter(pk=nid).first()
    t.classess.clear()
    t.delete()
    return redirect(reverse('teacher', kwargs={'page': 1}))


@check_login
def modal_add_teacher(request):
    ret = {'status': True, 'message': None}
    try:
        t_name = request.POST.get('t_name')
        class_id_list = request.POST.getlist('class_id_list')
        t = models.Teacher.objects.create(th_name=t_name)
        t.classess.add(*class_id_list)
    except Exception as e:
        ret['status'] = False
        ret['message'] = '添加失败'

    return HttpResponse(json.dumps(ret))


@check_login
def modal_edit_teacher(request):
    ret = {'status': True, 'message': None}
    obj = Mysql_Connet()
    try:
        nid = request.POST.get('nid')
        t_name = request.POST.get('t_name')
        class_list = request.POST.getlist('class_list')
        a_t = models.Teacher.objects.filter(pk=nid)
        a_t.update(th_name=t_name)
        at1 = a_t.first()
        at1.classess.clear()
        at1.classess.add(*class_list)

    except Exception as e:
        ret['status'] = False
        ret['message'] = '添加失败'

    obj.mysql_colse()
    return HttpResponse(json.dumps(ret))


@check_login
def modal_del_teacher(request):
    ret = {'status': True, 'message': None}
    obj = Mysql_Connet()
    try:
        t_id = request.POST.get('nid')
        # obj.mysql_commit('delete from relationship where t_id=%s',[t_id])
        # obj.mysql_commit('delete from teacher where id=%s',[t_id])
        models.Teacher2Class.objects.get(t_id=t_id).delete()
        models.Teacher.objects.get(id=t_id).delete()
    except Exception as e:
        print(e)
        ret['status'] = False
        ret['message'] = '删除失败'

    obj.mysql_colse()
    return HttpResponse(json.dumps(ret))


@check_login
def get_class_list(request):
    class_list = list(models.Classes.objects.values('id', 'class_name'))
    return HttpResponse(json.dumps(class_list))


@check_login
def get_teacher2class_list(request):
    nid = request.POST.get('nid')
    t = models.Teacher.objects.filter(pk=nid).first().classess.all()
    a = []
    for i in t:
        a.append(i.id)
    return HttpResponse(json.dumps(a))


@check_login
def logout(request):
    rep = redirect('/login/')
    rep.delete_cookie('liu')
    return rep


def add_data(request):
    for i in range(1, 200):
        v = models.Classes.objects.create(class_name=('classes' + str(i)))
        models.Student.objects.create(stu_name=('student' + str(i)), classes=v)
        models.Teacher.objects.create(th_name=('teacher' + str(i)))
    return HttpResponse('ok')
