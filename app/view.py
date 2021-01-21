from django.shortcuts import render,redirect,HttpResponse
from utils.connte_mysql import *
import json

def index(request):
    if request.method == 'GET':
        return render(
            request,
            'index.html'
        )
    else:
        if request.POST.get('username') == 'root' and request.POST.get('password') == '123':
            return redirect('/classes/')
        else:
            return render(request,'index.html',{'msg':'账号或密码错误！'})


def classes(request):
    class_list = mysql_result('select id,class_name from class')
    return render(request,'classes.html',{"classes_list":class_list})



def add_class(request):
    if request.method == "GET":
        return render(request,'add_class.html')
    else:
        v = request.POST.get('class_id')
        mysql_commit('insert into class(class_name) values(%s)', v)
        return redirect('/classes/')

def del_class(request):
    nid = request.GET.get('nid')
    mysql_commit('delete from class where id = %s', nid)

    return redirect('/classes/')

def edit_class(request):
    if request.method == 'GET':
        nid = request.GET.get('postid')
        class_list = mysql_fetchone('select id,class_name from class where id = %s',[nid,])
        return render(request,'edit_class.html',{'nid':nid,'class_list':class_list})
    else:
        nid = request.GET.get('nid')
        class_name = request.POST.get('title')
        mysql_commit("update class set class_name = %s where id = %s",[class_name,nid,])
        return redirect('/classes/')

def teacher(request):
    teacher_list = mysql_result('select id,th_name from teacher')
    return render(request,'teacher.html',{'teacher_list':teacher_list})

def add_teacher(request):
    if request.method == 'GET':
        return render(request,'add_teacher.html')
    else:
        v = request.POST.get('teacher_name')
        mysql_commit('insert into teacher(th_name) values(%s)',[v,])
        return redirect('/teacher/')

def del_teacher(request):
    nid = request.GET.get('nid')
    mysql_commit('delete from teacher where id=%s',[nid,])
    return redirect('/teacher/')


def edit_teacher(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        teach_date = mysql_fetchone('select id,th_name from teacher where id = %s',[nid,])
        return render(request, 'edit_teacher.html',{'teach_date':teach_date})
    else:
        nid = request.GET.get('nid')
        name = request.POST.get('name')
        mysql_commit("update teacher set th_name = %s where id = %s",[name,nid,])
        return redirect('/teacher/')

def student(request):
    student_list = mysql_result('select student.id,student.stu_name,class.class_name from student left join class on student.class_id = class.id')
    return render(request,'student.html',{'student_list':student_list})

def add_student(request):
    if request.method == "GET":
        class_list = mysql_result('select id,class_name from class')
        return render(request,'add_student.html',{'class_list':class_list})
    else:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        mysql_commit('insert into student(stu_name,class_id) values(%s,%s)',[name,class_id,])
        return redirect('/student/')

def del_student(request):
    nid = request.GET.get('nid')
    mysql_commit('delete from student where id=%s',[nid,])
    return redirect('/student/')

def edit_student(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        student_data = mysql_fetchone('select student.id,student.stu_name,class.class_name from student left join class on student.class_id = class.id where student.id = %s',[nid,])
        class_list = mysql_result('select * from class')
        return render(request,'edit_student.html',{'student_data':student_data,'class_list':class_list})
    else:
        nid = request.GET.get('nid')
        stu_name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        mysql_commit('update student set stu_name=%s,class_id=%s where id=%s',[stu_name,class_id,nid,])
        return redirect('/student/')


def modal_add_class(request):
    ret = {'status':True,'message':None}
    message_erro="处理erro"
    try:
        class_name = request.POST.get('class_name')
        if len(class_name)>0:
            mysql_commit('insert into class(class_name) values(%s)', class_name)
        else:
            message_erro = "班级名不能为空"
            raise Exception()
    except Exception as e:
        ret['status'] = False
        ret['message'] = message_erro

    return HttpResponse(json.dumps(ret))

def modal_edit_class(request):
    ret = {'status':True, 'message':None}
    message_erro = "处理erro"
    try:
        class_name = request.POST.get('class_name')
        nid = request.POST.get('nid')
        print('nid = {},  class_name = {}'.format(nid,class_name))
        if len(class_name)>0:
            mysql_commit('update class set class_name=%s where id=%s',[class_name,nid,])
        else:
            message_erro = "班级名不能为空"
            raise Exception()
    except Exception as e:
        ret['status'] = False
        ret['message'] = message_erro

    return HttpResponse(json.dumps(ret))


def modal_del_class(request):
    ret = {'status':True,'message':None}
    try:
        message_erro="处理erro"
        nid = request.POST.get('nid')
        mysql_commit('delete from class where id=%s',[nid,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = message_erro

    return HttpResponse(json.dumps(ret))