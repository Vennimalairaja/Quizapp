from django.urls import path
from .views import takequiz,addnewquestion,Staffcreationform
urlpatterns=[
    path('taketest/<int:qid>',takequiz,name='taketest'),
    path('addquestion/',addnewquestion,name='addnewquestion'),
    path('createuser/',Staffcreationform,name='newuser'),
]