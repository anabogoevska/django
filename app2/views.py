from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.http import HttpResponseRedirect
from .forms import IndexForm, MyAuthenticationForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from app2.models import Course, Lesson
from .forms import RegisterForm, IndexForm


def Register(request):
    form_class = UserCreationForm
    form = form_class(request.POST or None)
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("login")
    return render(request, 'register.html', {'form': form})



def loginPage(request):
   if request.method == "POST":
       form = AuthenticationForm(request, data=request.POST)
       if form.is_valid():
           username = form.cleaned_data.get('username')
           password = form.cleaned_data.get('password')

           user = authenticate(username=username, password=password)
           if user is not None:
               login(request,user)
               context = {
                   "user": user
               }
               messages.info(request, f"You are logged in as {username}.")
               return redirect("home")
           else:
               messages.error(request, "Invalid username or password.")

       else:
           messages.error(request, "Invalid username or password.")
   form = AuthenticationForm()
   return render(request=request, template_name="login.html", context={"login_form": form})



@login_required(login_url='login')
def home(request):

    course_list=Course.objects.all()
    return render(request, 'home.html', {'course_list':course_list})




def index(request):
    if request.method == "POST":
        form = IndexForm(request.POST)
        if form.is_valid():
            form.save()



    context = {"form": IndexForm}
    return render(request, 'index.html', context=context)

def default(request):
    return render(request, 'default.html')


@login_required(login_url='login')
def showAllLessons(request):

    course = request.GET.get('course')

    if course == None:
        lessons = Lesson.objects.order_by('-number_of_lessons').filter(is_published=True)
    else:
        lessons = Lesson.objects.filter(course__course_name=course)

    page_num = request.GET.get("page")
    paginator = Paginator(lessons, 5)

    try:
        lessons = paginator.page(page_num)
    except PageNotAnInteger:
        lessons=paginator.page(1)
    except EmptyPage:
        lessons= paginator.page(paginator.num_pages)

    courses = Course.objects.all()
    context = {
        'lessons': lessons,
        'courses': courses
    }

    return render(request, 'lessons.html', context)

def lessons_list(request, course_course_name=None):
    course = None
    courses = Course.objects.all()
    lesson = Lesson.objects.all()
    if course_course_name:
        course = get_object_or_404(Course, course_name = course_course_name)
        lesson = lesson.filter(course=course)

    return render(request, 'lessons.html', {'courses':courses,
                                            'course': course,
                                             'lesson': lesson
                                            })
def logOutPage(request):
    logout(request)
    return redirect("default")


@login_required(login_url='login')
def lessonsContent(request, id):
    obj = get_object_or_404(Lesson, pk=id)
    return render(request, 'lessonsContent.html', {'obj':obj})

@login_required(login_url='login')
def lessonsList(request, course_slug=None):
    lessons= None
    courses = Course.get_all_courses()
    course_name = request.GET('course')
    if course_name:
        lessons=Lesson.get_all_lessons_by_course_name(course_name)
    else:
        lessons=Lesson.get_all_lessons()
