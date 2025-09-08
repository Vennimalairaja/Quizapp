from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import Questions,Staff,Question,Students
from .forms import QuestionForm,StaffUserCreationForm,StudentDetailsForm,StudentAddForm
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .sendmail import send_email
# Create your views here.
def render_dashboard(request):
    if not hasattr(request.user,'staff'):
        return redirect('unauthorized')
    return render(request,'dashboard.html')

def addnewquestion(request):
    if not hasattr(request.user,'staff'):
        return redirect('login')
    else:
        if request.method=='POST':
            question=request.POST.get('question')
            Option_a=request.POST.get('option_a')
            Option_b=request.POST.get('option_b')
            Option_c=request.POST.get('option_c')
            Option_d=request.POST.get('option_d')
            Correct=request.POST.get('correct')
            data=Question.objects.create(Question=question,Option_a=Option_a,Option_b=Option_b,Option_c=Option_c,Option_d=Option_d,
            Correct_ans=Correct,Staff=request.user.staff)
            messages.success(request,'Question added Successfully!')
            return redirect('addnewquestion')
        else:
            return render(request,'Quiz.html')

def takequiz(request,qid=1):
    Questions=Question.objects.filter(Staff=request.user.students.Staff)
    data=Questions[qid-1]
    student=Students.objects.get(Student=request.user)
    if request.method=='POST':
        selected=request.POST.get('answer')
        next_qid=qid+1
        if data.Correct_ans==selected:
            student.score+=1
            student.save()
        else:
            messages.success(request,f'Incorrect answer:{selected} {data.Correct_ans}')
        if qid<len(Questions):
            return redirect('taketest',next_qid)
        else:
            return HttpResponse(f'Quiz completed. Thank you for taking the test!. {request.user}Your score :{student.score}')

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
    if request.user.is_authenticated:
        if hasattr(request.user,'staff'):
            return redirect('dashboard')
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if not hasattr(request.user,'staff'):
                return redirect('unauthorized')
            return redirect('dashboard')
        else:
            return render(request,'login.html',{'form':"Username and password doesn't match" })
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def unauthorized_view(request):
    return render(request,'unauthorized.html')

def add_students_view(request):
    form=StudentAddForm()
    if request.method=='POST':
        form=StudentAddForm(request.POST)
        if form.is_valid():
            student_name=form.cleaned_data['username']
            Email=form.cleaned_data['email']
            if does_user_exist(Email):
                messages.success(request,f'Student already exists !.Try adding another Student')
                return render(request,'addStudents.html',{'form':form})
            user1=form.save(commit=False)
            user1.set_password("Kendrick@579")
            user1.save()
            user=User.objects.get(username=student_name)
            student=Students.objects.create(Student_name=student_name,
            Email=Email,Staff=request.user.staff,Student=user,score=0)
            content=f'''Hello {student.Student_name},

You have been invited to take a test assigned by {student.Staff.user.username}.

📝 Test Details:  
- Assigned by: {student.Staff.user.username}  
- Your Username: {student.Student_name}  
- Your Password: Kendrick@579  

Please log in to the Quiz Portal using the above credentials and complete the test within the given time.  

👉 Login here: http://127.0.0.1:8000/studentLogin

We wish you the best of luck!  
If you face any issues logging in, please contact your teacher/staff.  

Best regards,  
Quiz App Team
'''
            send_email(receiver=student.Email,Subject='Invitation to take your Quiz test',content=content)
            messages.success(request,f'Student details Updated Succesfully!. {student_name} will be notified of the test')
            return render(request,'addStudents.html',{'form':form})
        else:
            return HttpResponse(f'Invalid form {form.errors}')
    return render(request,'addStudents.html',{'form':form})

def does_user_exist(Email):
    all_Students=Students.objects.all()
    out=False
    for i in all_Students:
        if i.Email==Email:
            return True
    return out

def studentDashboard_view(request):
    return render(request,'studentDashboard.html')

def StudentLogin(request):
    if request.user.is_authenticated:
        if hasattr(request.user,'students'):
            return redirect('student-Dashboard')
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if not hasattr(request.user,'students'):
                return redirect('unauthorized')
            return redirect('student-Dashboard')
        else:
            messages.success(request,'Wrong Credentials! Try Again')
            return render(request,'StudentLogin.html')
    return render(request,'StudentLogin.html')