from django.urls import path
from .views import logout_view,unauthorized_view,add_students_view,StudentLogin,studentDashboard_view,update_students_view
from .views import render_dashboard,takequiz,addnewquestion,Staffcreationform,firsttest,login_view,score_view
urlpatterns=[
    path('dashboard/',render_dashboard,name='dashboard'),
    path('taketest/',firsttest,name='first_test'),
    path('taketest/<int:qid>',takequiz,name='taketest'),
    path('addquestion/',addnewquestion,name='addnewquestion'),
    path('Signup/',Staffcreationform,name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('unauthorized/',unauthorized_view,name='unauthorized'),
    path('addStudents/',add_students_view,name='add_students'),
    path('studentLogin/',StudentLogin,name='student_login'),
    path('studentdashboard/',studentDashboard_view,name='student-Dashboard'),
    path('staffdashboard/',update_students_view,name='staff-view'),
    path('viewscore',score_view,name='student-score')
]