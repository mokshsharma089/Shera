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
        code=newRandomCode(10)
        context={
            'code':code
        }
        return render(request,'create_group.html',context)
    if request.method == 'POST':
        if request.POST.get('password1') and request.POST.get('password2'):
            if not request.POST.get('mail'):
                error="Enter Mail Id"
                context={
                'code':request.POST.get('code'),
                'message':error
                }
                return render(request,'create_group.html',context)
            if not request.POST.get('title'):
                error="Enter Title for Tab"
                context={
                'code':request.POST.get('code'),
                'message':error
                }
                return render(request,'create_group.html',context)
            password1=request.POST.get('password1')
            password2=request.POST.get('password2')
            if password1 == password2:
                code=request.POST.get('code')
                salt=newRandomCode(4)
                Pass=hash(password1+salt)
                title=request.POST.get('title')
                mail=request.POST.get('mail')
                Group.objects.create(code=code,password=Pass,salt=salt,total=0,title=title,mail=mail)
                #change to httpredirect something like that to group page
                return HttpResponseRedirect('/Gr/{0}'.format(code))
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
    log=Transaction.objects.filter(group=obj.pk)
    context={
        'total':obj.total,
        'title':obj.title,
        'code':obj.code,
        'members':members,
        'transactions':log
    }
    return render(request,'group.html',context)

def AddMember(request,slug,*args,**kwargs):
    obj=get_object_or_404(Group,code=slug)
    if request.method=='GET':
        context={
            'code':obj.code,
            'title':obj.title,
            'mail':obj.mail,
        }
        return render(request,'AddMember.html',context)
    if request.method=='POST':
        if request.POST.get('Name'):
            name=request.POST.get('Name')
            Member.objects.create(name=name,group=obj,amount_spent=0,delta=0)
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
            'members':members,
            'title':group.title,
            'mail':group.mail,
        }
        return render(request,'AddTransaction.html',context)
    if request.method=='POST':
        if request.POST.get('member') and request.POST.get('amount') and request.POST.get('title'):
            memberPK=request.POST.get('member')
            member=Member.objects.get(pk=memberPK)
            amount=float(request.POST.get('amount'))
            title=request.POST.get('title')
            new_total=group.total+amount
            group.total=new_total
            group.save()
            # group.update(total=new_total)
            Transaction.objects.create(group=group,member=member,amount=amount,title=title)
            Mem=list(members)
            no_of_people=len(list(members))
            amount_owed_by_each_member=amount/no_of_people
            amount_delta_for_payee=(no_of_people-1)*amount_owed_by_each_member
            for i in members:
                if(i == member):
                    old_delta=i.delta
                    new_delta=old_delta-amount_delta_for_payee
                    i.delta=new_delta
                    old_amount=i.amount_spent
                    i.amount_spent=amount+old_amount
                    i.save()
                    # i.update(delta=new_delta)
                else:
                    old_delta=i.delta
                    new_delta=old_delta+amount_owed_by_each_member
                    i.delta=new_delta
                    i.save()
                    # i.update(delta=new_delta)
            return HttpResponseRedirect('/Gr/{0}'.format(slug))
        else:
            error="All fields are compulsory"
            context={
                'code':group.code,
                'members':members,
                'message':error
            }
            return render(request,'AddTransaction.html',context)


def GetGroup(request):
    if request.method=='GET':
        return render(request,'findGroup.html')
    if request.method=='POST':
        if not request.POST.get('mail') and not request.POST.get('code'):
            error="Please Enter any One Field"
            context={
                'message':error
            }
            return render(request,'findGroup.html',context)
        elif request.POST.get('code') and not request.POST.get('mail'):
            inputCode=request.POST.get('code')
            obj=Group.objects.filter(code=inputCode)
            if obj.count()>0:
                return HttpResponseRedirect('/Gr/{0}'.format(inputCode))
            else:
                error="No Open Tab with This Code"
                context={
                'message':error
                }
                return render(request,'findGroup.html',context)
        elif request.POST.get('mail') and not request.POST.get('code'):
            Inputmail=request.POST.get('mail')
            obj=Group.objects.filter(mail=Inputmail)
            if obj.count()>0:
                context={
                    'mail':Inputmail,
                    'groups':obj
                }
                return render(request,'showgroupsByMail.html',context)
            else:
                error="No Open Tab with this Mail"
                context={
                'message':error
                }
                return render(request,'findGroup.html',context)
        else:
            error="Please Enter Only One Field"
            context={
                'message':error
            }
            return render(request,'findGroup.html',context)
        






    