from django.shortcuts import render,redirect,HttpResponse
from utils.connte_mysql import *
from functools import wraps
import json

def check_login(func):
    @wraps(func)
    def inner(request,*args,**kwargs):
        ret = request.get_signed_cookie('liu',default='0',salt='abc')
        if ret == 'fenglin':
            return func(request,*args,**kwargs)
        else:
            return redirect('/login/')

    return inner



def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        obj = Mysql_Connet()
        find_password = obj.mysql_fetchone('select password from userdata where username=%s',[user])

    if find_password == None:
        return render(request, 'login.html')

    if find_password['password'] == pwd:
        cook = redirect('/management/')
        cook.set_signed_cookie('liu','fenglin',salt='abc',max_age=10)
        return cook
    else:
        return render(request,'login.html')







@check_login
def management(request):
    return render(request,'management.html')

@check_login
def classes(request):
    # class_list = mysql_result('select id,class_name from class')
    obj = Mysql_Connet()
    class_list = obj.mysql_result('select id,class_name from class',[])
    obj.mysql_colse()
    return render(request, 'classes.html', {"classes_list":class_list})


@check_login
def add_class(request):
    if request.method == "GET":
        return render(request,'add_class.html')
    else:
        v = request.POST.get('class_id')
        mysql_commit('insert into class(class_name) values(%s)', v)
        return redirect('/classes/')

@check_login
def del_class(request):
    nid = request.GET.get('nid')
    mysql_commit('delete from class where id = %s', nid)

    return redirect('/classes/')

@check_login
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

@check_login
def student(request):
    obj = Mysql_Connet()
    student_list = obj.mysql_result('select student.id,student.stu_name,class.class_name,class.id as clsid from student left join class on student.class_id = class.id',[])
    class_list = obj.mysql_result('select id,class_name from class',[])
    obj.mysql_colse()
    return render(request,'student.html',{'student_list':student_list,'class_list':class_list})

@check_login
def add_student(request):
    if request.method == "GET":
        class_list = mysql_result('select id,class_name from class')
        return render(request,'add_student.html',{'class_list':class_list})
    else:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        mysql_commit('insert into student(stu_name,class_id) values(%s,%s)',[name,class_id,])
        return redirect('/student/')

@check_login
def del_student(request):
    nid = request.GET.get('nid')
    mysql_commit('delete from student where id=%s',[nid,])
    return redirect('/student/')

@check_login
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

@check_login
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

@check_login
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

@check_login
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



@check_login
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

@check_login
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

@check_login
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

@check_login
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

@check_login
def add_teacher(request):
    obj = Mysql_Connet()
    if request.method == "GET":
        class_list = obj.mysql_result('select id,class_name from class',[])
        obj.mysql_colse()
        return render(request,'add_teacher.html',{'class_list':class_list})
    else:
        t_name = request.POST.get('teacher_name')
        add_class_list = request.POST.getlist('selete_class_id')
        print(add_class_list)
        t_id = obj.mysql_commit_return_id('insert into teacher(th_name) values(%s)',[t_name,])
        t_2_c = []
        for class_id in add_class_list:
            t_2_c.append((t_id,class_id))
        obj.mysql_many_commit('insert into relationship(t_id,c_id) values(%s,%s)',t_2_c)
        obj.mysql_colse()
        return redirect('/teacher/')

@check_login
def edit_teacher(request):
    obj = Mysql_Connet()
    if request.method == "GET":
        class_list = obj.mysql_result('select id,class_name from class',[])
        t_id = request.GET.get('nid')
        t_name = obj.mysql_fetchone('select th_name from teacher where id=%s',[t_id])['th_name']
        old_class_list = obj.mysql_result('select id,c_id from relationship where t_id=%s',[t_id,])
        d_class_list=[]
        for o_class in old_class_list:
            d_class_list.append(o_class['c_id'])
        return render(request,'edit_teacher.html',{'class_list':class_list,'t_name':t_name,'old_class_list':d_class_list,'t_id':t_id})
    else:
        t_id = request.GET.get('nid')
        teacher_name = request.POST.get('teacher_name')
        selete_class_id = request.POST.getlist('selete_class_id')
        obj.mysql_commit('update teacher set th_name=%s where id=%s',[teacher_name,t_id])
        new_class_2_teacher = [(t_id, class_id) for class_id in selete_class_id]
        #方法一直接删除再添加
        obj.mysql_commit('delete from relationship where t_id=%s',[t_id,])
        obj.mysql_many_commit('insert into relationship(t_id,c_id) values(%s,%s)',new_class_2_teacher)
        #方法二 对比后添加编辑 ??暂时不知道怎么做，先放着
        # [{'id': 5, 'c_id': 2}, {'id': 6, 'c_id': 1}]
        # old_class_list = obj.mysql_result('select id,c_id from relationship where t_id=%s',[t_id,])
        # print(old_class_list)
        # for new_c_id in selete_class_id:
        #     for row in old_class_list:
        #         if new_c_id == row['c_id']

        obj.mysql_colse()
        return redirect('/teacher/')

@check_login
def del_teacher(request):
    del_id = request.GET.get('nid')
    obj = Mysql_Connet()
    obj.mysql_commit('delete from teacher where id=%s',[del_id,])
    obj.mysql_commit('delete from relationship where t_id=%s',[del_id,])
    return redirect('/teacher/')

@check_login
def modal_add_teacher(request):
    ret = {'status':True,'message':None}
    obj = Mysql_Connet()
    try:
        t_name = request.POST.get('t_name')
        class_id_list = request.POST.getlist('class_id_list')
        t_id = obj.mysql_commit_return_id('insert into teacher(th_name) values(%s)',[t_name])
        class_2_teacher = [(t_id,c_id) for c_id in class_id_list]
        obj.mysql_many_commit('insert into relationship(t_id,c_id) values(%s,%s)',class_2_teacher)
    except Exception as e:
        ret['status']=False
        ret['message']='添加失败'

    obj.mysql_colse()
    return HttpResponse(json.dumps(ret))

@check_login
def modal_edit_teacher(request):
    ret = {'status': True, 'message': None}
    obj = Mysql_Connet()
    try:
        nid = request.POST.get('nid')
        t_name = request.POST.get('t_name')
        class_list = request.POST.getlist('class_list')
        obj.mysql_commit('update teacher set th_name=%s where id=%s',[t_name,nid])
        obj.mysql_commit('delete from relationship where t_id=%s',[nid])
        class2teacher = [(nid,class_id) for class_id in class_list]
        obj.mysql_many_commit('insert into relationship(t_id,c_id) values(%s,%s)',class2teacher)

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
        obj.mysql_commit('delete from relationship where t_id=%s',[t_id])
        obj.mysql_commit('delete from teacher where id=%s',[t_id])

    except Exception as e:
        ret['status'] = False
        ret['message'] = '删除失败'

    obj.mysql_colse()
    return HttpResponse(json.dumps(ret))

@check_login
def get_class_list(request):
    obj = Mysql_Connet()
    class_list = obj.mysql_result('select id,class_name from class',[])
    obj.mysql_colse()
    return HttpResponse(json.dumps(class_list))

@check_login
def get_teacher2class_list(request):
    nid = request.POST.get('nid')
    obj = Mysql_Connet()
    class_list = obj.mysql_result('select c_id from relationship where t_id=%s',[nid])
    obj.mysql_colse()
    a = []
    for i in class_list:
        a.append(i['c_id'])
    return HttpResponse(json.dumps(a))

@check_login
def logout(request):
    rep = redirect('/login/')
    rep.delete_cookie('liu')
    return rep