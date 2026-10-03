from django.core.management.base import BaseCommand
from django.db import transaction

from punsalang_q2.models import PersonalInformation, Project, TechStack


PERSONAL_INFO = {
    'first_name': 'Karl Adrian',
    'middle_name': 'Tayag',
    'last_name': 'Punsalang',
    'summary': (
        "Hi, I'm Karl Adrian Punsalang, a BS Computer Engineering student "
        "based in Sto. Tomas, Pampanga, passionate about web development and "
        "programming. I build clean, modern, and interactive digital experiences."
    ),
    'contact_number': '+63 955-922-9821',
    'email': 'punsalangkarladrian7@gmail.com',
    'address': 'Sto. Tomas, Pampanga',
}

PROJECTS = [
    {
        'project_name': 'Personal Portfolio Website',
        'description': (
            'A portfolio website showcasing my skills and projects. Started as a '
            'static HTML/CSS/JavaScript page and grew into a Django app with an '
            'admin-only dashboard for managing projects and tech stacks.'
        ),
        'tech_stack': ['HTML', 'CSS', 'JavaScript', 'Python', 'Django'],
        'link': 'https://github.com/punsalang22/PORTFOLIO-WEBSITE',
    },
    {
        'project_name': 'ATM Simulation',
        'description': 'An ATM system using C++ and C-style strings.',
        'tech_stack': ['C++'],
        'link': 'https://github.com/punsalang22',
    },
    {
        'project_name': 'Student Management System',
        'description': 'A basic CRUD application for managing students.',
        'tech_stack': ['Python', 'Django'],
        'link': 'https://github.com/punsalang22',
    },
]


class Command(BaseCommand):
    help = 'Fill an empty database with my personal information, projects and tech stacks.'

    @transaction.atomic
    def handle(self, *args, **options):
        if PersonalInformation.objects.exists():
            self.stdout.write('Personal information already exists - skipped.')
        else:
            PersonalInformation.objects.create(**PERSONAL_INFO)
            self.stdout.write(self.style.SUCCESS('Added personal information.'))

        for data in PROJECTS:
            if Project.objects.filter(project_name__iexact=data['project_name']).exists():
                self.stdout.write(f'Project "{data["project_name"]}" already exists - skipped.')
                continue

            stacks = []
            for name in data['tech_stack']:
                # Reuse an existing stack (case-insensitive) so nothing is duplicated.
                stack = TechStack.objects.filter(name__iexact=name).first()
                if stack is None:
                    stack = TechStack.objects.create(name=name)
                stacks.append(stack)

            fields = {key: value for key, value in data.items() if key != 'tech_stack'}
            project = Project.objects.create(**fields)
            project.tech_stack.set(stacks)
            self.stdout.write(self.style.SUCCESS(f'Added project "{project.project_name}".'))

        self.stdout.write(self.style.SUCCESS('Done.'))
