from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import Questions,Staff,Question,Students,Student_results
from .forms import QuestionForm,StaffUserCreationForm,StudentDetailsForm,StudentAddForm
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .sendmail import send_email
# Create your views here.
def custom_csrf_view(request,reason=''):
    return redirect('login')

def custom_permission_denied(request,exception=None):
    return render(request,'404.html')

def render_dashboard(request):
    if not hasattr(request.user,'staff'):
        return redirect('login')
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
    student=request.user.students
    if student.took_test==True:
        messages.success(request,'You completed the test. Thank you!')
        return redirect('student-Dashboard')
    else:
        Questions=Question.objects.filter(Staff=request.user.students.Staff)
        data=Questions[qid-1]
        student=Students.objects.get(Student=request.user)
        if request.method=='POST' and student.took_test==False:
            selected=request.POST.get('answer')
            next_qid=qid+1
            if data.Correct_ans==selected:
                student.score+=1
                student.save()
                
            else:
                if student.score>0:
                    student.score-=1
                    student.save()
            result=Student_results.objects.create(student=request.user.students,
                Question=data.Question,student_answer=selected,correct_answer=data.Correct_ans)
            if qid<len(Questions):
                return redirect('taketest',next_qid)
            else:
                content=f''' 
                Dear {request.user},

    Thank you for attending and completing the exam. We truly appreciate the time and effort you put into taking this test.

    Your performance has been recorded successfully. Please find your login details below for your reference:

    Username: {request.user}

    Password: Kendrick@579

    Your total score :{request.user.students.score}

    You can log in anytime to check your score and view further updates from {request.user.students.Staff} (your assigned staff).

    Once again, thank you for your participation. We wish you the very best in your learning journey!

    Best regards,
    {request.user.students.Staff}
    QuizApp Team
                '''
                student.took_test=True
                student.save()
                send_email(receiver=request.user.students.Email,Subject='Thank you for completing the Exam',content=content)
                messages.success(request,'Test completed you can log out!')
                return redirect('student-Dashboard')
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
            user=Staff.objects.create(user=obj,email=obj.email)
            content=f'''
            Hi {username},

Welcome to QuizTrack! 🚀
We’re excited to have you on board. With QuizTrack, you can:

✅ Create and manage quizzes for your students
✅ Add students and assign quizzes to them
✅ Track each student’s score and monitor their overall progress

Getting started is simple:

Log in to your dashboard

Add your students

Create your first quiz and start tracking results

👉 [http://127.0.0.1/dashboard]

If you ever need help, feel free to reply to this email—we’re here to support you.

Happy teaching,
The QuizTrack Team
            '''
            send_email(receiver=user.email,Subject='🎉 Welcome to QuizTrack – Start Creating Your First Quiz!',content=content)
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

def staff_results_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user,'staff'):
            data=request.user.staff.students_set.all().order_by('-score')
            return render(request,'staff_results.html',{'students':data})
        return redirect('unauthorized')
    else:
        return redirect('unauthorized')
def add_students_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user,'staff'):
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
            
                    content=f'''
                    Dear {student.Student_name},

We’re happy to inform you that {student.Staff} has added you to their students list on QuizApp. 🎉

As part of this, you may receive notifications about upcoming tests assigned to you. Make sure to check your email regularly so you don’t miss any important updates.

👉 Keep in mind:

You’ll be notified when a test is scheduled.

You can log in to your account anytime to view your details.

If you have any questions, please reach out to {student.Staff} directly.

We’re excited to have you with us, and wish you the best in your learning journey!

Best regards,
QuizApp Team
                    '''    
                    messages.success(request,f'Student details Updated Succesfully!. {student_name} will be notified of the test')
                    return render(request,'addStudents.html',{'form':form})
                elif request.method=='POST' and request.POST.get('action')=='inform':
                    all_students=Students.objects.all()
                    for i in all_students:
                        content=f'''Hello {i.Student_name},

        You have been invited to take a test assigned by {i.Staff.user.username}.

        📝 Test Details:  
        - Assigned by: {i.Staff.user.username}  
        - Your Username: {i.Student_name}  
        - Your Password: Kendrick@579  

        Please log in to the Quiz Portal using the above credentials and complete the test within the given time.  

        👉 Login here: http://127.0.0.1:8000/studentLogin

        We wish you the best of luck!  
        If you face any issues logging in, please contact your teacher/staff.  

        Best regards,  
        Quiz App Team
        '''
                        send_email(receiver=i.Email,Subject='Invitation to take your Quiz test',content=content)
                    messages.success(request,'Mailed sent successfully!')
                    return render(request,'addStudents.html',{'form':form})                
                else:
                    return HttpResponse(f'Invalid form {form.errors}')
            return render(request,'addStudents.html',{'form':form})
    else:
        return redirect('unauthorized')


def does_user_exist(Email):
    all_Students=Students.objects.all()
    out=False
    for i in all_Students:
        if i.Email==Email:
            return True
    return out

def studentDashboard_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user,'students'):
            return render(request,'studentDashboard.html')
        return redirect('unauthorized')
    else:
        return redirect('unauthorized')

def view_score_staff(request,student):
    student=Students.objects.get(Student_name=student)
    data=Student_results.objects.filter(student=student)
    score=student.score
    return render(request,'view_score.html',{'answers':data,'score':score,'student':student.Student_name})

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
def update_students_view(request):
    students=Students.objects.all()
    if request.method=='POST':
        if request.POST.get('action')=='update':
            username=request.POST.get('student_id')
            Email=request.POST.get('email')
            student_obj=None
            for i in students:
                if i.Student_name==username:
                    student_obj=i
            student_obj.Email=Email
            student_obj.save()
            messages.success(request,'Email updated successfully!')
            return render(request,'Studentdashboard.html',{'students':students})
        elif request.POST.get('action')=='delete':
            username=request.POST.get('student_id')
            student_obj=None
            for i in students:
                if i.Student_name==username:
                    student_obj=i
            if student_obj is None:
                messages.success(request,'Student doesn\'t exist')
                return render(request,'Studentdashboard.html',{'students':students})
            student_obj.delete()
            messages.success(request,'Student details deleted Successfully!')
            return render(request,'Studentdashboard.html',{'students':students})
        else:
            return redirect('staff-view')
    if request.method=='POST' and request.POST.get('action')=='inform':
        all_students=Students.objects.all()
        for i in all_students:
            content=f'''Hello {i.Student_name},

        You have been invited to take a test assigned by {i.Staff.user.username}.

        📝 Test Details:  
        - Assigned by: {i.Staff.user.username}  
        - Your Username: {i.Student_name}  
        - Your Password: Kendrick@579  

        Please log in to the Quiz Portal using the above credentials and complete the test within the given time.  

        👉 Login here: http://127.0.0.1:8000/studentLogin

        We wish you the best of luck!  
        If you face any issues logging in, please contact your teacher/staff.  

        Best regards,  
        Quiz App Team
        '''
            send_email(receiver=i.Email,Subject='Invitation to take your Quiz test',content=content)
        messages.success(request,'Invitation sent successfully!')
        return render(request,'Studentdashboard.html',{'students':students})
    return render(request,'Studentdashboard.html',{'students':students})

def score_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user,'students'):
            student_result=Student_results.objects.filter(student=request.user.students)
            score=request.user.students.score
            return render(request,'view_score.html',{"answers":student_result,"score":score})
        elif  hasattr(request.user,'staff'):
            data=request.user.staff.students_set.all().order_by('-score')
            return render(request,'staff_results.html',{'students':data})
    else:
        return redirect('unauthorized')