from django.urls import path
from .views import addquestion,takequiz
urlpatterns=[
    path('questions/',addquestion,name='addquestions'),
    path('taketest/',takequiz,name='taketest'),
]