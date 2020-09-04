from django.urls import path,include
from main import views

urlpatterns=[
    path('',views.home,name="home"),
    path('CG',views.CreateGroup,name="CreateGroup"),
    path('Gr/<slug:slug>',views.Custom_Group,name="customGroup"),
    path('Gr/<slug:slug>/addM',views.AddMember,name="customGroupAddMember"),
    path('Gr/<slug:slug>/addT',views.addTransaction,name="customGroupAddTransaction")
]
