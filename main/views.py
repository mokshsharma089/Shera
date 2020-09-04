import random,string
from django.shortcuts import render,get_object_or_404,reverse
from .forms import GroupForm
from django.http import HttpResponseRedirect
from .models import Group,Member,Transaction
# Create your views here.

def home(request):
    return render(request,'home.html')

def newRandomCode(size):
    return ''.join(random.choice(string.ascii_lowercase+ string.ascii_uppercase + string.digits) for _ in range(size) )

def CreateGroup(request):   
    if request.method=='GET':
        code=newRandomCode(4)
        context={
            'code':code
        }
        return render(request,'create_group.html',context)
    if request.method == 'POST':
        if request.POST.get('password1') and request.POST.get('password2'):
            password1=request.POST.get('password1')
            password2=request.POST.get('password2')
            if password1 == password2:
                code=request.POST.get('code')
                salt=newRandomCode(4)
                Pass=hash(password1+salt)
                Group.objects.create(code=code,password=Pass,salt=salt)
                #change to httpredirect something like that to group page
                return render(request,'base.html')
            else:
                error="Passwords Dont Match enter again"
                context={
                'code':request.POST.get('code'),
                'message':error
                }
                return render(request,'create_group.html',context)

        else:
            error="Enter password"
            context={
                'code':request.POST.get('code'),
                'message':error
            }
            return render(request,'create_group.html',context)
        
def Custom_Group(request,slug,*args,**kwargs):
    obj=get_object_or_404(Group,code=slug)
    members=Member.objects.filter(group=obj.pk)
    context={
        'code':obj.code,
        'members':members
    }
    return render(request,'group.html',context)

def AddMember(request,slug,*args,**kwargs):
    obj=get_object_or_404(Group,code=slug)
    if request.method=='GET':
        context={
            'code':obj.code
        }
        return render(request,'AddMember.html',context)
    if request.method=='POST':
        if request.POST.get('Name'):
            name=request.POST.get('Name')
            Member.objects.create(name=name,group=obj)
            return HttpResponseRedirect('/Gr/{0}'.format(slug))
        else:
            error="Enter Name"
            context={
                'code':obj.code,
                'message':error
            }
            return render(request,'AddMember.html',context)

def addTransaction(request,slug,*args,**kwargs):
    group=get_object_or_404(Group,code=slug)
    members=Member.objects.filter(group=group.pk)
    if request.method=='GET':
        context={
            'code':group.code,
            'members':members
        }
        return render(request,'AddTransaction.html',context)
    if request.method=='POST':
        if request.POST.get('member') and request.POST.get('amount') and request.POST.get('title'):
            memberPK=request.POST.get('member')
            member=Member.objects.get(pk=memberPK)
            amount=request.POST.get('amount')
            title=request.POST.get('title')
            Transaction.objects.create(group=group,member=member,amount=amount,title=title)
            return HttpResponseRedirect('/Gr/{0}'.format(slug))
        else:
            error="All fields are compulsory"
            context={
                'code':group.code,
                'members':members,
                'message':error
            }
            return render(request,'AddTransaction.html',context)




    