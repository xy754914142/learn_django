from django.db import models

# Create your models here.

class Userdate(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

class Classes(models.Model):
    class_name = models.CharField(max_length=32)

class Student(models.Model):
    stu_name = models.CharField(max_length=32)
    classes = models.ForeignKey('Classes', on_delete=models.CASCADE)

class Teacher(models.Model):
    th_name = models.CharField(max_length=32)

class Teacher2Class(models.Model):
    t_id = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    c_id = models.ForeignKey('Classes', on_delete=models.CASCADE)
