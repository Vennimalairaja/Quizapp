from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import Questions,Staff
from .forms import QuestionForm,StaffUserCreationForm
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
# Create your views here.

def addnewquestion(request):
    if not hasattr(request.user,'staff'):
        return redirect('register')
    else:
        if request.method=='POST':
            question=request.POST.get('question')
            Option_a=request.POST.get('option_a')
            Option_b=request.POST.get('option_b')
            Option_c=request.POST.get('option_c')
            Option_d=request.POST.get('option_d')
            Correct=request.POST.get('correct')
            data=Questions.objects.create(Question=question,Option_a=Option_a,Option_b=Option_b,Option_c=Option_c,Option_d=Option_d,
            Correct_ans=Correct)
            messages.success(request,'Question added Successfully!')
            return redirect('addnewquestion')
        else:
            return render(request,'Quiz.html')

def takequiz(request,qid=1):
    data=get_object_or_404(Questions,id=qid)
    if request.method=='POST':
        selected=request.POST.get('answer')
        next_qid=qid+1
        if data.Correct_ans==selected:
            messages.success(request,f'Correct answer')
        else:
            messages.success(request,f'Incorrect answer:{selected} {data.Correct_ans}')
        if Questions.objects.filter(id=next_qid).exists():
            return redirect('taketest',next_qid)
        else:
            return HttpResponse(f'Quiz completed. Thank you for taking the test!. Your score :{total_score}')

    return render(request,'try.html',{'data':data})
def firsttest(request):
    return redirect('taketest',1)
def Staffcreationform(request):
    form=StaffUserCreationForm()
    if request.method=='POST':
        form=StaffUserCreationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            form.save()
            obj=User.objects.get(username=username)
            Staff.objects.create(user=obj,email=obj.email)
            return redirect('login')
    return render(request,'Signup.html',{'form':form})
def login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('addnewquestion')
    return render(request,'login.html')