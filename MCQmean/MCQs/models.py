from django.db import models

# Create your models here.

class Examset(models.Model):
    name = models.CharField(max_length=90)   
    qid = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=90)
    topic = models.CharField(max_length=200)
    time = models.IntegerField(default=60)
    fm = models.IntegerField(default=0)
    def __str__(self):
        return str(self.qid)


class Question(models.Model):
    tid = models.AutoField(primary_key=True)
    eid = models.IntegerField(default=0)  
    question = models.CharField(max_length=500)
    points = models.IntegerField(default=1)
    ans = models.CharField(max_length=200)
    op2 = models.CharField(max_length=200)
    op3 = models.CharField(max_length=200)
    op4 = models.CharField(max_length=200)
    def __str__(self):
        return str(self.eid)+">"+str(self.tid)+">"+str(self.question)


class Marks(models.Model):
    mid = models.IntegerField(default=0)  
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=50)
    marks = models.IntegerField(default=0)
    def __str__(self):
        return str(self.mid)+">"+str(self.name)
