from django.db import models

# Create your models here.
class Group(models.Model):
    code=models.CharField(max_length=10,unique=True)
    title=models.CharField(max_length=250)
    password=models.CharField(max_length=128)
    salt=models.CharField(max_length=4)
    total=models.FloatField()
    date=models.DateField(auto_now_add=True)
    mail=models.EmailField(max_length = 254,blank=False)
    def __str__(self):
        return str(self.code)

class Member(models.Model):
    name=models.CharField(max_length=100)
    delta=models.FloatField()
    #delta will be used to implement how much any person owes compared to other people
    amount_spent=models.FloatField()
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    def __str__(self):
        return "{0} of group {1}".format(self.name,self.group.code)

class Transaction(models.Model):
    title=models.CharField(max_length=50)
    member=models.ForeignKey(Member,on_delete=models.CASCADE)
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    amount=models.FloatField()
    date=models.DateField(auto_now_add=True)
    def __str__(self):
        return "{3} == Rs {0} by {1} for {2}".format(self.amount,self.member.name,self.title,self.group.code)