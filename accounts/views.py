from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required  # ADD THIS LINE
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from courses.models import Enrollment, Course 
from .models import User

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('accounts:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def dashboard_view(request):
    context = {'role': request.user.role}

    # Student dashboard context
    if request.user.role == 'student':
        enrolled_courses = Enrollment.objects.filter(student=request.user).select_related('course')
        context.update(
            enrolled_courses=enrolled_courses,
            enrolled_courses_count=enrolled_courses.count(),
            overall_progress=0,
            certificates_count=0,
        )

    # Teacher dashboard context
    elif request.user.role == 'teacher':
        teaching_courses = Course.objects.filter(teacher=request.user)
        context.update(
            teaching_courses=teaching_courses,
            teaching_courses_count=teaching_courses.count(),
            total_students_count=Enrollment.objects.filter(course__in=teaching_courses).values('student_id').distinct().count(),
            materials_uploaded_count=0,
            teacher_activities=[],
        )

    # Admin dashboard context
    elif request.user.role == 'admin':
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()
        context.update(
            total_users=UserModel.objects.count(),
            total_students=UserModel.objects.filter(role='student').count(),
            total_teachers=UserModel.objects.filter(role='teacher').count(),
            total_courses=Course.objects.count(),
            active_courses=Course.objects.count(),
            active_courses_percent=0,
            user_growth=0,
            completion_rate=0,
            recent_registrations=[],
        )

    return render(request, 'dashboard.html', context)