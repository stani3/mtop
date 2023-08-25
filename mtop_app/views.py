from django.shortcuts import render
from .models import Plan, Question

# Create your views here.
def home(request):
    plans1 = Plan.objects.all()[:3]
    plans2 = Plan.objects.all()[3:6]
    questions = Question.objects.all()



    context = {
        'plans1': plans1,
        'plans2': plans2,
        'questions': questions,
    }

    return render(request, 'mtop_app/home.html', context)


