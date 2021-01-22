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
    # class_list = mysql_result('select id,class_name from class')
    obj = Mysql_Connet()
    class_list = obj.mysql_result('select id,class_name from class',[])
    obj.mysql_colse()
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


def student(request):
    obj = Mysql_Connet()
    student_list = obj.mysql_result('select student.id,student.stu_name,class.class_name,class.id as clsid from student left join class on student.class_id = class.id',[])
    class_list = obj.mysql_result('select id,class_name from class',[])
    obj.mysql_colse()
    return render(request,'student.html',{'student_list':student_list,'class_list':class_list})

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
    message_erro = "处理erro"
    try:
        nid = request.POST.get('nid')
        mysql_commit('delete from class where id=%s',[nid,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = message_erro

    return HttpResponse(json.dumps(ret))




def modal_add_student(request):
    ret = {"status":True,'message':None}
    message_erro = "处理erro"
    try:
        stu_name = request.POST.get('stu_name')
        class_id = request.POST.get('class_id')
        if len(stu_name)>0:
            obj = Mysql_Connet()
            obj.mysql_commit('insert into student(stu_name,class_id) values(%s,%s)',[stu_name,class_id,])
            obj.mysql_colse()

        else:
            message_erro = "学生姓名不能为空"
            raise Exception()
    except Exception as e:
        ret['status'] = False

    ret['message'] = message_erro
    return HttpResponse(json.dumps(ret))

def modal_edit_student(request):
    ret = {'status':True,'message':None}
    message_erro = "处理erro"
    try:

        stu_id = request.POST.get('stu_id')
        stu_name = request.POST.get('stu_name')
        class_id = request.POST.get('class_id')
        if len(stu_name)>0:
            obj = Mysql_Connet()
            obj.mysql_commit('update student set stu_name=%s,class_id=%s where id=%s ', [stu_name, class_id, stu_id,])
            obj.mysql_colse()

        else:
            message_erro = "学生姓名不能为空"
            raise Exception()
    except Exception as e:
        ret['status'] = False

    ret['message'] = message_erro
    return HttpResponse(json.dumps(ret))

def modal_del_student(request):
    ret = {'status':True,'message':None}
    message_erro = '处理erro'
    try:
        stu_id = request.POST.get('nid')
        obj = Mysql_Connet()
        obj.mysql_commit('delete from student where id=%s',[stu_id,])
        obj.mysql_colse()
    except Exception as e:
        message_erro = "删除失败请稍后再试！"
        ret['status'] = False

    ret['message']=message_erro
    return HttpResponse(json.dumps(ret))


def teacher(request):
    obj = Mysql_Connet()
    teacher_list = obj.mysql_result('select teacher.id as t_id, teacher.th_name,class.class_name from teacher left join relationship on teacher.id=relationship.t_id left join class on relationship.c_id= class.id',[])
    teacher_lists = {}
    for teacher_i in teacher_list:
        tid = teacher_i['t_id']

        if  tid in teacher_lists:
            teacher_lists[tid]['classes_names'].append(teacher_i['class_name'])

        else:
            teacher_lists[tid]={'t_id':teacher_i['t_id'],'th_name':teacher_i['th_name'],'classes_names':[teacher_i['class_name'],]}

    class_list = obj.mysql_result('select * from class',[])
    obj.mysql_colse()
    return render(request,'teacher.html',{'teacher_list':teacher_lists.values(),'class_list':class_list})


def modal_add_teacher(request):
    obj = Mysql_Connet()
    if request.method == "GET":
        class_list = obj.mysql_result('select id,class_name from class',[])
        return render(request,'add_teacher.html',{'class_list':class_list})
    else:
        t_name = request.POST.get('teacher_name')
        add_class_list = request.POST.getlist('selete_class_id')

        t_id = obj.mysql_commit_return_id('insert into teacher(th_name) values(%s)',[t_name,])


        return HttpResponse(t_id)

def modal_edit_teacher(request):
    pass
def modal_del_teacher(request):
    pass
