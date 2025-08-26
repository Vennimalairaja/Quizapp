from django.urls import path
from .views import takequiz,addnewquestion,Staffcreationform,firsttest,login_view
urlpatterns=[
    path('taketest/',firsttest),
    path('taketest/<int:qid>',takequiz,name='taketest'),
    path('addquestion/',addnewquestion,name='addnewquestion'),
    path('Signup/',Staffcreationform,name='register'),
    path('login/',login_view,name='login')
]