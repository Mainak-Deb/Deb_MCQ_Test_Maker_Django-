from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Examset,Question,Marks
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login, logout 
import logging
import json

from django.contrib import messages
from django.utils import timezone
from math import ceil
import random
# Get an instance of a logger
logger = logging.getLogger(__name__)


code=[]
for i in range(48,58):
    code.append(chr(i))
for i in range(65,91):
    code.append(chr(i))
for i in range(97,123):
    code.append(chr(i))


def home(request):
    return render(request,"index.html")



def handleSignup(request):
    try:
        if request.method== "POST":
            #Get the post parameters
            username =request.POST['username']
            fname =request.POST['fname']
            lname =request.POST['lname']
            email =request.POST['email']
            pass1 =request.POST['pass1']
            pass2 =request.POST['pass2']

            #checks for erroneous inputs

            if (len(username)>10) :
                messages.error(request,"username must be under 10 characters")
                return redirect("home")

            #create the user
            if (pass1!=pass2) :
                messages.error(request,"password do not match")
                return redirect("home")

            #create the user        


            myuser= User.objects.create_user(username,email,pass1)
            myuser.first_name =fname
            myuser.last_name =lname
            myuser.save()
            messages.success(request,"Your Papyrus Account Has Been Succesfully Created, Please Login To Continue")
            return redirect("home")

        else:
            return render(request, 'error.html')
    except:
        return render(request, 'error.html')


def handleLogin(request):
	if request.method== "POST":
		#Get the post parameters
		loginusername =request.POST['loginusername']
		loginpassword =request.POST['loginpassword']	


		user =auth.authenticate(username=loginusername,password=loginpassword)

		if user is not None:
			auth.login(request,user)
			messages.success(request,"Succesfully logged In")
			return redirect("home")

		else:
			messages.error(request,"Invalid Credentials")
			return redirect("home")

	messages.error(request,"Please Signup Or Login to Continue")
	return redirect("home")


def handleLogout(request):
		logout(request)
		messages.success(request,"Succesfully logged Out")
		return redirect("home")
def createform(request):
		return render(request,"create.html")

def questionset(request):
        try:
            if request.method=="POST":
                name = request.POST.get('name','')
                subject = request.POST.get('subject','')
                topic = request.POST.get('topic','')
                time = request.POST.get('timestamp','')
                fm = request.POST.get('fullmarks','')
                eset = Examset(name=name, subject=subject,topic=topic,time=time,fm=fm)
                eset.save()
                eid = eset.qid
                print(eid)
                mcqset={
                    'id': eid,
                    'subject': subject,
                    'topic':topic,
                    'time':time,
                    'fm':fm,
                }
                print(mcqset)
                print("reach")
                return render(request, 'makeMCQ.html', mcqset)
            else:
                return render(request, 'error.html')
        except:
            return render(request, 'error.html')


def addqs(request):
        try:
            if request.method=="POST":
                name = request.POST.get('name','')
                id = request.POST.get('id','')
                if(str(request.user)==str(name)):
                    return render(request, 'addquestions.html',{'id':id})
                else:
                    return render(request, 'error.html')
            else:
                return render(request, 'error.html')
        except:
            return render(request, 'error.html')

def qsadded(request):
        try:
            if request.method=="POST":
                eid = request.POST.get('eid','')
                question =request.POST.get('question','')
                points = request.POST.get('Point','')
                ans = request.POST.get('Answer','')
                op2 = request.POST.get('Option2','')
                op3 = request.POST.get('Option3','')
                op4 = request.POST.get('Option4','')
                qusn = Question(eid=eid, question=question, points=points,ans=ans,op2=op2,op3=op3,op4=op4)
                qusn.save()
                # print(qusn)
                return render(request, 'addquestions.html',{'id':eid})
                
            else:
                return render(request, 'error.html')
        except:
            return render(request, 'error.html')



@login_required(login_url='handleLogin')
def dashboard(request,name):
   try:
    if(str(request.user)==str(name)):
        update = Examset.objects.filter(name=str(request.user))
        links=[]
        for i in update:
            sid=int(i.qid)+5000;
            st=""
            for j in range(4):
                    st=code[int(sid%62)]+st
                    sid=sid//62
            st="http://127.0.0.1:8000/test/"+st
            links.append([i.qid,i.subject,i.topic,st])
        print(links)
        table={"table":links}
        return render(request, 'dashboard.html',table)
    else:
	    return render(request, 'error.html')
   except:
       return render(request, 'error.html')


def edit(request):
        try:
            if request.method=="POST":
                name = request.POST.get('name','')
                id = request.POST.get('id','')
                if(str(request.user)==str(name)):
                    qry=list(Examset.objects.filter(qid=id))
                    for i in qry:
                        mcqset={
                            'id': i.qid,
                            'subject': i.subject,
                            'topic':i.topic,
                            'time':i.time,
                            'fm':i.fm,
                        }
                        # print(mcqset)
                return render(request, 'makeMCQ.html', mcqset)
            else:
                return render(request, 'error.html')
        except:
            return render(request, 'error.html')


def preview(request):
        try:
            if request.method=="POST":
                name = request.POST.get('name','')
                id = request.POST.get('id','')
                if(str(request.user)==str(name)):
                    mcqry=Question.objects.filter(eid=id)
                    #print(mcqry)
                    qsli=[]
                    for i in mcqry:
                        mcq={
                            'qs':i.question,
                            'point':i.points,
                            'ans':i.ans,
                             'op':[i.op2,i.op3,i.op4]                            
                        }
                        qsli.append(mcq)
                        
                    #print("qsli= ",qsli)
                return render(request, 'preview.html',{'qs':qsli})
            else:
                return render(request, 'error.html')
        except:
            return render(request, 'error.html')

def test(request,examid):
        try:
            slk=str(examid)
            c=0;
            for i in range(3,-1,-1):
                k=int(code.index(slk[i]))
                c=c+(k*(62**(3-i)))
            c=c-5000;

            mcqry2=Question.objects.filter(eid=c)
            #print(mcqry)
            tests=[]
            for i in mcqry2:
                opli=[i.op2,i.ans,i.op3,i.op4]
                random.shuffle(opli)
                testqs={
                    'id':i.tid,
                    'qs':i.question,
                    'point':i.points,
                    'op':opli
                }
                tests.append(testqs)
                
            random.shuffle(tests)
            print("qsli= ",tests)
            return render(request, 'test.html',{'tq':tests})
        except:
            return render(request, 'error.html')



def evaluate(request):
        try:
            if request.method=="POST":
                rq =dict(request.POST.items())          
                print(rq)
                marks=0
                rq.pop('csrfmiddlewaretoken')
                dstore=[rq['name'],rq['email']]
                print(dstore)
                rq.pop('name')
                rq.pop('email')

                for i in rq:
                    ans=Question.objects.filter(tid=int(i))
                    ali=[[x.ans,x.points,x.eid] for x in ans]
                    print(rq[i],ali[0][0])
                    if(rq[i]==ali[0][0]):
                        print(ali[0][1])
                        marks+=ali[0][1]
                    print(ans)
                dstore.append(marks)
                dstore.append(ali[0][2])
                attends=Marks(mid=dstore[3],name=dstore[0],email=dstore[1],marks=marks)
                attends.save()
                return render(request, 'evaluate.html',{'marks':marks})
            else:
                return render(request, 'error.html')
        except:
            return render(request, 'error.html')


def marks(request):
        try:
            if request.method=="POST":
                name = request.POST.get('name','')
                id = request.POST.get('id','')
                if(str(request.user)==str(name)):
                    stumarks=Marks.objects.filter(mid=int(id))
                    stu=[]
                    for i in stumarks:
                        mcqmarks={
                            'name':i.name,
                            'email':i.email,
                            'marks':i.marks,                         
                        }
                        stu.append(mcqmarks)
                    print(stu)
                    return render(request, 'marks.html',{'mcqmarks':stu})
                else:
                    return render(request, 'error.html')   
            else:
                return render(request, 'error.html')
        except:
            return render(request, 'error.html')

