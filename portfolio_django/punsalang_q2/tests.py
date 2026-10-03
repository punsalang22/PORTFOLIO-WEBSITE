from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Project, TechStack


class AdminLoginTests(TestCase):
    def setUp(self):
        User.objects.create_superuser('owner', 'owner@example.com', 'owner-pass-123')
        User.objects.create_user('regular', 'regular@example.com', 'regular-pass-123')
        User.objects.create_user('staffonly', 'staff@example.com', 'staff-pass-123', is_staff=True)

    def test_superuser_can_sign_in_and_is_redirected_to_dashboard(self):
        response = self.client.post(reverse('login'), {
            'username': 'owner', 'password': 'owner-pass-123',
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_regular_user_cannot_sign_in(self):
        response = self.client.post(reverse('login'), {
            'username': 'regular', 'password': 'regular-pass-123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, 'Please enter a correct username and password')

    def test_staff_user_who_is_not_superuser_cannot_sign_in(self):
        response = self.client.post(reverse('login'), {
            'username': 'staffonly', 'password': 'staff-pass-123',
        })
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_wrong_password_fails(self):
        response = self.client.post(reverse('login'), {
            'username': 'owner', 'password': 'wrong',
        })
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class DashboardAccessTests(TestCase):
    protected = [
        'dashboard', 'dashboard_projects', 'dashboard_tech_stacks',
        'project_create', 'tech_stack_create',
    ]

    def test_anonymous_users_are_sent_to_login(self):
        for name in self.protected:
            response = self.client.get(reverse(name))
            self.assertRedirects(response, f"{reverse('login')}?next={reverse(name)}")

    def test_logged_in_regular_user_is_sent_to_login(self):
        regular = User.objects.create_user('regular', password='regular-pass-123')
        self.client.force_login(regular)
        for name in self.protected:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith(reverse('login')))

    def test_superuser_can_open_every_dashboard_page(self):
        self.client.force_login(User.objects.create_superuser('owner', password='x'))
        for name in self.protected:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_logout(self):
        self.client.force_login(User.objects.create_superuser('owner', password='x'))
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 302)


class DashboardTableTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_superuser('owner', password='x'))
        self.python = TechStack.objects.create(name='Python')
        self.django = TechStack.objects.create(name='Django')
        self.project = Project.objects.create(
            project_name='Student Management System',
            description='A' * 80,
            link='https://github.com/example/sms',
        )
        self.project.tech_stack.set([self.python, self.django])
        other = Project.objects.create(project_name='Scraper', description='d', link='https://x.com')
        other.tech_stack.set([self.python])

    def test_project_table_columns(self):
        response = self.client.get(reverse('dashboard_projects'))
        self.assertContains(response, 'Student Management System')
        self.assertContains(response, 'A' * 49 + '…')       # truncated to 50 chars
        self.assertNotContains(response, 'A' * 50)
        self.assertContains(response, 'Django, Python')       # comma separated
        self.assertContains(response, '<a href="https://github.com/example/sms"')
        self.assertContains(response, reverse('project_create'))

    def test_tech_stack_table_columns(self):
        response = self.client.get(reverse('dashboard_tech_stacks'))
        self.assertContains(response, 'Python')
        self.assertContains(response, 'Scraper, Student Management System')
        self.assertContains(response, self.python.created_at.strftime('%b'))
        self.assertContains(response, reverse('tech_stack_create'))

    def test_one_tech_stack_is_shared_by_many_projects(self):
        self.assertEqual(TechStack.objects.filter(name='Python').count(), 1)
        self.assertEqual(self.python.projects.count(), 2)


class CreateViewTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_superuser('owner', password='x'))
        self.python = TechStack.objects.create(name='Python')

    def test_create_tech_stack(self):
        response = self.client.post(reverse('tech_stack_create'), {'name': 'Django'})
        self.assertRedirects(response, reverse('dashboard_tech_stacks'))
        self.assertTrue(TechStack.objects.filter(name='Django').exists())

    def test_tech_stack_name_is_required(self):
        response = self.client.post(reverse('tech_stack_create'), {'name': '   '})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')
        self.assertEqual(TechStack.objects.count(), 1)

    def test_duplicate_tech_stack_is_rejected_case_insensitively(self):
        response = self.client.post(reverse('tech_stack_create'), {'name': 'python'})
        self.assertContains(response, 'already exists')
        self.assertEqual(TechStack.objects.count(), 1)

    def test_create_project_form_lists_every_tech_stack(self):
        TechStack.objects.create(name='Django')
        response = self.client.get(reverse('project_create'))
        self.assertContains(response, 'Python')
        self.assertContains(response, 'Django')
        self.assertContains(response, '<textarea')

    def test_create_project(self):
        response = self.client.post(reverse('project_create'), {
            'project_name': 'Weather App',
            'description': 'Shows the weather.',
            'tech_stack': [self.python.pk],
            'link': 'https://github.com/example/weather',
        })
        self.assertRedirects(response, reverse('dashboard_projects'))
        project = Project.objects.get(project_name='Weather App')
        self.assertEqual(list(project.tech_stack.all()), [self.python])

    def test_create_project_fails_when_fields_are_missing(self):
        response = self.client.post(reverse('project_create'), {})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(
            set(form.errors),
            {'project_name', 'description', 'tech_stack', 'link'},
        )
        self.assertContains(response, 'Select at least one tech stack.')
        self.assertFalse(Project.objects.exists())

    def test_create_project_rejects_invalid_link(self):
        response = self.client.post(reverse('project_create'), {
            'project_name': 'X', 'description': 'Y',
            'tech_stack': [self.python.pk], 'link': 'not a url',
        })
        self.assertIn('link', response.context['form'].errors)
        self.assertFalse(Project.objects.exists())


class PublicPortfolioTests(TestCase):
    def test_new_project_shows_on_public_portfolio(self):
        stack = TechStack.objects.create(name='Rust')
        project = Project.objects.create(
            project_name='Brand New Project', description='Fresh', link='https://example.com',
        )
        project.tech_stack.add(stack)

        listing = self.client.get(reverse('project_list'))
        self.assertContains(listing, 'Brand New Project')
        self.assertContains(listing, 'Rust')

        detail = self.client.get(reverse('project_detail', args=[project.id]))
        self.assertContains(detail, 'Rust')

    def test_home_page_works_with_empty_database(self):
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)


class SeedPortfolioCommandTests(TestCase):
    def test_fills_empty_database_and_is_safe_to_rerun(self):
        from io import StringIO
        from django.core.management import call_command

        call_command('seed_portfolio', stdout=StringIO())
        call_command('seed_portfolio', stdout=StringIO())   # second run adds nothing

        from .models import PersonalInformation
        self.assertEqual(PersonalInformation.objects.count(), 1)
        self.assertEqual(Project.objects.count(), 3)
        python = TechStack.objects.get(name='Python')
        self.assertEqual(python.projects.count(), 2)          # shared, not duplicated
        self.assertContains(self.client.get(reverse('project_list')), 'ATM Simulation')
