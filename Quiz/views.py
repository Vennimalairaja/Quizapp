from django.shortcuts import render,redirect
from .models import Questions
from .forms import QuestionForm
# Create your views here.
def addquestion(request):
    form=QuestionForm()
    if request.method=='POST':
        form=QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addquestions')
    else:
        return render(request,'Quiz.html',{'form':form})
def takequiz(request):
    data=Questions.objects.all()
    return render(request,'takeQuiz.html',{'data':data})