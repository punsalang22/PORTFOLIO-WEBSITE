from django.shortcuts import render, get_object_or_404
from .models import Project, PersonalInformation

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'project_detail.html', {'project': project})

def personal_info(request):
    info = PersonalInformation.objects.first()
    return render(request, 'personal_info.html', {'info': info})