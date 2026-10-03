from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ProjectForm, SuperuserAuthenticationForm, TechStackForm
from .models import Project, PersonalInformation, TechStack


# ---------- Public portfolio ----------

def project_list(request):
    projects = Project.objects.prefetch_related('tech_stack')
    return render(request, 'project_list.html', {'projects': projects})

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'project_detail.html', {'project': project})

def personal_info(request):
    info = PersonalInformation.objects.first()
    return render(request, 'personal_info.html', {'info': info})


# ---------- Admin-only sign-in ----------

class AdminLoginView(LoginView):
    template_name = 'dashboard/login.html'
    authentication_form = SuperuserAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


# Any non-superuser (anonymous or regular account) is sent to the sign-in page.
superuser_required = user_passes_test(
    lambda user: user.is_active and user.is_superuser,
    login_url='login',
)


# ---------- Dashboard ----------

@superuser_required
def dashboard(request):
    return render(request, 'dashboard/home.html', {
        'project_count': Project.objects.count(),
        'tech_stack_count': TechStack.objects.count(),
    })

@superuser_required
def dashboard_projects(request):
    projects = Project.objects.prefetch_related('tech_stack').order_by('project_name')
    return render(request, 'dashboard/project_list.html', {'projects': projects})

@superuser_required
def dashboard_tech_stacks(request):
    tech_stacks = TechStack.objects.prefetch_related(
        Prefetch('projects', queryset=Project.objects.order_by('project_name'))
    )
    return render(request, 'dashboard/tech_stack_list.html', {'tech_stacks': tech_stacks})

@superuser_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Project "{project.project_name}" was created.')
            return redirect('dashboard_projects')
    else:
        form = ProjectForm()
    return render(request, 'dashboard/project_form.html', {
        'form': form,
        'has_tech_stacks': TechStack.objects.exists(),
    })

@superuser_required
def tech_stack_create(request):
    if request.method == 'POST':
        form = TechStackForm(request.POST)
        if form.is_valid():
            tech_stack = form.save()
            messages.success(request, f'Tech stack "{tech_stack.name}" was created.')
            return redirect('dashboard_tech_stacks')
    else:
        form = TechStackForm()
    return render(request, 'dashboard/tech_stack_form.html', {'form': form})
